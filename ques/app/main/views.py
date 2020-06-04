from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, current_app
from flask import abort
from flask_login import current_user, login_required
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm, CreateQuestionaireForm
from .. import db
from ..models import User, Role, Post, Permission, Questionaire, Question, Option, QuestionaireRelease
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
    pagination = Questionaire.query.order_by(Questionaire.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False
    )
    questionaires = pagination.items

    return render_template('index.html', current_time=datetime.utcnow(), questionaires=questionaires, pagination=pagination)

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





###########################questionaire##############################

@main.route('/questionaire/create', methods=['GET', 'POST'])
@login_required
def create_questionaire():
    form = CreateQuestionaireForm()
    if form.validate_on_submit():
        q = Questionaire(title=form.title.data, 
                        description=form.description.data,
                        author=current_user._get_current_object()
                        )
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('main.create_question', id=q.id))
    return render_template('create_questionaire.html', form=form)


def get_question_dict(questionaire):
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
    return renderQuestions

def question_delete(questionaire):
    if current_user != questionaire.author:
        abort(403)
    
    questionaire_name = questionaire.title
    questionaire_description = questionaire.description
    questions = questionaire.questions.all()
    # options = 
    renderQuestions = []
    for question in questions:
        options = question.options.all()
        for option in options:
            db.session.delete(option)
        db.session.delete(question)
    db.session.commit()

@main.route('/questionaire/<int:id>/create_question', methods=['GET', 'POST'])
@login_required
def create_question(id):
    def get_questions():
        question_count = 0
        questionaire = Questionaire.query.get_or_404(id)
        while True:
            question_form = 'ques_' + str(question_count)
            if question_form + '.type' in request.form:
                add_db_question = Question(
                    type = request.form[question_form + '.type'],
                    description = request.form[question_form + '.description'],
                    must_do = True if request.form[question_form + '.must_do'] == "1" else False,
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
    
    renderQuestions = get_question_dict(questionaire)
    length = len(renderQuestions)
    if request.method == 'POST':
        questionaire.title = request.form["questionaire_title"].replace("'", "\'").replace('"', '\"')
        questionaire.description = request.form["questionaire_description"].replace("'", "\'").replace('"', '\"')
        db.session.add(questionaire)
        db.session.commit()
        question_delete(questionaire)
        questions = get_questions()
        return redirect(url_for('main.questionaire', id=questionaire.id))

    return render_template('create_question.html', questionaire=questionaire, renderQuestions=renderQuestions, length=length)



@main.route('/questionaire/<int:id>')
@login_required
def questionaire(id):
    questionaire = Questionaire.query.get_or_404(id)
    renderQuestions = get_question_dict(questionaire)
    length = len(renderQuestions)

    return render_template('questionaire.html', questionaire=questionaire, 
                            renderQuestions=renderQuestions, length=length)


@main.route('/questionaire/<int:id>/release', methods=["GET", "POST"])
@login_required
def release_questionaire(id):
    questionaire = Questionaire.query.get_or_404(id)
    release = QuestionaireRelease.query.filter_by(questionaire_id=id).first()
    if(release):
        flash("你的问卷已经发布过了")
        return redirect(url_for('main.questionaire', id=id))
    if current_user != questionaire.author:
        abort(403)
    if request.method == "POST":
        times = 0
        mode = 0
        if request.form["mode"] == "0":
            mode = 0
        elif request.form["mode"] == "1" :
            mode = 1
            times = request.form["times"]
        elif request.form["mode"] == "2":
            mode = 2
            times = request.form["times"]
        
        start_obj = datetime.strptime(request.form["start_time"], '%Y-%m-%dT%H:%M')
        finish_obj = datetime.strptime(request.form["finish_time"], '%Y-%m-%dT%H:%M')
        release = QuestionaireRelease (
            start_time = start_obj,
            finish_time = finish_obj,
            mode = mode,
            times = times,
            status = 1,
            questionaire = questionaire,
        )
        flash("你的问卷发布成功")
        return redirect(url_for('main.questionaire', id=id))
    return render_template('questionaire_release.html')

@main.route('/questionaire/<int:id>/answer', methods=["GET", "POST"])
def answer_questionaire(id):
    questionaire = Questionaire.query.get_or_404(id)
    renderQuestions = get_question_dict(questionaire)
    length = len(renderQuestions)

    return render_template('ans_questionaire.html', questionaire=questionaire, 
                            renderQuestions=renderQuestions, length=length)