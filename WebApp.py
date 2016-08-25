from flask import *
from dbFunctions import getEventLogOfLastNHours,getConfigValue
from GPIOConfig import data_no_of_hours, graph_no_of_hours, project_description
from WebAppConfig import *
from EventNames import CheckMoistureLevelEvent
from flask_login import LoginManager, login_required, login_user, logout_user, current_user,set_login_view
from User import *
from Forms import LoginForm
from flask_bcrypt import Bcrypt


app = Flask(__name__, static_url_path='')
login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)
app.secret_key=appSecretKey
with app.app_context():
    set_login_view("login")

dburi = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.format(dbUser, dbPass, dbHost, dbPort, dbSchema)
print dburi

app.config.__setitem__('SQLALCHEMY_DATABASE_URI',dburi)
app.config.__setitem__('SQLALCHEMY_TRACK_MODIFICATIONS',True)
db.init_app(app)

phones = ["iphone", "android", "blackberry"]



@app.route("/")
def home():
    result = getEventLogOfLastNHours(data_no_of_hours, CheckMoistureLevelEvent)
    data = [dict(eventTime=row[0],
                 eventAnalogValue=row[1]) for row in result]

    return render_template('home.html',project_description=project_description, isMobileRequest=isMobileRequest(request))



@app.route("/dashboard")
def dashboard():
    result = getEventLogOfLastNHours(data_no_of_hours, CheckMoistureLevelEvent)
    data = [dict(eventTime=row[0],
                 eventAnalogValue=row[1]) for row in result]

    return render_template('dashboard.html',graph_no_of_hours=graph_no_of_hours,data_no_of_hours=data_no_of_hours,data=data, isMobileRequest=isMobileRequest(request))




@app.route("/login", methods=['GET','POST'])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    print db
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
    return render_template('appConfig.html', message="Valid API Key")


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



def isMobileRequest(request):
    agent = request.headers.get('User-Agent')
    return any(phone in agent.lower() for phone in phones)


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


if __name__ == "__main__":
    context = (ssl_certfile_location, ssl_keyfile_location)
    app.run(host=server_host, port=server_port, ssl_context=context, debug=True, threaded=True)
    print db


