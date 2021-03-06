from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class LetterForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class LetterLineForm(FlaskForm):
    line_content = TextAreaField('Przedmiot', validators=[DataRequired()])
    submit = SubmitField('Dodaj')