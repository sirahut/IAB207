from flask import Blueprint, render_template, url_for, redirect, request
from .models import Auctions, Review
from .forms import AuctionsForm, ReviewForm


from datetime import datetime
from . import db
import os
from werkzeug.utils import secure_filename
from flask_wtf import form
from wtforms.fields.core import DateField


# create blueprint
bp = Blueprint('auction', __name__, url_prefix='/auctions')


@bp.route('/<id>')
def show(id):
    auction = Auctions.query.filter_by(id=id).first()
    comment_form = ReviewForm()
    return render_template('auctions/show.html', auctions=auction, form=comment_form)

@bp.route('/<id>/comment', methods=['GET', 'POST'])
def comment(id):
    comment_form = ReviewForm()
    if form.validate_on_submit():
        print("Comment posted by the user:  ", comment_form.text.data)
    return redirect(url_for('auction.show', id=1))

@bp.route('/create', methods=['GET', 'POST'])
def create():
    print('Method type: ', request.method)
    create_form = AuctionsForm()
    if create_form.validate_on_submit():
        auctions = Auctions(name=create_form.name.data,
                            brand=create_form.brand.data,
                            model=create_form.model.data,
                            condition=create_form.model.data,
                            description=create_form.model.data,
                            image=create_form.image.data,
                            open_bid=create_form.open_bid.data,
                            start=create_form.open_bid.data)


        db.session.add(auctions)
        db.session.commit()

    
        print('Successfully created new auction listing', 'success')
        return redirect(url_for('auction.create'))

    return render_template('auctions/create.html', form=create_form)

