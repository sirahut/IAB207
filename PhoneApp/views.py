<<<<<<< Updated upstream
from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Model
=======
from flask import Blueprint, render_template, request, session
from PhoneApp.forms import AuctionsForm
from PhoneApp.models import Auctions, User
>>>>>>> Stashed changes

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    auction_item = AuctionsForm()
    user = User.query.filter_by().first()
    auction = Auctions.query.filter_by().all()


    return render_template('index.html', user=user)

# def search():


@bp.route('/search')
def search():
    if request.args['search']:
        mod = "%" + request.args['search'] + '%'
        model = Model.query.filter(
            Model.name.like(mod)).all()
        return render_template('base.html', model=model)
    else:
        return redirect(url_for('main.index'))
