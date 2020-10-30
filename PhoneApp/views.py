from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Model
from flask import Blueprint, render_template, request, session
from PhoneApp.forms import AuctionsForm
from PhoneApp.models import Auctions, Bid, User
from PhoneApp import auctions
from sqlalchemy import func
from datetime import datetime
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    auctions = Auctions.query.filter_by().all()
    bids = Bid.query.filter_by().all()
    users = User.query.filter_by().all()
    full_page = 'Yes'

    # grab attribute of the auction
    for auction in auctions:
        # starting_bid
        starting_bid = (float(auction.open_bid))

        # current_bid
        current_bid = db.session.query(
            func.max(Bid.bid_amount)).filter_by(auction_id=auction.id).scalar()
        # if current is not None format to 2 decimal
        if current_bid is not None:
            auction.current_bid = "${:.2f}".format(current_bid)
        # if there are no bids on this auction show starting bid instead
        else:
            auction.current_bid = "${:.2f}".format(starting_bid)
        # bid number
        auction.bid_number = Bid.query.filter_by(
            auction_id=auction.id).count()
        auction.timeleft = auction.end - datetime.now()

    return render_template('index.html', auctions=auctions, bids=bids, users=users, full_page=full_page)


@bp.route('/search')
def search():
    if request.args['search']:
        bids = Bid.query.filter_by().all()
        users = User.query.filter_by().all()
        auc = "%" + request.args['search'] + '%'
        auctions = Auctions.query.filter(
            Auctions.title.like(auc)).all()
        full_page = 'No'

        # grab attribute of the auction
        for auction in auctions:
            # starting_bid
            starting_bid = (float(auction.open_bid))

            # current_bid
            current_bid = db.session.query(
                func.max(Bid.bid_amount)).filter_by(auction_id=auction.id).scalar()
            # if current is not None format to 2 decimal
            if current_bid is not None:
                auction.current_bid = "${:.2f}".format(current_bid)
            # if there are no bids on this auction show starting bid instead
            else:
                auction.current_bid = "${:.2f}".format(starting_bid)
            # bid number
            auction.bid_number = Bid.query.filter_by(
                auction_id=auction.id).count()
            auction.timeleft = auction.end-datetime.now()

        return render_template('index.html', auctions=auctions, bids=bids, users=users, full_page=full_page)
    else:
        return redirect(url_for('main.index'))
