from flask import *
from dbFunctions import getEventLogOfLastNHours, getLatestEventsData
from GPIOConfig import data_no_of_hours, graph_no_of_hours, project_description
from WebAppConfig import *
from EventNames import CheckMoistureLevelEvent
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, set_login_view
from User import *
from Forms import LoginForm, TurnOnTapForm
from flask_bcrypt import Bcrypt
from GenerateGraph import plot_graph
from WaterPumpFunctions import turnOnWaterForCorrectSeconds
import datetime

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


@app.route("/")
def home():
    result = getEventLogOfLastNHours(data_no_of_hours, CheckMoistureLevelEvent)
    data = [dict(eventTime=row[0],
                 eventAnalogValue=row[1]) for row in result]

    return render_template('home.html', project_description=project_description,
                           isMobileRequest=isMobileRequest(request))


@app.route("/dashboard")
def dashboard():
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
    if form.validate_on_submit():
        user = User.query.get(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect("/appConfig")
        else:
            render_template("login.html", form=form, message="Invalid Login!!!")

    return render_template("login.html", form=form)


@app.route("/appConfig", methods=['GET'])
@login_required
def appConfig():
    return render_template('appConfig.html', formTurnOnTap=TurnOnTapForm(csrf_enabled=True))


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
    return render_template('appConfig.html', formTurnOnTap=TurnOnTapForm(csrf_enabled=True), data=data)


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
                result = turnOnWaterForCorrectSeconds(datetime.datetime.now(), secondsInFloat)
                if result:
                    message = "Plant Watered !!!"
                else:
                    message = "No enough water in container to water plant !!!"
        except ValueError:
            message = "Invalid input, Only float values accepted !!!"
    else:
        message = "Invalid operation !!!"

    return render_template('appConfig.html', formTurnOnTap=TurnOnTapForm(csrf_enabled=True), message=message)


def isMobileRequest(request):
    agent = request.headers.get('User-Agent')
    return any(phone in agent.lower() for phone in phones)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    context = (ssl_certfile_location, ssl_keyfile_location)
    print db
    app.run(host=server_host, port=server_port, ssl_context=context, debug=True, threaded=True)
