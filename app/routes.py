from app import app, db
from app.forms import RegistrationForm, CategoryForm, QuestionForm, AnswerForm, DummyAnswerForm, NewQuizForm
from flask import render_template, flash, redirect, request, url_for, session
from app.models import Visitor, Category, Question, Quiz, QuizDetails
from passlib.hash import sha256_crypt
import sqlite3
from sqlite3 import Error
from functools import wraps
import datetime


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


# User login
# noinspection PyUnreachableCode,PyUnreachableCode
@app.route('/login', methods=['GET', 'POST'])
def login():
    global result, conn
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()

        # Get user by username
        t = (username,)
        try:
            result = cur.execute('SELECT * FROM visitor WHERE username = ?', t)
        except Error as e:
            print(e)

        if result:
            # Get stored hash
            data = cur.fetchone()
            password = data[9]
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    global conn
    form = RegistrationForm(request.form)
    print(request.method)
    if request.method == 'POST':
        first_name = form.first_name.data
        last_name = form.last_name.data
        adresa_ptt = form.adresa_ptt.data
        adresa_mesto = form.adresa_mesto.data
        adresa_ulica_broj = form.adresa_ulica_broj.data
        email = form.email.data
        visitor_type_id_type_visitor = form.visitor_type_id_type_visitor.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute query
        cur.execute(
            "INSERT INTO visitor (first_name,last_name,adresa_ptt,adresa_mesto,adresa_ulica_broj,email,visitor_type_id_type_visitor,username,password) VALUES(?,?,?,?,?,?,?,?,?)",
            (first_name, last_name, adresa_ptt, adresa_mesto, adresa_ulica_broj, email, visitor_type_id_type_visitor,
             username, password))
        # Commit to DB
        conn.commit()
        # Close connection
        cur.close()
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    global user
    if session['logged_in']:
        username = session['username']
        user = Visitor.query.filter_by(username=username).first()
    return render_template('dashboard.html', user=user)


# noinspection PyUnreachableCode
@app.route('/category', methods=['GET', 'POST'])
@is_logged_in
def category():
    # Create cursor
    global conn

    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    # Get category
    result_cat = cur.execute("SELECT * FROM category")
    categorys = cur.fetchall()
    print(categorys)
    if result_cat:
        return render_template('category.html', categorys=categorys)
    else:
        msg = 'No category Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection


@app.route('/category_add', methods=['GET', 'POST'])
@is_logged_in
def category_add():
    global conn
    form = CategoryForm(request.form)
    if request.method == 'POST':  # and form.validate():
        name = form.name.data
        explanation = form.explanation.data
        # Create cursor
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute
        cur.execute("INSERT INTO category(name, explanation) VALUES(?,?)", (name, explanation))
        # Commit to DB
        conn.commit()
        # Close connection
        conn.close()
        flash('Category created', 'success')
        return redirect(url_for('category'))
    return render_template('category_add.html', form=form)


# Edit Category
@app.route('/category_edit/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def category_edit(p_id):
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()

    # Get article by id
    category_e = cur.fetchone()
    cur.close()
    # Get form
    form = CategoryForm(request.form)
    # Populate category form fields
    form.name.data = category_e[1]
    form.explanation.data = category_e[2]
    if request.method == 'POST':  # and form.validate():
        name = request.form['name']
        explanation = request.form['explanation']
        print(explanation)
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute
        cur.execute("UPDATE category SET name = ?, explanation = ? WHERE id_category = ?", (name, explanation, p_id))
        # Commit to DB
        conn.commit()
        # Close connection
        cur.close()
        flash('Category updated', 'success')
        return redirect(url_for('category'))
    return render_template('category_edit.html', form=form)


# Delete Category
@app.route('/category_delete/<string:c_id>', methods=['GET', 'POST'])
@is_logged_in
def category_delete(c_id):
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    # Execute
    cur.execute("DELETE FROM category WHERE id_category = ?", [c_id])
    # Commit to DB
    conn.commit()
    # Close connection
    cur.close()
    flash('Category deleted', 'success')
    return redirect(url_for('category'))


# noinspection PyUnreachableCode
@app.route('/question', methods=['GET', 'POST'])
@is_logged_in
def question():
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    # Get question
    result_q = cur.execute("SELECT * FROM question")
    questions = cur.fetchall()
    if result_q:
        return render_template('question.html', questions=questions)
    else:
        msg = 'No question Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection


@app.route('/question_add', methods=['GET', 'POST'])
@is_logged_in
def question_add():
    global conn
    form = QuestionForm(request.form)
    if request.method == 'POST':  # and form.validate():
        id_category = form.id_category.data.id_category
        question_text = form.question_text.data
        num_question_in_game = form.num_question_in_game.data
        print(id_category, question_text, num_question_in_game)
        # Create cursor
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute
        cur.execute("INSERT INTO question(id_category, question_text, num_question_in_game) VALUES(?,?, ?)",
                    (id_category, question_text, num_question_in_game))
        # Commit to DB
        conn.commit()
        # Close connection
        conn.close()
        flash('Question created', 'success')
        return redirect(url_for('question'))
    return render_template('question_add.html', form=form)


# Edit Question
@app.route('/question_edit/<string:q_id>', methods=['GET', 'POST'])
@is_logged_in
def question_edit(q_id):
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()

    # Get article by q_id

    question_e = cur.fetchone()
    cur.close()
    # Get form
    form = QuestionForm(request.form)
    # Populate category form fields
    form.id_category.data = question_e[1]
    form.question_text.data = question_e[2]
    form.num_question_in_game.data = question_e[3]
    if request.method == 'POST':  # and form.validate():
        id_category = request.form['id_category']
        question_text = request.form['question_text']
        num_question_in_game = request.form['num_question_in_game']
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute
        cur.execute(
            "UPDATE question SET id_category = ?, question_text = ?, num_question_in_game = ? WHERE id_question = ?",
            (id_category, question_text, num_question_in_game, q_id))
        # Commit to DB
        conn.commit()
        # Close connection
        cur.close()
        flash('Question updated', 'success')
        return redirect(url_for('question'))
    return render_template('question_edit.html', form=form)


# Delete Question
@app.route('/question_delete/<string:qd_id>', methods=['GET', 'POST'])
@is_logged_in
def question_delete(qd_id):
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    # Execute
    cur.execute("DELETE FROM question WHERE id_question = ?", [qd_id])
    # Commit to DB
    conn.commit()
    # Close connection
    cur.close()
    flash('Question deleted', 'success')
    return redirect(url_for('question'))


# Answer
# noinspection PyUnreachableCode
@app.route('/answer', methods=['GET', 'POST'])
@is_logged_in
def answer():
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    # Get category
    result_a = cur.execute("SELECT * FROM answer")
    answers = cur.fetchall()
    if result_a:
        return render_template('answer.html', answers=answers)
    else:
        msg = 'No answer Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection


# Add answer
@app.route('/answer_add', methods=['GET', 'POST'])
@is_logged_in
def answer_add():
    global conn
    form = AnswerForm(request.form)
    if request.method == 'POST':  # and form.validate():
        id_question = form.id_question.data.id_question
        answer_text = form.answer_text.data
        # Create cursor
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute
        cur.execute("INSERT INTO answer(id_question, answer_text) VALUES(?,?)", (id_question, answer_text))
        # Commit to DB
        conn.commit()
        # Close connection
        conn.close()
        flash('Answer created', 'success')
        return redirect(url_for('answer'))
    return render_template('answer_add.html', form=form)


# Edit answer
@app.route('/answer_edit/<string:ae_id>', methods=['GET', 'POST'])
@is_logged_in
def answer_edit(ae_id):
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()

    # Get article by ae_id

    category_a = cur.fetchone()
    cur.close()
    # Get form
    form = AnswerForm(request.form)
    # Populate category form fields
    form.id_question.data = category_a[1]
    form.answer_text.data = category_a[2]
    if request.method == 'POST':  # and form.validate():
        id_question = request.form['id_question']
        answer_text = request.form['answer_text']
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute
        cur.execute("UPDATE answer SET id_question = ?, answer_text = ? WHERE id_answer = ?",
                    (id_question, answer_text, ae_id))
        # Commit to DB
        conn.commit()
        # Close connection
        cur.close()
        flash('Answer updated', 'success')
        return redirect(url_for('answer'))
    return render_template('answer_edit.html', form=form)


# Delete answer
@app.route('/answer_delete/<string:ad_id>', methods=['GET', 'POST'])
@is_logged_in
def answer_delete(ad_id):
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    # Execute
    cur.execute("DELETE FROM answer WHERE id_answer = ?", [ad_id])
    # Commit to DB
    conn.commit()
    # Close connection
    cur.close()
    flash('Answer deleted', 'success')
    return redirect(url_for('answer'))


# noinspection PyUnreachableCode
@app.route('/answerdummy', methods=['GET', 'POST'])
@is_logged_in
def answerdummy():
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    # Get category
    result_ad = cur.execute("SELECT * FROM dummy_answer")
    answerds = cur.fetchall()
    if result_ad:
        return render_template('answerdummy.html', answerds=answerds)
    else:
        msg = 'No answer dummy found'
        return render_template('dashboard.html', msg=msg)
    # Close connection


# Add answer
@app.route('/answerdummy_add', methods=['GET', 'POST'])
@is_logged_in
def answerdummy_add():
    global conn
    form = DummyAnswerForm(request.form)
    if request.method == 'POST':  # and form.validate():
        id_question = form.id_question.data.id_question
        dummy_answer_text = form.dummy_answer_text.data
        serial_number = form.serial_number.data
        # Create cursor
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute
        cur.execute("INSERT INTO dummy_answer(id_question, dummy_answer_text, serial_number) VALUES(?,?,?)",
                    (id_question, dummy_answer_text, serial_number))
        # Commit to DB
        conn.commit()
        # Close connection
        conn.close()
        flash('Answer created', 'success')
        return redirect(url_for('answerdummy'))
    return render_template('answerdummy_add.html', form=form)


# Edit answer
@app.route('/answerdummy_edit/<string:ans_id>', methods=['GET', 'POST'])
@is_logged_in
def answerdummy_edit(ans_id):
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()

    # Get article by ans_id

    cur.close()
    # Get form
    form = DummyAnswerForm(request.form)
    # Populate category form fields
    form.id_question.data = category[1]
    form.dummy_answer_text.data = category[2]
    form.serial_number.data = category[3]
    if request.method == 'POST':  # and form.validate():
        id_question = request.form['id_question']
        dummy_answer_text = request.form['dummy_answer_text']
        serial_number = request.form['serial_number']
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()
        # Execute
        cur.execute(
            "UPDATE dummy_answer SET id_question = ?, dummy_answer_text = ?, dummy_answer_text = ? WHERE id_dummy_answer = ?",
            (id_question, dummy_answer_text, serial_number, ans_id))
        # Commit to DB
        conn.commit()
        # Close connection
        cur.close()
        flash('Dummy answer updated', 'success')
        return redirect(url_for('answer'))
    return render_template('answerdummy_edit.html', form=form)


# Delete answer
@app.route('/answerdummy_delete/<string:ansd_id>', methods=['GET', 'POST'])
@is_logged_in
def answerdummy_delete(ansd_id):
    # Create cursor
    global conn
    try:
        conn = sqlite3.connect("quiz.db")
    except Error as e:
        print(e)
    cur = conn.cursor()
    # Execute
    cur.execute("DELETE FROM dummy_answer WHERE id_dummy_answer = ?", [ansd_id])
    # Commit to DB
    conn.commit()
    # Close connection
    cur.close()
    flash('Dummy answer deleted', 'success')
    return redirect(url_for('answer'))


@app.route('/newquiz', methods=['GET', 'POST'])
@is_logged_in
def newquiz():
    global user, conn
    loged = session['logged_in']  # True or False
    username = session['username']
    if loged:
        user = Visitor.query.filter_by(username=username).first()
    form = NewQuizForm()
    if request.method == 'POST':  # if form.validate_on_submit():
        # Create cursor
        try:
            conn = sqlite3.connect("quiz.db")
        except Error as e:
            print(e)
        cur = conn.cursor()

        selected_categories = request.form.getlist('selected_categories')
        max_num_question = request.form.get('maxnumquestion')
        create_time = datetime.datetime.now()

        # Execute
        cur.execute(
            "INSERT INTO quiz (id_visitor,datetime_of_create,datetime_of_start,datetime_of_end,total_question_true,total_question_false,total_score_in_percent) VALUES (?,?,?,?,?,?,?) ",
            (user.id_visitor, create_time, create_time, create_time, 0, 0, 0))
        # quiz = Quiz(id_visitor=user.id_visitor, datetime_of_create=create_time, datetime_of_start=create_time, datetime_of_end=create_time,total_question_true=0, total_question_false=0,total_score_in_percent=0)
        # db.session.add(quiz)
        # db.session.commit()
        # Commit to DB
        conn.commit()

        quiz_new = Quiz.query.filter_by(id_visitor=user.id_visitor, datetime_of_create=create_time).first()

        for current_category in selected_categories:

            for current_num_question in range(int(max_num_question)):
                current_id_question = get_id_question_for_category(int(current_category))
                quizdetails = QuizDetails(id_quiz=quiz_new.id_quiz, id_category=int(current_category),
                                          id_question=current_id_question)
                db.session.add(quizdetails)
                db.session.commit()
        # return render_template('newquizstart.html', title='New quiz start', form=form, current_quiz=current_quiz)
        flash('You create new quiz!')
        return redirect(url_for('newquizstart', current_quiz=quiz_new.id_quiz))
    categories = Category.query.all()
    return render_template('newquiz.html', title='New quiz setup', form=form, categories=categories)


def get_id_question_for_category(p_current_category):
    """Pitanja sa minimalnim brojem koriscenja"""
    question_min = db.session.execute(
        'select id_question,min(num_question_in_game) from question where id_category=:val group by id_category',
        {'val': p_current_category}).first()
    return_id_question = question_min.id_question
    query_question = Question.query.filter_by(id_question=return_id_question).first()
    query_question.num_question_in_game = query_question.num_question_in_game + 1
    db.session.commit()
    return return_id_question


@app.route('/newquizstart', methods=['GET', 'POST'])
@is_logged_in
def newquizstart():
    global procenat_uspeha, user
    print(request)
    current_quiz = request.args.get('current_quiz', None)

    loged = session['logged_in']  # True or False
    username = session['username']
    if loged:
        user = Visitor.query.filter_by(username=username).first()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        if request.form["quiz"] == "Start":
            start_quiz = Quiz.query.filter_by(id_quiz=current_quiz).first()
            startime = datetime.datetime.now()
            start_quiz.datetime_of_start = startime
            db.session.commit()
            if current_quiz != '':
                quizshow = db.session.execute('select\
                                                quiz.id_quiz,\
                                                question.question_text,\
                                                "QUI"||quiz.id_quiz||"DET"||quiz_details.id_quiz_details||"QUE"||question.id_question as radio_name,\
                                                (select answer_text from answer where id_question = question.id_question) answer_text, 1 as answer_value,\
                                                (select dummy_answer_text from dummy_answer where id_question = question.id_question and serial_number = 1) dummy_answer_text1, 0 as dummy_answer_value1,\
                                                (select dummy_answer_text from dummy_answer where id_question = question.id_question and serial_number = 2) dummy_answer_text2, 0 as dummy_answer_value2,\
                                                (select dummy_answer_text from dummy_answer where id_question = question.id_question and serial_number = 3) dummy_answer_text3, 0 as dummy_answer_value3,\
                                                (select a1||","||a2||","||a3||","||a4 as random_answer FROM random_answer order by random() limit 1) as random_answer\
                                                from quiz, quiz_details , question \
                                                where quiz.id_quiz = :val \
                                                and quiz.id_quiz = quiz_details.id_quiz \
                                                and quiz_details.id_question = question.id_question',
                                              {'val': current_quiz})
                return render_template('newquizstart.html', title='New quiz start', quizshow=quizshow,
                                       startime=startime)
        elif request.form["quiz"] == "Finish":
            """ Setuj vreme zavrsetka i disejblus taster start """
            finish_quiz = Quiz.query.filter_by(id_quiz=current_quiz).first()
            print(finish_quiz)
            endtime = datetime.datetime.now()
            finish_quiz.datetime_of_end = endtime
            db.session.commit()
            """ Pokupi sva radio polja """

            finishquizdetails = db.session.execute('select * from quiz_details where quiz_details.id_quiz = :val',
                                                   {'val': finish_quiz.id_quiz})
            print(finishquizdetails)
            """ Prodji kroz njih u petlji """
            for finishquizdetail in finishquizdetails:
                """ procitaj vrednosti i upisi u quiz_details """
                current_option = "QUI" + str(finishquizdetail.id_quiz) + "DET" + str(
                    finishquizdetail.id_quiz_details) + "QUE" + str(finishquizdetail.id_question)
                print(current_option)
                option = request.form[current_option]
                """ procitaj vrednosti i upisi u quiz_details """
                current_row = QuizDetails.query.filter_by(id_quiz_details=finishquizdetail.id_quiz_details).first()
                current_row.answer_true = option
            """ Prikazi statistiku """
            db.session.commit()
            start_quiz = Quiz.query.filter_by(id_quiz=current_quiz).first()
            quizstat = db.session.execute('select count(*) as num_que, sum(answer_true) as num_true_que\
                                                                       from quiz_details\
                                                                       where id_quiz = :val',
                                          {'val': current_quiz})
            for rows in quizstat:
                print(rows.num_true_que)
                print(rows.num_que)
                procenat_uspeha = (int(rows.num_true_que) * 100) / int(rows.num_que)
            return render_template('finish.html', title='Finish quiz', user=user, procenat_uspeha=procenat_uspeha,
                                   quiz=start_quiz.id_quiz, starttime=start_quiz.datetime_of_start, endtime=endtime)
    return render_template('newquizstart.html', title='New quiz start')


@app.route('/finish', methods=['GET', 'POST'])
@is_logged_in
def finish():
    # noinspection PyGlobalUndefined
    global quiz
    loged = session['logged_in']  # True or False
    """username = session['username']"""
    if loged:
        pass
        """user = Visitor.query.filter_by(username=username).first()"""
    id_quiz = request.args.get('quiz', None)
    starttime = request.args.get('starttime', None)
    endtime = request.args.get('endtime', None)

    if id_quiz != '':
        quiz = db.session.execute('select count(*) as num_que, sum(answer_true) as num_true_que\
                                                           from quiz_details\
                                                           where id_quiz = :val',
                                  {'val': id_quiz})
    uspeha_procenat = (quiz.num_true_que * 100) / quiz.num_que

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    return render_template('finish.html', title='Finish quiz', procenat_uspeha=uspeha_procenat, starttime=starttime,
                           endtime=endtime)


@app.route('/sofar')
@is_logged_in
def sofar():
    global user
    loged = session['logged_in']  # True or False
    username = session['username']
    if loged:
        user = Visitor.query.filter_by(username=username).first()

    results = db.session.execute('select quiz.id_quiz as id_quiz, datetime(quiz.datetime_of_create, "localtime") as datetime_of_create, datetime(quiz.datetime_of_start, "localtime") as datetime_of_start, datetime(quiz.datetime_of_end, "localtime") as datetime_of_end,\
                                    count(*) as number_of_question, sum(quiz_details.answer_true) as number_of_true\
                                    from quiz, quiz_details\
                                    where quiz.id_visitor = :val\
                                    and quiz.id_quiz = quiz_details.id_quiz\
                                    group by quiz.id_quiz, quiz.datetime_of_create, quiz.datetime_of_start, quiz.datetime_of_end;',
                                 {'val': user.id_visitor})
    print(0)
    if not results:
        print(1)
        flash('Nije pronadjen rezultat!')
        return redirect(url_for('sofar.html'))
    else:
        data = results.fetchall()
        return render_template('sofar.html', user=user, data=data)


@app.route('/sofargrapf')
def sofargraph():
    loged = session['logged_in']  # True or False
    username = session['username']
    results = []
    labels = []
    values = []

    if loged:
        user_so_far_graph = Visitor.query.filter_by(username=username).first()
        results = db.session.execute('select quiz.id_quiz as id_quiz, datetime(quiz.datetime_of_create, "localtime") as datetime_of_create, datetime(quiz.datetime_of_start, "localtime") as datetime_of_start, datetime(quiz.datetime_of_end, "localtime") as datetime_of_end,\
                                        count(*) as number_of_question, sum(ifnull(quiz_details.answer_true,0)) as number_of_true\
                                        from quiz, quiz_details\
                                        where quiz.id_visitor = :val\
                                        and quiz.id_quiz = quiz_details.id_quiz\
                                        group by quiz.id_quiz, quiz.datetime_of_create, quiz.datetime_of_start, quiz.datetime_of_end;',
                                     {'val': user_so_far_graph.id_visitor})

    for row in results:
        labels.append(row["datetime_of_end"])
        estimation = (100 * row["number_of_true"]) / row["number_of_question"]
        values.append(estimation)
    line_labels = labels
    line_values = values
    return render_template('sofargraph.html', title='Graph of the result', max=100, labels=line_labels,
                           values=line_values)
