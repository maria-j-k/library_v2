from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from flaskr.user_models import User

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already registered.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PasswordChangeForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired()])
    password2 = PasswordField('Confirm new password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change password')

class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Confirm')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Confirm')

