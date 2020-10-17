from flask import Blueprint, render_template, url_for, redirect, request
from .models import Watchlist

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
    watchlist = Watchlist.query.filter_by(id=id).first()

    return render_template('watchlist/watchlist.html', watchlist=watchlist)


# @bp.route('/<id>/addWatchlist', methods=['GET', 'POST'])
# @login_required
# def add_to_watchlist(id):

#         # here the form is created
#         review_form_instance = ReviewForm()
#         auction_obj = Auctions.query.filter_by(id=id).first()
#         review = Review(text=review_form_instance.review.data,
#                         auction=auction_obj, user=current_user)

#         db.session.add(review)
#         db.session.commit()
#         if review_form_instance.validate_on_submit():  # this is true only in case of POST method
#             print(
#                 f'Review form is valid. The review was {review_form_instance.review.data}')
#         else:
#             print('Review form is invalid')
#     # notice the signature of url_for
#         return redirect(url_for('auction.show', id=id)

