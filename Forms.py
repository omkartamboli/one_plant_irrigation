from flask_wtf import Form
from wtforms import StringField, PasswordField, RadioField, IntegerField, FloatField
from wtforms.validators import DataRequired, Optional


class LoginForm(Form):
    """Form class for user login."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class TurnOnTapForm(Form):
    secondsInFloat = StringField('Seconds to turn on tap for', validators=[Optional()])


class TurnOnRefillTapForm(Form):
    secondsInFloat = StringField('Seconds to turn on refill tap for', validators=[DataRequired()])


class AppConfigForm(Form):
    EnableEmailNotifications = RadioField('Enable Email', validators=[DataRequired()],
                                          choices=[('True', 'On'), ('False', 'Off')])
    EnableSMSNotifications = RadioField('Enable SMS', validators=[DataRequired()],
                                        choices=[('True', 'On'), ('False', 'Off')])

    graph_no_of_hours = IntegerField('Hours (Graph)', validators=[DataRequired()])
    data_no_of_hours = IntegerField('Hours (Data)', validators=[DataRequired()])

    EnablePumpFunctions = RadioField('Enable Waterpump', validators=[DataRequired()],
                                     choices=[('True', 'On'), ('False', 'Off')])
    maxTimeToKeepPumpOnInSeconds = FloatField('Pump Max (Seconds)', validators=[DataRequired()])
    timeToKeepPumpOnInSecondsForFullWaterCapacity = FloatField('Pump Full Capacity (Seconds)',
                                                               validators=[DataRequired()])
    no_of_mins_for_rational_value = FloatField('Minutes for rational value', validators=[DataRequired()])