from flask import Blueprint, session, redirect, url_for, render_template
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

bp = Blueprint('auth', __name__, url_prefix='/authentication')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        session['email'] = login_form.user_name.data
        return redirect(url_for('auth.login'))

    return render_template('authentication/login.html', form=login_form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        return redirect(url_for('auth.login'))

    return render_template('authentication/register.html', form=register_form)


@bp.route('/logout')
def logout():
    session.clear()
    return render_template('authentication/logout.html')
