from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    print(__name__)
    app = Flask(__name__)
    app.secret_key = 'anythingyoulike'
    app.debug = True

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///techdrop.sqlite'
    db.init_app(app)

    UPLOAD_FOLDER = '/static/images'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.debug = True

    bootstrap = Bootstrap(app)

    from . import views
    app.register_blueprint(views.bp)

    from . import Auctions
    app.register_blueprint(Auctions.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
