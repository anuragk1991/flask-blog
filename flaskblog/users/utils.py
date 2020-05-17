import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message

def send_reset_mail(user, token):
	msg = Message('Reset Password Link', sender='flaskblog.py@gmail.com', recipients=[user.email])
	msg.body = url_for('users.reset_password', token=token, _external=True)

	mail.send(msg)

def savePictureFile(picture):
	random_fn = secrets.token_hex(8)
	_, file_ext = os.path.splitext(picture.filename)
	filename = random_fn+file_ext
	image = os.path.join(current_app.root_path, 'static/profile_pics', filename)

	size = (200, 200)
	i = Image.open(picture)
	i.thumbnail(size)
	i.save(image)
	return filename
