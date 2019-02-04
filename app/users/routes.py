from flask import Blueprint, render_template, flash, redirect, request, url_for, session
from app.users.__utils__ import is_logged_in
from passlib.hash import sha256_crypt
import sqlite3
from sqlite3 import Error
from app.users.forms import RegistrationForm


users = Blueprint('users', __name__)


# User login
@users.route('/login', methods=['GET', 'POST'])
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
                return redirect(url_for('main.dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
            # Close connection
            # cur.close()
    return render_template('login.html')


# User logout
@users.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('users.login'))


# User registration
@users.route('/register', methods=['GET', 'POST'])
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
