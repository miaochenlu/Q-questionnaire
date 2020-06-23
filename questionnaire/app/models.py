
from . import db
from . import login_manager
from datetime import datetime
from flask import current_app
from markdown import markdown
import bleach
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy="dynamic")
    def __repr__(self):
        return '<Role %r>' %self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                    Permission.COMMENT |
                    Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                        Permission.COMMENT |
                        Permission.WRITE_ARTICLES |
                        Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            # 设置了权限
            role.permissions = roles[r][0]
            # 设置了default
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True)

    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    questionnaires = db.relationship('questionnaire', backref="author", lazy="dynamic")

    posts = db.relationship('Post', backref="author", lazy="dynamic")
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
    
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(), 
                    username=forgery_py.internet.user_name(True), 
                    password=forgery_py.lorem_ipsum.word(), 
                    confirmed=True, name=forgery_py.name.full_name(), 
                    location=forgery_py.address.city(), 
                    about_me=forgery_py.lorem_ipsum.sentence(), 
                    member_since=forgery_py.date.date(True)) 
            db.session.add(u) 
            try:
                db.session.commit() 
            except IntegrityError:
                db.session.rollback()

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

    def is_anonymous(self):
        return True

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)

    @staticmethod
    def on_change_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p'] 
        target.body_html = bleach.linkify(bleach.clean(
                        markdown(value, output_format='html'),
                        tags=allowed_tags, strip=True))
    

class questionnaire(db.Model):
    __tablename__ = "questionnaires"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    description = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    questions = db.relationship('Question', backref="questionnaire", lazy="dynamic")
    releases = db.relationship('questionnaireRelease', backref="questionnaire", lazy="dynamic")

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    description = db.Column(db.String(64))
    must_do = db.Column(db.Boolean)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaires.id'))
    options = db.relationship('Option', backref="question", lazy="dynamic")
    score = db.relationship('Score', backref="question", uselist=False)
    number_control = db.relationship('NumberControl', backref="question", uselist=False)
    row_control = db.relationship('RowControl', backref="question", uselist=False)
    questionanswers = db.relationship("QuestionAnswer", backref='question', lazy='dynamic')
    relation = db.relationship('Relation', backref="question", uselist=False)

class Option(db.Model):
    __tablename__ = "options"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    

class RowControl(db.Model):
    __tablename__ = "rowcontrols"
    id = db.Column(db.Integer, primary_key=True)
    row_type = db.Column(db.Boolean) # 0 for one row 1 for multiple row
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

class NumberControl(db.Model):
    __tablename__ = "numbercontrols"
    id = db.Column(db.Integer, primary_key=True)
    number_type = db.Column(db.Boolean) # 0 int 1 for decimal
    min = db.Column(db.String(20))
    max = db.Column(db.String(20))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    left_text = db.Column(db.String(64))
    right_text = db.Column(db.String(64))
    radio_num = db.Column(db.Integer)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))


class questionnaireRelease(db.Model):
    __tablename__ = "questionnairereleases"
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(), default=datetime.utcnow)
    finish_time = db.Column(db.DateTime())
    mode = db.Column(db.Integer)
    times = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaires.id'))

    def valid(self):
        current_time = datetime.utcnow()
        if status and current_time > start_time and current_time < finish_time:
            return True
        return False

class questionnaireAnswer(db.Model):
    __tablename__ = "questionnaireanswers"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    ip = db.Column(db.String(64))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaires.id'))
    questionanswers = db.relationship("QuestionAnswer", backref='questionnaireanswer', lazy='dynamic')

class QuestionAnswer(db.Model):
    __tablename__ = "questionanswers"
    id = db.Column(db.Integer, primary_key=True)
    questionnaire_answer_id = db.Column(db.Integer, db.ForeignKey('questionnaireanswers.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    answer = db.Column(db.Text)
    

class Relation(db.Model):
    __tablename__ = "relations"
    id = db.Column(db.Integer, primary_key=True)
    relate_ques = db.Column(db.Integer) 
    relate_option = db.Column(db.Integer) 
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))

login_manager.anonymous_user = AnonymousUser