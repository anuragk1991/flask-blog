import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegisterForm, LoginForm, AccountUpdateForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = [
	{
		'author': 'Anurag',	
		'title': 'First Post',	
		'date_posted': 'April 24, 2020',
		'content': 'Details of the post'	
	},
	{
		'author': 'Anurag',	
		'title': 'Second Post',	
		'date_posted': 'April 24, 2020',
		'content': 'Details of the second post'	
	}
]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
	return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if(current_user.is_authenticated):
		return redirect(url_for('home'))
	form = RegisterForm()
	if form.validate_on_submit():
		hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
		db.session.add(user)
		db.session.commit()
		flash('Account Created For {}. You can Login now'.format(form.username.data), 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if(current_user.is_authenticated):
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()

		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next = request.args.get('next')
			return redirect(next) if next else redirect(url_for('home'))
		else:
			flash('Invalid username or password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

def savePictureFile(picture):
	random_fn = secrets.token_hex(8)
	_, file_ext = os.path.splitext(picture.filename)
	filename = random_fn+file_ext
	image = os.path.join(app.root_path, 'static/profile_pics', filename)

	size = (200, 200)
	i = Image.open(picture)
	i.thumbnail(size)
	i.save(image)
	return filename

@app.route('/account', methods=['GET', 'POST'])
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
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email

	return render_template('account.html', title='Account', image_file=image_file, form=form)