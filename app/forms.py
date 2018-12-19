from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms_alchemy.fields import QuerySelectField
from app.models import Visitor, Category, Question, Answer

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First name:', validators=[DataRequired()])
    last_name = StringField('Lasta name:', validators=[DataRequired()])
    adresa_ptt = StringField('Zip code:', validators=[DataRequired()])
    adresa_mesto = StringField('Place:', validators=[DataRequired()])
    adresa_ulica_broj = StringField('Street and number:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    visitor_type_id_type_visitor = SelectField('Type of visitor', choices=[('1', 'Visitor'),('2', 'Admin')], validators=[DataRequired()])
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Repeat the password:', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registration')

class CategoryForm(FlaskForm):
    name = StringField('Name of category:', validators=[DataRequired()])
    explanation = StringField('Explain category:', validators=[DataRequired()])
    submit = SubmitField('Add category')

    def __repr__(self):
        return '{}'.format(self.name)

def choice_query():
    return Category.query.all()

class QuestionForm(FlaskForm):
    question_id_category = QuerySelectField('The question belongs to the category:', query_factory=choice_query, get_label='name', allow_blank=False)
    question_text = StringField('Text question:',validators=[DataRequired()])
    submit = SubmitField('Add question')

def choice_query_to_answer():
    return Question.query.all()

class AnswerForm(FlaskForm):
    answer_id_question = QuerySelectField('The answer belongs to the query:', query_factory=choice_query_to_answer, get_label='question_text', allow_blank=False)
    answer_text = StringField('Text answer:',validators=[DataRequired()])
    submit = SubmitField('Add answer')