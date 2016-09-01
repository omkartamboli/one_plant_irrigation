from flask import *
from dbFunctions import getEventLogOfLastNHours, getLatestEventsData, updateConfigValue
from GPIOConfig import data_no_of_hours, graph_no_of_hours, project_description, getConfigValue, loadConfigFromDb
from WebAppConfig import *
from EventNames import CheckMoistureLevelEvent
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, set_login_view
from User import *
from Forms import LoginForm, TurnOnTapForm, AppConfigForm
from flask_bcrypt import Bcrypt
from GenerateGraph import plot_graph
from WaterPumpFunctions import turnOnWaterForCorrectSeconds
import datetime
import logging
import os
from os import path

app = Flask(__name__, static_url_path='')
login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)
app.secret_key = appSecretKey
with app.app_context():
    set_login_view("login")

app.config.__setitem__('SQLALCHEMY_DATABASE_URI',
                       'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.format(dbUser, dbPass, dbHost, dbPort, dbSchema))
app.config.__setitem__('SQLALCHEMY_TRACK_MODIFICATIONS', True)
db.init_app(app)

phones = ["iphone", "android", "blackberry"]

def loadAppConfigFormFromDB():
    form = AppConfigForm(csrf_enabled=True)
    form.EnableEmailNotifications.data = str(getConfigValue('EnableEmailNotifications'))
    form.EnableSMSNotifications.data = str(getConfigValue('EnableSMSNotifications'))
    form.EnablePumpFunctions.data = str(getConfigValue('EnablePumpFunctions'))
    form.data_no_of_hours.data = getConfigValue('data_no_of_hours')
    form.graph_no_of_hours.data = getConfigValue('graph_no_of_hours')
    form.maxTimeToKeepPumpOnInSeconds.data = getConfigValue('maxTimeToKeepPumpOnInSeconds')
    form.timeToKeepPumpOnInSecondsForFullWaterCapacity.data = getConfigValue(
        'timeToKeepPumpOnInSecondsForFullWaterCapacity')
    return form

@app.route("/")
def home():
    result = getEventLogOfLastNHours(data_no_of_hours, CheckMoistureLevelEvent)
    data = [dict(eventTime=row[0],
                 eventAnalogValue=row[1]) for row in result]

    return render_template('home.html', project_description=project_description,
                           isMobileRequest=isMobileRequest(request))


@app.route("/dashboard")
def dashboard():
    # Load configuration from DB
    loadConfigFromDb()

    result = getEventLogOfLastNHours(data_no_of_hours, CheckMoistureLevelEvent)
    data = [dict(eventTime=row[0],
                 eventAnalogValue=row[1]) for row in result]

    return render_template('dashboard.html', graph_no_of_hours=graph_no_of_hours, data_no_of_hours=data_no_of_hours,
                           data=data, isMobileRequest=isMobileRequest(request))


@app.route("/login", methods=['GET', 'POST'])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    form = LoginForm(csrf_enabled=True)

    if form.is_submitted():
        if form.validate():
            user = User.query.get(form.username.data)
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("/appConfig")
            else:
                return render_template("login.html", form=form, message="Invalid Login!!!")
        else:
            return render_template("login.html", form=form, message="Invalid Login!!!")
    else:
        return render_template("login.html", form=form)


@app.route("/appConfig", methods=['GET'])
@login_required
def appConfig():
    return render_template('appConfig.html', formTurnOnTap=TurnOnTapForm(csrf_enabled=True),
                           formAppConfig=loadAppConfigFormFromDB())


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect("/")


@app.route("/updateGraph", methods=["POST"])
@login_required
def updateGraph():
    plot_graph(True)
    return redirect("/dashboard")


@app.route("/updateData", methods=["POST"])
@login_required
def updateData():
    data = getLatestEventsData()
    return render_template('appConfig.html', formTurnOnTap=TurnOnTapForm(csrf_enabled=True),
                           formAppConfig=loadAppConfigFormFromDB(), data=data)


@app.route("/turnOnTap", methods=["POST"])
@login_required
def turnOnTap():
    form = TurnOnTapForm()
    message = None
    if form.validate_on_submit():
        seconds = form.secondsInFloat.data
        try:
            secondsInFloat = None if seconds is None else float(seconds)

            if secondsInFloat is not None and (secondsInFloat < 0 or secondsInFloat > 10):
                message = "Invalid value, enter value between 0 and 10"
            else:

                # Load configuration from DB
                loadConfigFromDb()

                result = turnOnWaterForCorrectSeconds(datetime.datetime.now(), secondsInFloat)
                if result:
                    message = "Plant Watered !!!"
                else:
                    message = "No enough water in container to water plant !!!"
        except ValueError:
            message = "Invalid input, Only float values accepted !!!"
    else:
        message = "Invalid operation !!!"

    return render_template('appConfig.html', formTurnOnTap=TurnOnTapForm(csrf_enabled=True),
                           formAppConfig=loadAppConfigFormFromDB(), message=message)


@app.route("/changeConfig", methods=["POST"])
@login_required
def changeConfig():
    form = AppConfigForm()

    if form.validate_on_submit():
        timestamp = datetime.datetime.now()

        updateConfigValue('EnableEmailNotifications', form.EnableEmailNotifications.data, timestamp)
        updateConfigValue('EnableSMSNotifications', form.EnableSMSNotifications.data, timestamp)
        updateConfigValue('EnablePumpFunctions', form.EnablePumpFunctions.data, timestamp)
        updateConfigValue('graph_no_of_hours', form.graph_no_of_hours.data, timestamp)
        updateConfigValue('data_no_of_hours', form.data_no_of_hours.data, timestamp)
        updateConfigValue('maxTimeToKeepPumpOnInSeconds', form.maxTimeToKeepPumpOnInSeconds.data, timestamp)
        updateConfigValue('timeToKeepPumpOnInSecondsForFullWaterCapacity',
                          form.timeToKeepPumpOnInSecondsForFullWaterCapacity.data, timestamp)

        return render_template('appConfig.html', formTurnOnTap=TurnOnTapForm(csrf_enabled=True),
                               formAppConfig=loadAppConfigFormFromDB())
    else:
        configErrorMessage = "Invalid data, varify the inputs !!!"
        return render_template('appConfig.html', formTurnOnTap=TurnOnTapForm(csrf_enabled=True),
                       formAppConfig=AppConfigForm(csrf_enabled=True), configErrorMessage=configErrorMessage)




def isMobileRequest(request):
    agent = request.headers.get('User-Agent')
    return any(phone in agent.lower() for phone in phones)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    context = (ssl_certfile_location, ssl_keyfile_location)
    logging.info(db)
    extra_dirs = ['./templates', './static']

    extra_files = extra_dirs[:]
    for extra_dir in extra_dirs:
        for dirname, dirs, files in os.walk(extra_dir):
            for filename in files:
                filename = path.join(dirname, filename)
                if path.isfile(filename):
                    extra_files.append(filename)

    app.run(host=server_host, port=server_port, ssl_context=context, debug=True, threaded=True, extra_files=extra_files)
