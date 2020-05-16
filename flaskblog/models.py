from datetime import datetime
from flaskblog import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
	posts = db.relationship('Post', backref='author', lazy=True)

	def get_verification_token(self, expire_time):
		s = Serializer(app.config['SECRET_KEY'], expire_time)
		token = s.dumps({"user_id": self.id}).decode('utf-8')
		return token

	@staticmethod
	def get_user_from_token(token):
		s = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except Exception:
			return None
		user = User.query.get(user_id)
		return user

	def __repr__(self):
		return f'User({self.email}, {self.username}, {self.image_file})'

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
