from flask import render_template, flash, url_for, redirect
from .forms import LoginForm, RegistForm
from flask_login import login_user, logout_user, current_user, login_required
from . import auth
from .. import db
from ..models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.rememberme.data)
            flash('登入成功', 'success')
            return redirect(url_for('main.index'))
        flash('錯誤的帳號或密碼!', 'error')
    return render_template('auth/login.html', form=form)

@auth.route('/regist', methods=['GET', 'POST'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, 
                    password=form.password.data,
                    realname=form.realname.data)
        db.session.add(user)
        db.session.commit()
        flash('註冊成功!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/regist.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('成功登出!', 'success')
    return redirect(url_for('main.index'))