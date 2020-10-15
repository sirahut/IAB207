from flask import Blueprint, session, redirect, url_for, render_template, flash, get_flashed_messages
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User, Auctions
from . import db

bp = Blueprint('auth', __name__, url_prefix='/authentication')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form_instance = LoginForm()
    error = None
    if login_form_instance.validate_on_submit():
        # grab all data from the form
        username = login_form_instance.user_name.data
        pwd = login_form_instance.password.data

        # attempt to grab username from db
        u = User.query.filter_by(name=username).first()
        if u is None:
            error = 'Incorrect username or password'
        # if does exist -> comepare password
        elif not check_password_hash(u.password_hash, pwd):
            error = 'Incorrect password'
        # if password matchs -> login
        if error is None:
            # if error is none -> the username and password are correct
            login_user(u)
            return redirect(url_for('main.index'))
        else:
            flash(error, "danger")

    return render_template('authentication/login.html', form=login_form_instance)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form_instance = RegisterForm()

    if register_form_instance.validate_on_submit():
        # grab all of the data from the form
        username = register_form_instance.user_name.data
        email = register_form_instance.email.data
        pwd = register_form_instance.password.data

        # check if theere is a user with that username already
        # it will return a user object or 'None'
        u = User.query.filter_by(name=username).first()
        if u:
            flash('This username already exists, try different', 'info')
            return redirect(url_for('authentication.login'))

        pwd_hash = generate_password_hash(pwd)
        new_user = User(name=username, emailid=email, password_hash=pwd_hash)

        db.session.add(new_user)
        db.session.commit()
        # if the username is unique we want to create the user and commit to db
        return redirect(url_for('main.index'))

    else:
        return render_template('authentication/register.html', form=register_form_instance)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('authentication/logout.html')
