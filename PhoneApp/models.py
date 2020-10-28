from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # backref
    auctions = db.relationship('Auctions', backref='user')
    reviews = db.relationship('Review', backref='user')
    bids = db.relationship('Bid', backref='user')
    watchlists = db.relationship('Watchlist', backref='user')


class Auctions(db.Model):
    __tablename__ = 'auctions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    # brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    # condition = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    open_bid = db.Column(db.Float(), nullable=False)
    start = db.Column(db.DateTime, default=datetime.now())
    # will change this later
    end = db.Column(db.DateTime)
    # auction status
    status = db.Column(db.String(80), default='Active')
    # FK
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'))
    # backref
    reviews = db.relationship('Review', backref='auction')
    bids = db.relationship('Bid', backref='auction')
    watchlists = db.relationship('Watchlist', backref='auction')

    def __repr__(self):
        return "<Name: {}>".format(self.name)


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    # FK
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'))

    def __repr__(self):
        return "<Name: {}>".format(self.text)


class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    bid_amount = db.Column(db.Float, nullable=False)
    bid_date = db.Column(db.DateTime, default=datetime.now())
    # FK
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'))

    def __repr__(self):
        return "<Name: {}>".format(self.text)


class Watchlist(db.Model):
    __tablename__ = 'watchlists'
    id = db.Column(db.Integer, primary_key=True)
    added_date = db.Column(db.DateTime, default=datetime.now())
    # FK
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'))

    def __repr__(self):
        return "<Name: {}>".format(self.text)


class Brand(db.Model):
    __tablename__ = 'brands'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80))

    auctions = db.relationship('Auctions', backref='brand')

    def __repr__(self):
        return '[Brand {}]'.format(self.name)


class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return "<Review: {}>".format(self.text)


class Condition(db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(50))

    auctions = db.relationship('Auctions', backref='condition')

    def __repr__(self):
        return '[Condition {}]'.format(self.name)
