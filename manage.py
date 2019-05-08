from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown

app = Flask(__name__)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
pagedown = PageDown()
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hackersir.db'


db.init_app(app)
pagedown.init_app(app)
login_manager.init_app(app)

"""
Models
"""
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import hashlib
from markdown import markdown

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    realname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password是不可讀取的!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        if value is None or (value is ''):
            target.body_html = ''
        else:
            target.body_html = markdown(value)

db.event.listen(Post.body, 'set', Post.on_body_changed)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

"""
Views
"""
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from forms import PostForm, CommentForm, LoginForm, RegistForm

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/posts/<int:id>', methods=['GET', 'POST'])
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

@app.route('/edit', methods=['GET', 'POST'])
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('post', id=post.id))
    
    return render_template('edit.html', form=form, post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.rememberme.data)
            flash('登入成功', 'success')
            return redirect(url_for('index'))
        flash('錯誤的帳號或密碼!', 'error')
    return render_template('auth/login.html', form=form)

@app.route('/regist', methods=['GET', 'POST'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email已被註冊', 'error')
        else:
            if User.query.filter_by(username=form.username.data).first():
                flash('使用者已被註冊', 'error')
            else:
                user = User(email=form.email.data,
                            username=form.username.data, 
                            password=form.password.data,
                            realname=form.realname.data)
                db.session.add(user)
                db.session.commit()
                flash('註冊成功!', 'success')
                return redirect(url_for('login'))
    return render_template('auth/regist.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('成功登出!', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
