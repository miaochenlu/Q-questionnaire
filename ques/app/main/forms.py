from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, DateTimeField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

from ..models import User, Role

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers, dots or underscores')])

    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])

    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user
    
    def validate_email(self, email):
        if email.data != self.user.email and \
            User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')
    
    def validate_username(self, username):
        if email.data != self.user.username and \
            User.query.filter_by(username=username.data).first():
            raise ValidationError('Username already registered.')

class PostForm(FlaskForm):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class CreateQuestionaireForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 20)])
    description = TextAreaField('Description')
    submit = SubmitField('Create')

class QuestionaireReleaseForm(FlaskForm):
    start_time = DateTimeField("开始时间",
                          format="%Y-%m-%d %H:%M:%S", 
                          default=datetime.now(),
                          validators=[DataRequired()])
    end_time = DateTimeField("结束时间",
                          format="%Y-%m-%d %H:%M:%S", 
                          default=datetime.now(),
                          validators=[DataRequired()])
    mode = RadioField("填写模式", choices=[(0, "仅注册用户可填写"), (1, "无需注册, 可填写限定次"), (2, "无需注册, 每天可填写限定次")])
    times = IntegerField('填写次数', validators=[DataRequired()])
    submit = SubmitField('发布')
