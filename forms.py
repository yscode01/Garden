from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    keywords = StringField('Keywords', validators=[DataRequired()])
    category = StringField('Category')
    author = StringField('Author')
    tags = StringField('Tags')
    submit = SubmitField('Search')
