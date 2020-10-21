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
def watchlist(id):
    # the "id" has to be id of the user_id
    user = User.query.filter_by(id=id).first()
    watchlists = Watchlist.query.filter_by(user_id=id).all()
    #auction = Auctions.query.filter_by(id=auction_id)

    return render_template('watchlist/watchlist.html', user=user)
