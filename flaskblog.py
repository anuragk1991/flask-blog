from flask import Flask, render_template

app = Flask(__name__)

posts = [
	{
		'author': 'Anurag',	
		'title': 'First Post',	
		'date': 'April 24, 2020',
		'content': 'Details of the post'	
	},
	{
		'author': 'Anurag',	
		'title': 'Second Post',	
		'date': 'April 24, 2020',
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

if __name__ == '__main__':
	app.run(debug=True)