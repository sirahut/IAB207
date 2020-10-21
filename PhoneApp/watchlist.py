from flask import Blueprint, render_template, url_for, redirect
from .models import Watchlist, Auctions, User
from .forms import WatchListForm
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from PhoneApp.forms import AuctionsForm, ReviewForm
from PhoneApp.models import Auctions, Review
from werkzeug.utils import secure_filename
from PhoneApp.auctions import check_upload_file


# create blueprint
bp = Blueprint('watchlist', __name__, url_prefix='/watchlists')

# render template


@bp.route('/<id>')
@login_required
def watchlist(id):
    # the "id" has to be id of the user_id
    user = User.query.filter_by(id=id).first()
    watchlists = Watchlist.query.filter_by(user_id=id).all()
    #auction = Auctions.query.filter_by(id=auction_id)

    return render_template('watchlist/watchlist.html', user=user)


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
