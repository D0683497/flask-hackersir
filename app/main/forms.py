from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_pagedown.fields import PageDownField

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
