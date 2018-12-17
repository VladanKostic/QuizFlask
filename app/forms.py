from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

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