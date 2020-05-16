from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required

class PostForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	content = TextAreaField('Content', validators=[Required()])
	submit = SubmitField('Add Post')

