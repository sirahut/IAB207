from flask import Blueprint, render_template, url_for, redirect, request
from .models import Auctions, Review
from travel.forms import AuctionsForm, ReviewForm
from .forms import AuctionsForm, ReviewForm

from datetime import datetime
from . import db
from . import Auctions
import os
from werkzeug.utils import secure_filename


# create blueprint
bp = Blueprint('auction', __name__, url_prefix='/auctions')


@bp.route('/<id>')
def show(id):
    #destination = get_destination()
    return render_template('auctions/show.html')
