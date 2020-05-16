from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskblog import db
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

@posts.route("/post/add", methods=['GET', 'POST'])
@login_required
def add_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
		db.session.add(post)
		db.session.commit()
		flash('Your posted added successfully', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', title='Add Post', form=form, legend='Add Post')

@posts.route('/post/<int:post_id>')
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	form = PostForm()
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post updated successfully!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content

	return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)

	db.session.delete(post)
	db.session.commit()
	flash('Post deleted successfully', 'success')

	return redirect(url_for('main.home'))
