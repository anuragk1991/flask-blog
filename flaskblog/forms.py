from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Required, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

class RegisterForm(FlaskForm):
	username = StringField('Username', validators=[Required(), Length(min=4, max=20)])
	email = StringField('Email', validators=[Required(), Email()])
	password = PasswordField('Password', validators=[Required(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[Required(), Length(min=6), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('username already taken, choose another one')
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('email already registered')


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	submit = SubmitField('Log In')
	remember = BooleanField('Remember Me')

class AccountUpdateForm(FlaskForm):
	username = StringField('Username', validators=[Required(), Length(min=4, max=20)])
	email = StringField('Email', validators=[Required(), Email()])
	image_file = FileField('Upload Your Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if current_user.username != username.data:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('username already taken, choose another one')
	def validate_email(self, email):
		if current_user.email != email.data:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('email already registered')

class PostForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	content = TextAreaField('Content', validators=[Required()])
	submit = SubmitField('Add Post')