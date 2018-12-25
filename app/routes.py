from app import app, db
from app.forms import LoginForm, RegistrationForm, CategoryForm, QuestionForm, AnswerForm, DummyAnswerForm, NewQuizForm, NewQuizStart
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.models import Visitor, Category, Question, Answer, DummyAnswer, Quiz, QuizDetails #, QuizShow
import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    """
        Ovo je  View funkcija za potrebe realizacije aplikativne rute /index.
        """
    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Visitor.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Wrong user name!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        #return redirect(next_page, user=user)
        return render_template('index.html', user=user)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Visitor(first_name=form.first_name.data,last_name=form.last_name.data,adresa_ptt=form.adresa_ptt.data, adresa_mesto=form.adresa_mesto.data, adresa_ulica_broj=form.adresa_ulica_broj.data, email=form.email.data,visitor_type_id_type_visitor=form.visitor_type_id_type_visitor.data,username=form.username.data,password=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations on registering for the quiz!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()
    form=CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, explanation=form.explanation.data)
        db.session.add(category)
        db.session.commit()
        flash('You are add new category on the quiz!')
        return render_template('index.html', user=user)
    return render_template('category.html', title='Category', form=form)

@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()
    form=QuestionForm()
    if form.validate_on_submit():
        question = Question(question_id_category=form.question_id_category.data.id_category, question_text=form.question_text.data, num_question_in_game=0)
        db.session.add(question)
        db.session.commit()
        flash('You are add new question on the quiz!')
        return render_template('index.html', user=user)
    return render_template('question.html', title='Question', form=form)

@app.route('/answer', methods=['GET', 'POST'])
@login_required
def answer():
    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()
    form=AnswerForm()
    if form.validate_on_submit():
        answer = Answer(answer_id_question=form.answer_id_question.data.id_question, answer_text=form.answer_text.data)
        db.session.add(answer)
        db.session.commit()
        flash('You are add new answer on the question!')
        return render_template('index.html', user=user)
    return render_template('answer.html', title='Answer', form=form)

@app.route('/dummyanswer', methods=['GET', 'POST'])
@login_required
def dummyanswer():
    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()
    form=DummyAnswerForm()
    if form.validate_on_submit():
        dummyanswer = DummyAnswer(dummyanswer_id_question=form.dummyanswer_id_question.data.id_question, dummy_answer_text=form.dummy_answer_text.data, serial_number=1)
        db.session.add(dummyanswer)
        db.session.commit()
        flash('You are add new dummy answer on the question!')
        return render_template('index.html', user=user)
    return render_template('dummyanswer.html', title='Dummy answer', form=form)


@app.route('/newquiz', methods=['GET', 'POST'])
@login_required
def newquiz():
    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()
    form = NewQuizForm()
    if form.validate_on_submit():
        selected_categories = request.form.getlist('selected_categories')
        max_num_question = request.form.get('maxnumquestion')
        create_time = datetime.datetime.now()
        quiz = Quiz(id_visitor=user.id_visitor, datetime_of_create=create_time, datetime_of_start=create_time, datetime_of_end=create_time,total_question_true=0, total_question_false=0,total_score_in_percent=0)
        db.session.add(quiz)
        db.session.commit()
        current_quiz =  Quiz.query.filter_by(id_visitor=user.id_visitor,datetime_of_create=create_time).first()
        for current_category in selected_categories:
            current_question = 1
            for current_question in range(int(max_num_question)):
                quizdetails = QuizDetails(id_quiz=current_quiz.id_quiz,id_category=int(current_category),id_question=1)
                db.session.add(quizdetails)
                db.session.commit()
        #return render_template('newquizstart.html', title='New quiz start', form=form, current_quiz=current_quiz)
        flash('You create new quiz!')
        return redirect(url_for('newquizstart',current_quiz=current_quiz.id_quiz))
    categories = Category.query.all()
    return render_template('newquiz.html', title='New quiz setup', form=form, categories=categories)

@app.route('/newquizstart', methods=['GET', 'POST'])
@login_required
def newquizstart():
    print(request)
    current_quiz = request.args.get('current_quiz', None)

    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        if request.form["quiz"] == "Start":
            start_quiz=Quiz.query.filter_by(id_quiz=current_quiz).first()
            startime = datetime.datetime.now()
            start_quiz.datetime_of_start = startime
            db.session.commit()
            quizshow = []

            if current_quiz != '':
                quizshow = db.session.execute('select\
                                                quiz.id_quiz,\
                                                question.question_text,\
                                                "QUI"||quiz.id_quiz||"DET"||quiz_details.id_quiz_details||"QUE"||question.id_question as radio_name,\
                                                (select answer_text from answer where answer_id_question = question.id_question) answer_text, 1 as answer_value,\
                                                (select dummy_answer_text from dummy_answer where dummyanswer_id_question = question.id_question and serial_number = 1) dummy_answer_text1, 0 as dummy_answer_value1,\
                                                (select dummy_answer_text from dummy_answer where dummyanswer_id_question = question.id_question and serial_number = 2) dummy_answer_text2, 0 as dummy_answer_value2,\
                                                (select dummy_answer_text from dummy_answer where dummyanswer_id_question = question.id_question and serial_number = 3) dummy_answer_text3, 0 as dummy_answer_value3 \
                                                from quiz, quiz_details , question \
                                                where quiz.id_quiz = :val \
                                                and quiz.id_quiz = quiz_details.id_quiz \
                                                and quiz_details.id_question = question.id_question',
                                                {'val': current_quiz})
                return render_template('newquizstart.html', title='New quiz start', quizshow=quizshow, startime=startime)
        elif request.form["quiz"] == "Finish":
            """ Setuj vreme zavrsetka i disejblus taster start """
            finish_quiz = Quiz.query.filter_by(id_quiz=current_quiz).first()
            print(finish_quiz)
            endtime = datetime.datetime.now()
            finish_quiz.datetime_of_end = endtime
            db.session.commit()
            """ Pokupi sva radio polja """
            finishquizdetails = []
            finishquizdetails = db.session.execute('select * from quiz_details where quiz_details.id_quiz = :val',{'val':finish_quiz.id_quiz})
            print(finishquizdetails)
            """ Prodji kroz njih u petlji """
            for finishquizdetail in finishquizdetails:
                """ procitaj vrednosti i upisi u quiz_details """
                current_option = "QUI"+str(finishquizdetail.id_quiz)+"DET"+str(finishquizdetail.id_quiz_details)+"QUE"+str(finishquizdetail.id_question)
                print(current_option)
                option = request.form[current_option]
                """ procitaj vrednosti i upisi u quiz_details """
                current_row = QuizDetails.query.filter_by(id_quiz_details=finishquizdetail.id_quiz_details).first()
                current_row.answer_true =  option
            """ Prikazi statistiku """
            db.session.commit()
    return render_template('newquizstart.html', title='New quiz start')




