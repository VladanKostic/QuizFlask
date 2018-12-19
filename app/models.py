from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from sqlalchemy.orm import synonym

"""
Bila je greska pri radu:
AttributeError: 'Korisnik' object has no attribute 'is_active'
Your User class is missing methods that flask-login expects. Flask-login provides a UserMixin, which you are importing but not using.
"""
class Visitor(UserMixin,db.Model):
    id_visitor = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    adresa_ptt = db.Column(db.String(64), index=True, unique=True)
    adresa_mesto = db.Column(db.String(64), index=True, unique=True)
    adresa_ulica_broj = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    visitor_type_id_type_visitor = db.Column(db.Integer, index=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    id=synonym('id_visitor') # Resenje za raise NotImplementedError('No `id` attribute - override `get_id`') i primenu UserMix

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password( self, password ):
        self.password = generate_password_hash(password)

    def check_password( self, password ):
        return check_password_hash(self.password, password)

@login.user_loader
def load_user(id_visitor):
    return Visitor.query.get(int(id_visitor))

class Category(db.Model):
    id_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    explanation = db.Column(db.String(512), index=True)

def choice_query_category():
    return Category.query.all()

class Question(db.Model):
    id_question = db.Column(db.Integer, primary_key=True)
    question_id_category = db.Column(db.Integer, db.ForeignKey('category.id_category'))
    question_text = db.Column(db.String(256))
    num_question_in_game = db.Column(db.Integer)

def choice_query_to_answer():
    return Question.query.all()

class Answer(db.Model):
    id_answer = db.Column(db.Integer, primary_key=True)
    answer_id_question = db.Column(db.Integer, db.ForeignKey('question.id_question'))
    answer_text = db.Column(db.String(256))
