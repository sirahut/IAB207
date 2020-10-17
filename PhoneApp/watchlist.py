from flask import Blueprint, render_template, url_for, redirect
from .models import Auctions

from flask_login import login_required, current_user
from datetime import datetime
from . import db


# create blueprint
bp = Blueprint('watchlist', __name__, url_prefix='/watchlists')

# render template
@bp.route('/<id>')
def show(id):
    watchlist = Auctions.query.filter_by(id=id).first()
    
    return render_template('auctions/show.html', auction=auction)

# 