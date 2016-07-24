from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class MovieForm(Form):
    search = StringField('search', validators=[DataRequired()])
