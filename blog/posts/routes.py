from flask import flash, redirect, render_template, request, url_for, abort, Blueprint
from flask_login import current_user, login_required
from blog import db
from blog.posts.forms import PostForm
from blog.models import Post, Comments
from blog.users.utils import role_required

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@role_required(['Admin', 'Writer'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
              
        post = Post(author = current_user, title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()

        flash('The post has been created','success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments

    return render_template('post.html', title=post.title, post=post, comments=comments)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@role_required(['Admin', 'Writer'])
def post_update(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user and 'Admin' not in current_user.roles_names:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('The post has been updated.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@role_required(['Admin', 'Writer'])
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user and 'Admin' not in current_user.roles_names:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('The post has been deleted.', 'success')

    return redirect(url_for('main.home'))