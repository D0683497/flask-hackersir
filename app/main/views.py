from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import main
from .forms import PostForm, CommentForm
from ..models import Post, Comment
from .. import db

@main.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@main.route('/posts/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    #詳情頁面
    post = Post.query.get_or_404(id)

    #評論
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()

    return render_template('post.html', title=post.title, form=form, post=post)

@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    post = None
    form = PostForm()

    if id == 0:
        post = Post(author=current_user)
    else:
        #修改
        post = Post.query.get_or_404(id)
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post', id=post.id))
    
    return render_template('edit.html', form=form, post=post)