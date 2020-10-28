from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import Form, BooleanField, StringField, validators, DateTimeField, IntegerField, FloatField
from wtforms.fields.html5 import DateField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .models import Brand, Condition

ALLOWED_FILE = ('png', 'jpg', 'JPG', 'PNG')


def condition_query():
    return Condition.query


def brand_query():
    return Brand.query


class AuctionsForm(FlaskForm):
    title = StringField('Title', validators=[
        InputRequired('Title is required')])
    brand = QuerySelectField(
        query_factory=brand_query, allow_blank=False, get_label='brand')
    # brand = StringField('Brand', validators=[
    #                     InputRequired('Brand Is Required')])

    model = StringField('Model', validators=[
                        InputRequired('Model is required')])
    condition = QuerySelectField(
        query_factory=condition_query, allow_blank=False, get_label='condition')

    description = StringField('Description', validators=[InputRequired('Description is required'),
                                                         Length(min=10, max=300, message='Description is too short or too long')])
    image = FileField('Mobile Images', validators=[
        FileRequired(message='Please add an image'),
        FileAllowed(ALLOWED_FILE, message="Only supports valid filetypes")])

    open_bid = FloatField('Opening Bid', [validators.NumberRange(min=100)])
    start = DateField('Start Date', id='datepick')
    end = DateField('End Date', id='datepick')
    submit = SubmitField('Create')

    def validate_end(self, field):
        if field.data <= self.start.data:
            raise ValidationError(
                "Error!: Please enter later date than start date.")


class LoginForm(FlaskForm):
    user_name = StringField('User Name', validators=[
                            InputRequired('User Name is required')])
    password = PasswordField('Password', validators=[
                             InputRequired('Password Name is required')])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    user_name = StringField('User Name', validators=[
                            InputRequired('User Name is required')])
    email = StringField('Email', validators=[InputRequired(
        'Email is required'), Email('Email is not valid')])
    contact_number = StringField('Contact Number')
    address = StringField('Address')
    password = PasswordField('Password', validators=[
                             InputRequired('Password Name is required')])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     EqualTo('password', message='Passwords do not match')])

    submit = SubmitField('Register')


class ReviewForm(FlaskForm):
    review = TextAreaField('', validators=[InputRequired('Review Is Required'), Length(
        min=5, max=400, message='Comment is too long or too short')])
    submit = SubmitField('Write Review')


class WatchListForm(FlaskForm):
    add = SubmitField('Add to Watchlist')


class PlaceBidForm(FlaskForm):
    # the bid amount has to be more than current bid
    # draw from Bid table
    # grab the highest bid
    # SELECT * FROM BID WHERE auction_id = <id>
    #min = highest_bid+1
    bid_amount = FloatField('$', [validators.NumberRange(min=1)])
    place = SubmitField('Place Bids')
