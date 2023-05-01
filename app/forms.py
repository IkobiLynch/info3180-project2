# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms import StringField, TextAreaField, EmailField, PasswordField
from wtforms.validators import InputRequired, DataRequired, Length

class UserForm (FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=80)])
    firstname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=80)])
    lastname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=80)])
    email = EmailField('Email', validators=[InputRequired(), Length(min=2, max=80)])
    location = StringField('Location', validators=[InputRequired(), Length(min=2, max=80)])
    biography = TextAreaField('Biography', validators=[DataRequired(), Length(min=2, max=80)])
    profile_photo = FileField('Profile Photo', validators=[FileRequired(), FileSize(max_size=4000000), FileAllowed(["jpg", "png"], message="Image Files Only!")])

    
class LoginForm (FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=2, max=80)])
    