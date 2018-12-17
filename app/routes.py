from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.models import Visitor

@app.route('/')
@app.route('/index')
@login_required
def index():
    """
        Ovo je  View funkcija za potrebe realizacije aplikativne rute /index.
        """
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        Ovo je  View funkcija za potrebe realizacije aplikativne rute /index.
        """
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
        return redirect(next_page)
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
