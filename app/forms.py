from flask.ext.wtf import Form
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

class MovieForm(Form):
    search = StringField('search', validators=[DataRequired()])

class PosterForm(Form):
    url = StringField('url', validators=[DataRequired()])
    imdbid = HiddenField('imdbid', validators=[DataRequired()])

class QueueForm(Form):
    name = StringField('name', validators=[DataRequired()])
