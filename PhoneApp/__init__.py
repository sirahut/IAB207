from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()


def create_app():
    print(__name__)
    app = Flask(__name__)
    app.secret_key = 'anythingyoulike'
    app.debug = True
    # set the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///techdrop.sqlite'
    # initialize db with flask app
    db.init_app(app)

    # initialize the login manager
    login_manager = LoginManager()

    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # importing views module here to avoid circular references
    # a commonly used practice.

    UPLOAD_FOLDER = '/static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.debug = True

    bootstrap = Bootstrap(app)

    from . import views
    app.register_blueprint(views.bp)

    from . import auctions
    app.register_blueprint(auctions.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import watchlist
    app.register_blueprint(watchlist.bp)

    return app
