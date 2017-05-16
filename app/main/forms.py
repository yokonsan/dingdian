from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    name = StringField('你要搜索的小说名是？', validators=[DataRequired()])
    submit = SubmitField('搜索')

