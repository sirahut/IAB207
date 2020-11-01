from flask import Blueprint, render_template, url_for, redirect, request
from .models import Auctions, Review, Bid, Watchlist
from .forms import AuctionsForm, ReviewForm, WatchListForm, PlaceBidForm
from flask_login import login_required, current_user
from datetime import datetime
from . import db
import os
from werkzeug.utils import secure_filename
from flask_wtf.form import FlaskForm
from flask.helpers import flash
from unicodedata import name
from sqlalchemy.databases import mysql, sqlite
from sqlalchemy import func
from sqlalchemy.sql.functions import user
from PhoneApp.models import User
from werkzeug.exceptions import abort
import sqlalchemy
from sqlalchemy.engine import create_engine


# create blueprint
bp = Blueprint('auction', __name__, url_prefix='/auctions')


@bp.route('/<id>',  methods=['GET', 'POST'])
def show(id):
    # get auction from database
    auction = Auctions.query.filter_by(id=id).first()
    # get all the form
    placebid = PlaceBidForm()
    review_form = ReviewForm()
    watchlist_form = WatchListForm()
# --------- attribute on the page show.html ----------
    # initial as None
    current_bid2f = None
    starting_bid = None
    starting_bid2f = None
    bid_number = None
    priceControl2f = None
    timeleft = auction.end-datetime.now()

    # get current bid from the database
    current_bid = db.session.query(
        func.max(Bid.bid_amount)).filter_by(auction_id=id).scalar()

    # format 2 decimal number
    if current_bid is not None:
        current_bid2f = "{:.2f}".format(current_bid)

    # starting bid
    if auction is not None:
        starting_bid = (float(auction.open_bid))
    # format 2 decimal number
        starting_bid2f = "{:.2f}".format(starting_bid)
    # bid number count
        bid_number = Bid.query.filter_by(auction_id=id).count()

    # priceControl
        priceControl = ''
    # add one to starting bid/ current bid
        if current_bid is None:
            priceControl = starting_bid + 1
        else:
            priceControl = current_bid + 1
    # format 2 decimal number
        priceControl2f = "{:.2f}".format(priceControl)

# ------- watchlist button --------
    add_to_watchlist_button = ''
    # if the user not logged in the button will show 'Add to Watchlist'
    if not current_user.is_authenticated:
        add_to_watchlist_button = 'Add to Watchlist'
    # check if user already have this auction in the watchlist
    else:
        watchlistAdded = Watchlist.query.filter_by(
            user_id=current_user.id).filter_by(auction_id=id).first()
        # if there is no this auction in the watchlist
        if watchlistAdded is None:
            add_to_watchlist_button = 'Add to Watchlist'

        # if the auction already in the watchlist
        else:
            # set button to "Remove from Watchlist"
            add_to_watchlist_button = 'Remove from Watchlist'

# -------- end of watchlist button ---------

# -------- Select the winner when auction is closed
    won_user = None
    if current_bid is not None:
        # The user that won the auction is the user that placed the current bid when it's closed
        won_user = Bid.query.filter_by(
            bid_amount=current_bid).filter_by(auction_id=auction.id).first().user.name

# -------- Views all bids ----------------
    all_bids = Bid.query.filter_by(
        auction_id=id).order_by(Bid.bid_amount).all()
    # counting number from 1
    count = 1
    for bid in all_bids:
        bid.count = count
        count += 1

    return render_template('auctions/show.html', auction=auction, review_form=review_form, watchlist=watchlist_form, bid_form=placebid, current_bid=current_bid2f, bid_number=bid_number,
                           starting_bid=starting_bid2f, priceControl=priceControl2f, add_to_watchlist_button=add_to_watchlist_button, all_bids=all_bids, timeleft=timeleft, won_user=won_user)


@bp.route('/<id>/bid', methods=['GET', 'POST'])
@login_required
def placebid(id):
    placebid = PlaceBidForm()
    # --------placebid function--------
    if placebid.validate_on_submit():
        # get auction from database
        auction = Auctions.query.filter_by(id=id).first()
        # grab bid amount from the form (user input)
        bid_amount = placebid.bid_amount.data
        # starting bid
        starting_bid = (float(auction.open_bid))
        # get current bid from the database
        current_bid = db.session.query(
            func.max(Bid.bid_amount)).filter_by(auction_id=id).scalar()

        error = None
        # if there are no bids at all
        if current_bid is None:
            # bid amount(user input) has to be greater than open bid
            if (bid_amount < starting_bid):
                error = 'Bid amount has to be greater than starting bid'
        # if bid amount(user input) is less than current bid
        elif bid_amount < current_bid:
            error = 'Bid amount must be greater than current bid'
        # if the bid amount is valid
        if error is None:
            # update to the database
            bid = Bid(bid_amount=placebid.bid_amount.data,
                      auction=auction, user=current_user)
            db.session.add(bid)
            db.session.commit()
            # refresh the page
            return redirect(url_for('auction.show', id=id))
        else:
            # render the error to show.html
            flash(error, "danger")
            print('bid amount is invalid')
    return redirect(url_for('auction.show', id=id))
# ------- end of bid function --------


def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)

    upload_path = os.path.join(
        BASE_PATH, 'static/images', secure_filename(filename))
    db_upload_path = '/static/images/' + secure_filename(filename)
    # save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    create_form = AuctionsForm()
    if create_form.validate_on_submit():
        db_file_path = check_upload_file(create_form)
        auctions = Auctions(title=create_form.title.data,
                            brand=create_form.brand.data,
                            model=create_form.model.data,
                            condition=create_form.condition.data,
                            description=create_form.description.data,
                            image=db_file_path,
                            open_bid=create_form.open_bid.data,
                            start=create_form.start.data,
                            end=create_form.end.data,
                            user=current_user)

        db.session.add(auctions)
        db.session.commit()
        message = "The list has been created successfully"
        flash(message, "success")
        print('Successfully created new auction listing', 'success')
        return redirect(url_for('auction.create'))

    return render_template('auctions/create.html', form=create_form)


@bp.route('/<id>/review', methods=['GET', 'POST'])
@login_required
def review(id):
    # here the form is created
    review_form_instance = ReviewForm()
    auction_obj = Auctions.query.filter_by(id=id).first()
    review = Review(text=review_form_instance.review.data,
                    auction=auction_obj, user=current_user)

    db.session.add(review)
    db.session.commit()
    if review_form_instance.validate_on_submit():  # this is true only in case of POST method
        print(
            f'Review form is valid. The review was {review_form_instance.review.data}')
    else:
        print('Review form is invalid')
# notice the signature of url_for
    return redirect(url_for('auction.show', id=id))


@bp.route('/listed/<id>', methods=['GET'])
@login_required
def listed(id):
    user = User.query.filter_by(id=id).first()

    for auction in user.auctions:
        # grab current bid from database
        current_bid = db.session.query(
            func.max(Bid.bid_amount)).filter_by(auction_id=auction.id).scalar()
        if current_bid is not None:
            # format to two decimal places
            auction.current_bid = "${:.2f}".format(current_bid)
            # initialise as None
        auction.won_user = None
        if current_bid is not None:
            # The user that won the auction is the user that placed the current bid when it's closed
            auction.won_user = Bid.query.filter_by(
                bid_amount=current_bid).filter_by(auction_id=auction.id).first().user.name

    if user != current_user:
        return redirect(url_for('main.index', id=id))
    return render_template('auctions/listed.html', user=user)


@bp.route("/delete/<id>", methods=['GET', 'POST'])
@login_required
def delete_component(id):
    # this is a function to close auction
    if request.method == 'POST':
        status = Auctions.query.get(id)
        # status = Auctions.query.filter_by(
        #     id=id).update(dict(status='Closed'))
        status.status = "Closed"
        db.session.commit()
        return redirect(url_for('auction.listed', id=current_user.id))
    else:
        return("/")


@bp.route("/listed/<id>/updated", methods=['GET', 'POST'])
@login_required
def edit_component(id):

    user = Auctions.query.filter_by(id=id)
    auction_item = AuctionsForm()
# currently empty function

    return render_template('auctions/update.html', id=id, user=user, form=auction_item)


@bp.route('/categories')
def index():
    return "This is your category"

# route to allow users to search
