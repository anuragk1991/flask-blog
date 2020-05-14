from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[Required(), Length(min=4, max=20)])
	email = StringField('Email', validators=[Required(), Email()])
	password = PasswordField('Password', validators=[Required(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[Required(), Length(min=6), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Email()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Log In')
	remember = BooleanField('Remember Me')