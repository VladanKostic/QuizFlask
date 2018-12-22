from app import app, db
from app.forms import LoginForm, RegistrationForm, CategoryForm, QuestionForm, AnswerForm, DummyAnswerForm, NewQuizForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.models import Visitor, Category, Question, Answer, DummyAnswer

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
def dummyanswer():
    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()
    form=DummyAnswerForm()
    if form.validate_on_submit():
        dummyanswer = DummyAnswer(dummyanswer_id_question=form.dummyanswer_id_question.data.id_question, dummy_answer_text=form.dummy_answer_text.data)
        db.session.add(dummyanswer)
        db.session.commit()
        flash('You are add new dummy answer on the question!')
        return render_template('index.html', user=user)
    return render_template('dummyanswer.html', title='Dummy answer', form=form)


@app.route('/newquiz', methods=['GET', 'POST'])
def newquiz():
    if current_user.is_authenticated:
        user = Visitor.query.filter_by(username=current_user.username).first()
    form = NewQuizForm()
    if form.validate_on_submit():
        selected_categories = request.form.getlist('selected_categories')
    #categories = Category.query.filter_by(id_category = None).all()
    categories = Category.query.all()
    return render_template('newquiz.html', title='New quiz setup', form=form, categories=categories)
