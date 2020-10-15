from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = ['png', 'jpg', 'JPG', 'PNG']


class AuctionsForm(FlaskForm):
    name = StringField('Country', validators=[
                       InputRequired('Country is required')])
    image = StringField('Image', validators=[
                        InputRequired('Image is required')])
    # brand
    # model
    # condition
    description = StringField('Description', validators=[InputRequired('Description is required'),
                                                         Length(min=10, max=300, message='Description is too short or too long')])
    image = FileField('Destination Image', validators=[
        FileRequired(message='Image can not be empty'),
        FileAllowed(ALLOWED_FILE, message="Only supports valid filetypes")])

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
