from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange


class RegisterForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    old = IntegerField('Old', validators=[DataRequired(), NumberRange(min=18, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    city = StringField('City')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    # remember = BooleanField('Remember me')
    submit = SubmitField('Register me')

