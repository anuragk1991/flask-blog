import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, current_app as app
from flaskblog import db, bcrypt
from flaskblog.users.forms import RegisterForm, LoginForm, AccountUpdateForm, ForgotPasswordForm, ResetPasswordForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from flaskblog.users.utils import send_reset_mail, savePictureFile

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
	if(current_user.is_authenticated):
		return redirect(url_for('main.home'))
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
		db.session.add(user)
		db.session.commit()
		flash('Account Created For {}. You can Login now'.format(form.username.data), 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next = request.args.get('next')
			return redirect(next) if next else redirect(url_for('main.home'))
		else:
			flash('Invalid username or password', 'danger')
	return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
	form = AccountUpdateForm()

	if form.validate_on_submit():
		if form.image_file.data:
			if current_user.image_file != 'default.jpg':
				current_file_path = os.path.join(app.root_path, 'static/profile_pics', current_user.image_file)
			else:
				current_file_path = None
			image_file = savePictureFile(form.image_file.data)
			current_user.image_file = image_file
			if current_file_path:
				os.remove(current_file_path)
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('You account info updated successfully', 'success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>/posts')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query\
			.filter_by(username=username)\
			.first_or_404()

	posts = Post.query\
				.filter_by(author=user)\
				.order_by(Post.date_posted.desc())\
				.paginate(page=page, per_page=5)

	return render_template('user_posts.html', posts=posts, user=user)

@users.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = ForgotPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		token = user.get_verification_token(60)
		send_reset_mail(user, token)
		flash('Password reset link has ent to you email!', 'success')
		return redirect(url_for('users.forgot_password'))


	return render_template('forgot_password.html', form=form, title='Forgot Password')

@users.route('/reset_password/<string:token>', methods=['GET', 'POST'])
def reset_password(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = ResetPasswordForm()
	if form.validate_on_submit():
		user = User.get_user_from_token(token)
		if user is None:
			flash('Password reset link has been expired.', 'warning')
			return redirect(url_for('users.forgot_password'))
		else:
			user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			db.session.commit()
			flash('Password Updated Successfully', 'success')
			return redirect(url_for('users.login'))
	return render_template('reset_password.html', form=form, title="Reset Password")
