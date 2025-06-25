from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    phone = StringField('Phone', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    role = SelectField('Role', choices=[('seeker', 'Job Seeker'), ('employer', 'Job Provider')], validators=[InputRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class PostJobForm(FlaskForm):
    title = StringField('Job Title', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    salary = StringField('Salary', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    company = StringField('Company', validators=[InputRequired()])
    submit = SubmitField('Post Job')

from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class ApplicationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    resume = FileField('Resume (PDF only)', validators=[DataRequired(), FileAllowed(['pdf'], 'PDFs only!')])
    submit = SubmitField('Apply')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField