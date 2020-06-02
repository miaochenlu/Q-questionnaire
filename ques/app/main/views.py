from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, current_app
from flask import abort
from flask_login import current_user, login_required
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm, CreateQuestionaireForm
from .. import db
from ..models import User, Role, Post, Permission, Questionaire, Question, Option
from ..decorators import admin_required

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if  form.validate_on_submit() and current_user.can(Permission.WRITE_ARTICLES):
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        # db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items

    return render_template('index.html', current_time=datetime.utcnow(), form=form, posts=posts, pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/questionaire/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateQuestionaireForm()
    if form.validate_on_submit():
        q = Questionaire(title=form.title.data, 
                        description=form.description.data,
                        author=current_user._get_current_object()
                        )
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('main.create_question', id=q.id))
    return render_template('create.html', form=form)

@main.route('/questionaire/<int:id>/create_question', methods=['GET', 'POST'])
@login_required
def create_question(id):
    def get_questions():
        # questions = []
        question_count = 0
        questionaire = Questionaire.query.get_or_404(id)
        while True:
            question_form = 'ques_' + str(question_count)
            if question_form + '.type' in request.form:
                # question = {
                #     "type" : request.form[question_form + '.type'],
                #     "description": request.form[question_form + '.description'],
                #     "options" : get_options(question_form)

                # }
                # type = db.Column(db.Integer)
                # description = db.Column(db.String(64))
                # must_do = db.Column(db.Boolean)
                # questionaire_id = db.Column(db.Integer, db.ForeignKey('questionaires.id'))
                # options = db.relationship('Option', backref="question", lazy="dynamic")
                add_db_question = Question(
                    type = request.form[question_form + '.type'],
                    description = request.form[question_form + '.description'],
                    must_do = True if request.form[question_form + '.must_do'] == "on" else False,
                    questionaire = questionaire
                )
                
                db.session.add(add_db_question)
                db.session.commit()
                get_options(question_form, add_db_question.id)
                question_count += 1
            else:
                break

    def get_options(question_form, question_id):
        option_count = 0
        question = Question.query.get_or_404(question_id)
        while True:
            option = question_form + '.option_' + str(option_count)
            if option in request.form:
                db_add_option = Option (
                    description = request.form[option],
                    question = question
                )
                db.session.add(db_add_option)
                db.session.commit()
                option_count += 1
            else:
                break

    questionaire = Questionaire.query.get_or_404(id)
    if current_user != questionaire.author:
        abort(403)
    
    if request.method == 'POST':
        questions = get_questions()
        return redirect(url_for('main.questionaire', id=questionaire.id))

    return render_template('create_question.html')


@main.route('/questionaire/<int:id>')
@login_required
def questionaire(id):
    questionaire = Questionaire.query.get_or_404(id)
    if current_user != questionaire.author:
        abort(403)
    
    questionaire_name = questionaire.title
    questionaire_description = questionaire.description
    questions = questionaire.questions.all()
    # options = 
    renderQuestions = []
    for question in questions:
        q = {
                    "question" : question,
                    "options" : question.options.all()
        }
        renderQuestions.append(q)
    length = len(renderQuestions)

    return render_template('questionaire.html', questionaire_name=questionaire_name,
                            questionaire_description=questionaire_description, renderQuestions=renderQuestions, length=length)