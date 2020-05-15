from flask import Flask, render_template, url_for, flash, redirect
from forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '879ec7089103eb97c6a166b64e358ea8e8b295fb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f'User({self.email}, {self.username}, {self.image_file})'

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)

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
	form = RegisterForm()
	if form.validate_on_submit():
		flash('Account Created For {}'.format(form.username.data), 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'anuragk1991@gmail.com' and form.password.data == '123456':
			flash('Logged In!', 'success')
			return redirect('home')
		else:
			flash('Invalid email or password', 'danger')
	return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
	app.run(debug=True)