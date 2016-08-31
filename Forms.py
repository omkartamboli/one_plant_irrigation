from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, IntegerField, FloatField
from wtforms.validators import DataRequired, Optional


class LoginForm(Form):
    """Form class for user login."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class TurnOnTapForm(Form):
    secondsInFloat = StringField('Seconds to turn on tap for', validators=[Optional()])


class AppConfigForm(Form):
    EnableEmailNotifications = RadioField('Enable Email', validators=[DataRequired()])
    EnableSMSNotifications = RadioField('Enable SMS', validators=[DataRequired()])

    graph_no_of_hours = IntegerField('Hours (Graph)', validators=[DataRequired()])
    data_no_of_hours = IntegerField('Hours (Data)', validators=[DataRequired()])

    EnablePumpFunctions = RadioField('Enable Waterpump', validators=[DataRequired()])
    maxTimeToKeepPumpOnInSeconds = FloatField('Pump Max (Seconds)', validators=[DataRequired()])
    timeToKeepPumpOnInSecondsForFullWaterCapacity = FloatField('Pump Full Capacity (Seconds)',
                                                               validators=[DataRequired()])
