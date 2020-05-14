from flask import Flask, render_template, url_for
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '879ec7089103eb97c6a166b64e358ea8e8b295fb'

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
	return render_template('register.html', form=form)

@app.route('/login')
def login():
	return render_template('login.html')

if __name__ == '__main__':
	app.run(debug=True)