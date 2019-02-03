from flask_wtf import FlaskForm
from wtforms import StringField, validators
from wtforms.validators import DataRequired
from wtforms_alchemy.fields import QuerySelectField
from app.models import Category, Question


class CategoryForm(FlaskForm):
    name = StringField('Name of category:', validators=[DataRequired()])
    explanation = StringField('Explain category:', validators=[DataRequired()])

    def __repr__(self):
        return '{}'.format(self.name)


def choice_query():
    return Category.query.all()


class QuestionForm(FlaskForm):
    id_category = QuerySelectField('The question belongs to the category:', query_factory=choice_query, get_label='name', allow_blank=False)
    question_text = StringField('Text question:', validators=[DataRequired()])
    num_question_in_game = StringField('Num question in game:', validators=[DataRequired()])


def choice_query_to_answer():
    return Question.query.all()


class AnswerForm(FlaskForm):
    id_question = QuerySelectField('The answer belongs to the query:', query_factory=choice_query_to_answer, get_label='question_text', allow_blank=False)
    answer_text = StringField('Text answer:', validators=[DataRequired()])


def choice_query_to_du_answer():
    return Question.query.all()


class DummyAnswerForm(FlaskForm):
    id_question = QuerySelectField('The dummy answer belongs to the query:', query_factory=choice_query_to_du_answer, get_label='question_text', allow_blank=False)
    dummy_answer_text = StringField('Text for dummy answer:', [validators.DataRequired(), validators.Length(min=1, max=250, message='Dummy answer cannot be more than 25 characters!!!')])
    serial_number = StringField('Add serial number for dummy answer:', validators=[DataRequired()])


class NewQuizForm(FlaskForm):
    pass


class NewQuizStart(FlaskForm):
    pass
