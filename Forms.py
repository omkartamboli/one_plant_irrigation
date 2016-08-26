from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Optional


class LoginForm(Form):
    """Form class for user login."""
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class TurnOnTapForm(Form):
    secondsInFloat = StringField('Seconds to turn on tap for', validators=[Optional()])

