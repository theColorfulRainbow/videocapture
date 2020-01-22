from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LectureForm(FlaskForm):
    course = StringField('Course',
                           validators=[DataRequired()])
    amount = StringField('Amount of Topics',
                           validators=[DataRequired()])

    submit = SubmitField('Download')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PDFUpload(FlaskForm):
    pdf = FileField('Upload PDF', validators=[FileAllowed(['pdf']),DataRequired()])
    topic_positions = StringField('Ascending Page Number(s) Where Topic Ends', validators=[DataRequired(), Length(min=1, max=100)])
    course = StringField('Course')
    submit = SubmitField('Integrate')

class LectureUpload(FlaskForm):
    file = FileField('Upload PDF/Powerpoint', validators=[FileAllowed(['pptx','pdf']),DataRequired()])
    topic_positions = StringField('Ascending Page Number(s) Where Topic Ends', validators=[DataRequired(), Length(min=1, max=500)])
    course = StringField('Course')
    submit = SubmitField('Integrate')