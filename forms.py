from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_pagedown.fields import PageDownField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms import ValidationError

class PostForm(FlaskForm):
    title = StringField('標題', 
                        validators=[DataRequired()],
                        render_kw={'class': 'form-control', 'placeholder': '標題'}
                        )
    body = PageDownField("分享您的文章", 
                        validators=[DataRequired(message='不能為空!')],
                        render_kw={'class': 'form-control', 'placeholder': '分享您的文章'}
                        )
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-lg btn-primary btn-block'})

class CommentForm(FlaskForm):
    body = PageDownField('寫下您的評論', 
                        validators=[DataRequired()],
                        render_kw={'class': 'form-control', 'placeholder': '寫下您的評論'}
                        )
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-lg btn-primary btn-block'})

class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(message='不能為空!')],
        render_kw={'class': 'form-control', 'placeholder': 'Username'}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='不能為空!')],
        render_kw={'class': 'form-control', 'placeholder': 'Password'}
    )
    rememberme = BooleanField(
        'Remember me'
    )
    login = SubmitField(
        '登入',
        render_kw={'class': 'btn btn-lg btn-primary btn-block'}
    )


class RegistForm(FlaskForm):
    email = StringField('Email address',
                        validators=[DataRequired(
                            message='不能為空!'), Email(message='格式錯誤!'), Length(1, 64, message="長度需介於1到64之間")],
                        render_kw={'class': 'form-control',
                                   'placeholder': 'Email address'}
                        )
    realname = StringField('Real name',
                           render_kw={'class': 'form-control',
                                      'placeholder': 'Real name'}
                           )
    username = StringField(
        'Username',
        validators=[DataRequired(message='不能為空!')],
        render_kw={'class': 'form-control', 'placeholder': 'Username'}
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='不能為空!'),
                    EqualTo('confirmPassword', message='您輸入的密碼不相同!')],
        render_kw={'class': 'form-control', 'placeholder': 'Password'}
    )
    confirmPassword = PasswordField(
        'Confirm Password',
        validators=[DataRequired(message='不能為空!')],
        render_kw={'class': 'form-control', 'placeholder': 'Confirm Password'}
    )
    regist = SubmitField(
        '註冊',
        render_kw={'class': 'btn btn-lg btn-primary btn-block'}
    )
