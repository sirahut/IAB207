from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Model
from flask import Blueprint, render_template, request, session
from PhoneApp.forms import AuctionsForm
from PhoneApp.models import Auctions, User
from PhoneApp import auctions

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    auctions = Auctions.query.filter_by().all()
    return render_template('index.html', auctions=auctions)

# def search():


@bp.route('/search')
def search():
    if request.args['search']:
        auc = "%" + request.args['search'] + '%'

        auctions = Auctions.query.filter(
            Auctions.title.like(auc)).all()
        return render_template('index.html', auctions=auctions)
    else:
        return redirect(url_for('main.index'))
