from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import Form, BooleanField, StringField, validators, DateTimeField, IntegerField
from wtforms.fields.html5 import DateField, IntegerField

ALLOWED_FILE = ('png', 'jpg', 'JPG', 'PNG')


class AuctionsForm(FlaskForm):
    name = StringField('Name', validators=[
                       InputRequired('Country is required')])
    brand = StringField('Mobile Brand', validators=[
                        InputRequired('Mobile Brand Is Required')])

    image = StringField('Image', validators=[
                        InputRequired('Image is Required')])
    model = StringField('Model No.', validators=[
                        InputRequired('Model No. Is Required')])
    condition = StringField('Condition Of The Product', validators=[
                            InputRequired('Condition of the product is Required')])
    description = StringField('Description', validators=[InputRequired('Description is required'),
                                                         Length(min=10, max=300, message='Description is too short or too long')])
    image = FileField('Mobile Images', validators=[
        FileRequired(message='Image can not be empty'),
        FileAllowed(ALLOWED_FILE, message="Only supports valid filetypes")])

    open_bid = IntegerField('Opening Bid', [validators.NumberRange(min=1)])
    #start = DateField('Start Date', id='datepick')
    #end = DateField('End Date', id='datepick')
    submit = SubmitField('Create')


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

    password = PasswordField('Password', validators=[
                             InputRequired('Password Name is required')])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     EqualTo('password', message='Passwords do not match')])

    submit = SubmitField('Register')


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', validators=[InputRequired('Review Is Required'), Length(
        min=5, max=400, message='Comment is too long or too short')])
    submit = SubmitField('Post')
