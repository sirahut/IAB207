from flask import Blueprint, render_template, url_for, redirect
from .models import Watchlist, Auctions, User
from .forms import WatchListForm
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from sqlalchemy import func
from PhoneApp.forms import AuctionsForm, ReviewForm
from PhoneApp.models import Auctions, Review, Bid
from werkzeug.utils import secure_filename
from PhoneApp.auctions import check_upload_file
from flask.helpers import flash


# create blueprint
bp = Blueprint('watchlist', __name__, url_prefix='/watchlists')

# render template


@bp.route('/<id>')
@login_required
def watchlist(id):
    # the "id" has to be id of the user_id
    user = User.query.filter_by(id=id).first()

    # this will set to None if there are no watchlists
    are_there_any = Watchlist.query.filter_by(user_id=id).first()

    # get all watchlists of current user from database
    watchlists = Watchlist.query.filter_by(user_id=id).all()

    # if there are auctions in the watchlist
    if watchlists is not None:
        # get auction_id for each auction in the watchlist
        for watchlist in watchlists:
            if watchlist.auction is not None:
                auction_id = watchlist.auction.id

                auction = Auctions.query.filter_by(id=auction_id).first()

                # initail as none
                watchlist.current_bid2f = None
                # get current bid from the database
                current_bid = db.session.query(
                    func.max(Bid.bid_amount)).filter_by(auction_id=auction_id).scalar()
                # format to 2 decimal number
                if current_bid is not None:
                    watchlist.current_bid2f = "{:.2f}".format(current_bid)

                # starting bid
                starting_bid = (float(auction.open_bid))

                # bid number count
                watchlist.bid_number = Bid.query.filter_by(
                    auction_id=auction_id).count()

                # priceControl
                # add one to starting bid/ current bid
                if current_bid is None:
                    priceControl = starting_bid + 1
                else:
                    priceControl = current_bid + 1
                # format 2 decimal number
                watchlist.priceControl2f = "{:.2f}".format(priceControl)

    return render_template('watchlist/watchlist.html', watchlists=watchlists, user=user, are_there_any=are_there_any)


@bp.route('/<id>/add', methods=['GET', 'POST'])
@login_required
def add_to_watchlist(id):
    # get WatchlistForm
    watchlist_form = WatchListForm()
    # get an auction from the database
    auction = Auctions.query.filter_by(id=id).first()

    # ------- Add to Watchlist function -----
    watchlistAdded = Watchlist.query.filter_by(
        user_id=current_user.id).filter_by(auction_id=id).first()
    # if there is no this auction in the watchlist
    # Add to Watchlist button
    if watchlistAdded is None:
        if watchlist_form.validate_on_submit():
            watchlist = Watchlist(auction=auction, user=current_user)

            db.session.add(watchlist)
            db.session.commit()

            return redirect(url_for('auction.show', id=id))

   # if the auction already in the watchlist
    else:
        # Remove button
        if watchlist_form.validate_on_submit():
            # find that auction in the Watchlist table
            Watchlist.query.filter_by(auction_id=id).delete()

            db.session.commit()
            return redirect(url_for('auction.show', id=id))
# -------- end of watchlist button and function ---------
