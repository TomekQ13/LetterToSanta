from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.core import StringField
from wtforms.validators import DataRequired

class SendFriendRequestForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    submit = SubmitField('Wyślij')