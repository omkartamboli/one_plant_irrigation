from flask import *
from dbFunctions import getEventLogOfLastNHours,getConfigValue
from GPIOConfig import data_no_of_hours,graph_no_of_hours
from WebAppConfig import *
from EventNames import CheckMoistureLevelEvent
from flask.ext.login import LoginManager,login_required,set_login_view
from User import *


app = Flask(__name__, static_url_path='')
login_manager = LoginManager()

login_manager.init_app(app)
set_login_view("login")


phones = ["iphone", "android", "blackberry"]

@app.route("/moistureStatus")
def moistureStatus():
    result = getEventLogOfLastNHours(data_no_of_hours, CheckMoistureLevelEvent)
    data = [dict(eventTime=row[0],
                 eventAnalogValue=row[1]) for row in result]

    return render_template('index.html',graph_no_of_hours=graph_no_of_hours,data_no_of_hours=data_no_of_hours,data=data, isMobileRequest=isMobileRequest(request))




@app.route("/login", methods=['GET','POST'])
def login():
    return

@app.route("/appConfig", methods=['GET'])
@login_required
def appConfig():
    return render_template('appConfig.html', message="Valid API Key")





def isMobileRequest(request):
    agent = request.headers.get('User-Agent')
    return any(phone in agent.lower() for phone in phones)


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


@app.route("/validate", methods=['GET'])
def validate_get():
    return render_template('validate.html')


@app.route("/validate", methods=['POST'])
def validate_post():
    _apiKey = request.form['apiKey']

    if _apiKey is None:
        print "form api key is null"
        return render_template('validate.html', message="Invalid API Key")

    apiKeyConfig = getConfigValue("viewConfigApiKey")

    if apiKeyConfig is None:
        print "db api key is null"
        return render_template('validate.html', message="Invalid API Key")

    # validate the received values
    if _apiKey == apiKeyConfig:
        return render_template('appConfig.html', message="Valid API Key")
    else:
        return render_template('validate.html', message="Invalid API Key")


if __name__ == "__main__":
    context = (ssl_certfile_location, ssl_keyfile_location)
    app.run(host=server_host, port=server_port, ssl_context=context, debug=True, threaded=True)
