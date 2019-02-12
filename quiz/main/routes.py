from flask import Blueprint, render_template, session
from quiz.users.__utils__ import is_logged_in
from sqlite3 import Error
import sqlite3


main = Blueprint('main', __name__)


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html')


# Dashboard
@main.route('/dashboard')
@is_logged_in
def dashboard():
    if session['logged_in']:
        username = session['username']
        # Create cursor
        try:
            conn = sqlite3.connect("quiz.db")
            cur = conn.cursor()
            # Get user by username
            t = (username,)
            result = cur.execute('SELECT * FROM visitor WHERE username = ?', t)
            if result:
                # Get stored hash
                data = cur.fetchone()
                return render_template('dashboard.html', user=data[1])
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        except Error as e:
            print(e)
    else:
        error = 'User not login'
        return render_template('login.html', error=error)
        # Close connection
        # cur.close()
