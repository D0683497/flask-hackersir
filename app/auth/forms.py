from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms import ValidationError
from ..models import User

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
    def validata_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email已被註冊')

    def validata_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('使用者已被註冊')
    email = StringField('Email address',
                        validators=[DataRequired(
                            message='不能為空!'), Email(message='格式錯誤!'), Length(1, 64, message="長度需介於1到64之間"), validata_email],
                        render_kw={'class': 'form-control',
                                   'placeholder': 'Email address'}
                        )
    realname = StringField('Real name',
                           render_kw={'class': 'form-control',
                                      'placeholder': 'Real name'}
                           )
    username = StringField(
        'Username',
        validators=[DataRequired(message='不能為空!'), validata_username],
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
