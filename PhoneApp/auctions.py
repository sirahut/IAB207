from flask import Blueprint, render_template, url_for, redirect, request
from .models import Auctions, Review
from .forms import AuctionsForm, ReviewForm
from flask_login import login_required, current_user
from datetime import datetime
from . import db
import os
from werkzeug.utils import secure_filename


# create blueprint
bp = Blueprint('auction', __name__, url_prefix='/auctions')


@bp.route('/<id>')
def show(id):
    auction = Auctions.query.filter_by(id=id).first()
    review_form = ReviewForm()
    return render_template('auctions/show.html', auction=auction, form=review_form)


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
        auctions = Auctions(name=create_form.name.data,
                            brand=create_form.brand.data,
                            model=create_form.model.data,
                            condition=create_form.condition.data,
                            description=create_form.description.data,
                            image=db_file_path,
                            open_bid=create_form.open_bid.data,
                            # start=create_form.open_bid.data,
                            user=current_user)

        db.session.add(auctions)
        db.session.commit()

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
                    auction_id=auction_obj, user_id=current_user)

    db.session.add(review)
    db.session.commit()
    if review_form_instance.validate_on_submit():  # this is true only in case of POST method
        print(
            f'Review form is valid. The review was {review_form_instance.review.data}')
    else:
        print('Review form is invalid')
# notice the signature of url_for
    return redirect(url_for('auction.show', id=id))
