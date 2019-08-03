from datetime import datetime
from flask import render_template, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from app import db
from app.main import bp
from app.models import Post
from app.main.forms import AddPostForm

@bp.route('/')
@bp.route('/index')
def index():
    # Sort pages by date
    # sorted_posts = sorted(posts, reverse=True, 
    #     key=lambda page: page.meta['date'])
    return render_template('index.html', title="Home")

# @bp.route('/updateposts')
# def update_posts():
#     posts = [page for page in listdir(os.path.join(basedir, 'pages'))]
#     return render_template('post.html', post=posts[0])

@bp.route('/blog')
def blog():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('blog.html', posts=posts, title="blog")

@bp.route('/about')
def about():
    return render_template('about.html', title="about me")

@bp.route('/post/<post_id>')
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post, title=post.title)

@bp.route('/delete/<post_id>')
def delete_post(post_id):
	if current_user.role != "ADMIN":
		return render_template('errors/404.html')
	post = Post.query.filter_by(id=post_id).first_or_404()
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted!')
	return redirect(url_for('main.blog'))

@bp.route('/addpost', methods=['GET', 'POST'])
@login_required
def add_post():
    if current_user.role != "ADMIN":
        return render_template('errors/404.html')
    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data,
                    body=form.body.data, timestamp=datetime.now())
        db.session.add(post)
        db.session.commit()
        flash('Your post has been added!')
        return redirect(url_for('main.blog'))
    return render_template('forms/addpost.html', form=form)
# @bp.route('/<path:path>/')
# def page(path):
#     # `path` is the filename of a page, without the file extension
#     # e.g. "first-post"
#     page = pages.get_or_404(path)
#     return render_template('page.html', page=page)