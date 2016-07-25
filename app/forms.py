from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class MovieForm(Form):
    search = StringField('search', validators=[DataRequired()])

class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[
        DataRequired(), 
        EqualTo('confirm', message="Passwords Must Be Equal")])
    confirm = PasswordField('confirm', validators=[DataRequired()])
