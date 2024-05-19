from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    ReEnterPass = StringField('Re-enter Password', validators=[DataRequired()])
    
    submit = SubmitField('Create account')
class UploadForm(FlaskForm):
    html = TextAreaField('HTML', validators=[DataRequired()])
    css = TextAreaField('CSS', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    submit = SubmitField('Upload')
