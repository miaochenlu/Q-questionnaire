from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, current_app, g
from flask import abort
from flask import Markup
from flask_login import current_user, login_required
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm, CreateQuestionaireForm
from .. import db
from ..models import User, Role, Post, Permission, Questionaire, Question, Option, Score, RowControl, NumberControl, Relation, QuestionaireRelease, QuestionaireAnswer, QuestionAnswer
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
    if current_user.is_anonymous() == False:
        pagination = Questionaire.query.order_by(Questionaire.timestamp.desc()).paginate(
            page, per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
            error_out=False
        )
        questionaires = pagination.items
        return render_template('index.html', current_time=datetime.utcnow(), questionaires=questionaires, pagination=pagination)
    return render_template('anonymous.html')

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
def get_question_dict(questionaire):
    questionaire_name = questionaire.title
    questionaire_description = questionaire.description
    questions = questionaire.questions.all()
    # options = 
    renderQuestions = []
    for question in questions:
        q = {
                    "question" : question,
                    "options" : question.options.all(),
        }
        renderQuestions.append(q)
    return renderQuestions

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
        if question.score is not None:
            db.session.delete(question.score)
        if question.number_control is not None:
            db.session.delete(question.number_control)
        if question.row_control is not None:
            db.session.delete(question.row_control)
        if question.relation is not None:
            db.session.delete(question.relation)
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
                get_set_score(question_form, add_db_question.id)
                get_set_number(question_form, add_db_question.id)
                get_set_row(question_form, add_db_question.id)
                get_set_relation(question_form, add_db_question.id)
                db.session.commit()
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
    
    def get_set_score(question_form, question_id):
        question = Question.query.get_or_404(question_id)
        lefttext = question_form + '.lefttext'
        righttext = question_form + '.righttext'
        num = question_form + '.number'
        if lefttext in request.form and righttext in request.form and num in request.form:
            score = Score(
                left_text = request.form[lefttext],
                right_text = request.form[righttext],
                radio_num = request.form[num],
                question = question
            )
            db.session.add(score)
            db.session.commit()

    def get_set_number(question_form, question_id):
        question = Question.query.get_or_404(question_id)
        minnumber = question_form + '.minnumber'
        maxnumber = question_form + '.maxnumber'
        number_type = question_form + '.intordeci'
        if minnumber in request.form and maxnumber in request.form and number_type in request.form:
            num_ctr = NumberControl(
                min = request.form[minnumber] if request.form[minnumber] < request.form[maxnumber] else request.form[maxnumber],
                max = request.form[minnumber] if request.form[minnumber] > request.form[maxnumber] else request.form[maxnumber],
                number_type = False if request.form[number_type] == "0" else True,
                question = question
            )
            db.session.add(num_ctr)
            db.session.commit()
    
    def get_set_row(question_form, question_id):
        question = Question.query.get_or_404(question_id)
        row_type = question_form + '.row'
        if row_type in request.form:
            row_ctr = RowControl(
                row_type = False if request.form[row_type] == "0" else True,
                question = question
            )
            db.session.add(row_ctr)
            db.session.commit()

    def get_set_relation(question_form, question_id):
        question = Question.query.get_or_404(question_id)
        relate_ques_number =  question_form + ".ques_select"
        relate_option_number = question_form + ".option_select"
        if relate_ques_number in request.form and relate_option_number in request.form:
            rela = Relation (
                relate_ques = request.form[relate_ques_number],
                relate_option = request.form[relate_option_number],
                question_id = question.id,
            )
            db.session.add(rela)
            db.session.commit()

    questionaire = Questionaire.query.get_or_404(id)
    if current_user != questionaire.author:
        abort(403)
    releases = QuestionaireRelease.query.filter_by(questionaire_id=id).all()
    if len(releases) > 0:
        flash(Markup('对不起，该问卷已经发布, 不能修改。请<a href=\"/questionaire/create\">新建问卷</a>'))
        return render_template('warning.html')

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



@main.route('/questionaire/<int:id>/preview')
@login_required
def questionaire(id):
    questionaire = Questionaire.query.get_or_404(id)
    if current_user != questionaire.author:
        abort(403)
    renderQuestions = get_question_dict(questionaire)
    length = len(renderQuestions)

    return render_template('questionaire.html', questionaire=questionaire, 
                            renderQuestions=renderQuestions, length=length)


@main.route('/questionaire/<int:id>/release', methods=["GET", "POST"])
@login_required
def release_questionaire(id):
    questionaire = Questionaire.query.get_or_404(id)
    # release = QuestionaireRelease.query.filter_by(questionaire_id=id).first()
    # if(release):
    #     flash("你的问卷已经发布过了")
    #     return redirect(url_for('main.questionaire', id=id))
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
    releases = QuestionaireRelease.query.filter_by(questionaire_id=id).all()
    if len(releases) == 0:
        flash("对不起，该问卷尚未发布")
        return render_template("warning.html")

    release = releases[-1]
    renderQuestions = get_question_dict(questionaire)
    length = len(renderQuestions)

    if release.mode == 0 and current_user.is_anonymous() == True:
        flash("对不起，您需要登陆才能回答该问卷")
        return render_template("warning.html")
    if release.mode == 1:
        ip = request.remote_addr
        ans_count = QuestionaireAnswer.query.filter_by(questionaire_id=id).filter_by(ip = ip).count()
        if ans_count >= release.times:
            flash("对不起，您的总回答次数已达到上限")
            return render_template("warning.html")
    if release.mode == 2:
        ip = request.remote_addr
        current_time = datetime.utcnow()
        today_ans_count = QuestionaireAnswer.query.filter_by(questionaire_id=id).filter_by(ip = ip).filter(db.cast(QuestionaireAnswer.timestamp, db.DATE) == db.cast(current_time, db.DATE)).count()
        if today_ans_count >= release.times:
            flash("对不起，您今日的回答次数已达到上限")
            return render_template("warning.html")

    if request.method == "POST":
        questionaire_answer = QuestionaireAnswer(
            questionaire_id = id,
            author_id = current_user.id if current_user.is_anonymous() == False else None,
            ip = request.remote_addr,
            timestamp = datetime.utcnow(),
            # questionaire = questionaire
        )
        db.session.add(questionaire_answer)
        db.session.commit()

        for i in range(length):
            if renderQuestions[i]["question"].relation is None:
                if renderQuestions[i]["question"].type in [0, 2, 3, 4]:
                    if ('ques_' + str(i) + '.ans') not in request.form and renderQuestions[i]["question"].must_do == True:
                        db.session.delete(questionaire_answer)
                        db.session.commit()
                        flash('问题' + str(i+1) + '是必答题，您还没有作答', 'error')
                        return render_template('ans_questionaire.html', questionaire=questionaire, 
                                renderQuestions=renderQuestions, length=length)
                    else :
                        if ('ques_' + str(i) + '.ans') in request.form:
                            qans = QuestionAnswer (
                                questionaire_answer_id = questionaire.id,
                                question_id = renderQuestions[i]["question"].id,
                                answer = request.form['ques_' + str(i) + '.ans'],
                            )
                            db.session.add(qans)
                elif renderQuestions[i]["question"].type == 1:
                    ans_count = 0
                    for j in range(len(renderQuestions[i]["options"])):
                            if ('ques_' + str(i) + '.ans-' + str(j)) in request.form:
                                qans = QuestionAnswer (
                                    questionaire_answer_id = questionaire.id,
                                    question_id = renderQuestions[i]["question"].id,
                                    answer = request.form['ques_' + str(i) + '.ans-' + str(j)],
                                )
                                ans_count += 1
                                db.session.add(qans)

                    if ans_count == 0 and renderQuestions[i]["question"].must_do == True:
                        db.session.delete(questionaire_answer)
                        db.session.commit()
                        flash('问题' + str(i+1) + '是必答题，您还没有作答', 'error')
                        return render_template('ans_questionaire.html', questionaire=questionaire, 
                                renderQuestions=renderQuestions, length=length)
            else:
                # 必答情况
                must = False
                relate_question = renderQuestions[i]["question"].relation.relate_ques
                relate_option = renderQuestions[i]["question"].relation.relate_option
                if renderQuestions[relate_question]["question"].type == 0:
                    if ('ques_' + str(relate_question) + '.ans') not in request.form or request.form['ques_' + str(relate_question) + '.ans'] != str(relate_option):
                        must = False
                    else:
                        must = True
                elif renderQuestions[relate_question]["question"].type == 1:
                    if ('ques_' + str(relate_question) + '.ans-' + str(relate_option)) not in request.form:
                        must = False
                    else:
                        must = True

                if renderQuestions[i]["question"].type in [0, 2, 3, 4]:
                    if must == True and ('ques_' + str(i) + '.ans') not in request.form and renderQuestions[i]["question"].must_do == True:
                        db.session.delete(questionaire_answer)
                        db.session.commit()
                        flash('问题' + str(i+1) + '是必答题，您还没有作答', 'error')
                        return render_template('ans_questionaire.html', questionaire=questionaire, 
                                renderQuestions=renderQuestions, length=length)
                    else :
                        if ('ques_' + str(i) + '.ans') in request.form:
                            qans = QuestionAnswer (
                                questionaire_answer_id = questionaire.id,
                                question_id = renderQuestions[i]["question"].id,
                                answer = request.form['ques_' + str(i) + '.ans'],
                            )
                            db.session.add(qans)
                elif renderQuestions[i]["question"].type == 1:
                    ans_count = 0
                    for j in range(len(renderQuestions[i]["options"])):
                            if ('ques_' + str(i) + '.ans-' + str(j)) in request.form:
                                qans = QuestionAnswer (
                                    questionaire_answer_id = questionaire.id,
                                    question_id = renderQuestions[i]["question"].id,
                                    answer = request.form['ques_' + str(i) + '.ans-' + str(j)],
                                )
                                ans_count += 1
                                db.session.add(qans)

                    if must == True and ans_count == 0 and renderQuestions[i]["question"].must_do == True:
                        db.session.delete(questionaire_answer)
                        db.session.commit()
                        flash('问题' + str(i+1) + '是必答题，您还没有作答', 'error')
                        return render_template('ans_questionaire.html', questionaire=questionaire, 
                                renderQuestions=renderQuestions, length=length)

            db.session.commit()
        flash("提交成功！感谢您的参与")
        return render_template("warning.html")
    return render_template('ans_questionaire.html', questionaire=questionaire, 
                            renderQuestions=renderQuestions, length=length)



def get_ans(question):
    ans = {}
    question_answers = question.questionanswers.all()
    if question.type == 0 or question.type == 1: #单选题
        for i in range(len(question.options.all())):
            pans = {
                str(i): 0
            }
            ans.update(pans)
        for q_answer in question_answers:
            ans[q_answer.answer] += 1
    elif question.type == 4:
        for i in range(question.score.radio_num):
            pans = {
                str(i): 0
            }
            ans.update(pans)
        for q_answer in question_answers:
            ans[q_answer.answer] += 1
    else:
        for q_answer in question_answers:
            pans = {
                q_answer.answer: 1
            }
            ans.update(pans)
    return ans




def get_tot_info(questionaire, release):
    questionaire_name = questionaire.title
    questionaire_description = questionaire.description
    questions = questionaire.questions.all()
    # options = 
    renderQuestions = []
    for question in questions:
        q = {
                    "question" : question,
                    "options" : question.options.all(),
                    "score" : question.score,
                    "answers": get_ans(question)
        }
        renderQuestions.append(q)
    return renderQuestions

########################################test#########################


@main.route('/questionaire/<int:id>/analyse', methods=["GET", "POST"])
@login_required
def analyse_questionaire(id):
    questionaire = Questionaire.query.get_or_404(id)
    releases = QuestionaireRelease.query.filter_by(questionaire_id=id).all()
    if len(releases) == 0:
        flash("对不起，该问卷尚未发布，无统计结果")
        return render_template("warning.html")

    release = releases[-1]
    renderQuestions = get_tot_info(questionaire, release)
    length = len(renderQuestions)



    return render_template("test.html", questionaire=questionaire, renderQuestions=renderQuestions, length=length)

