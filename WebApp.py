from flask import *
from dbFunctions import getEventLogOfLastNHours
from GPIOConfig import data_no_of_hours,graph_no_of_hours, maxTimeToKeepPumpOnInSeconds
from WebAppConfig import *
import logging
import traceback
from WaterPumpFunctions import turnOnWaterPumpForNSecondsStandAloneMode

app = Flask(__name__, static_url_path='')

@app.route("/moistureStatus")
def moistureStatus():
    result = getEventLogOfLastNHours(data_no_of_hours)
    data = [dict(eventTime=row[0],
                 eventAnalogValue=row[1]) for row in result]

    return render_template('index.html',graph_no_of_hours=graph_no_of_hours,data_no_of_hours=data_no_of_hours,data=data)

@app.route("/turnOnTap")
def turnOnTap():
    apiKey = request.args.get('apiKey')
    noOfSeconds = request.args.get('noOfSeconds')
    noOfSecondsAsFloat = 1.0

    try:
        noOfSecondsAsFloat = float(noOfSeconds)
    except:
        noOfSecondsAsFloat = 1.0
        logging.error(traceback.format_exc())

    if apiKey is None or turnOnTapApiKey != apiKey:
        message = 'Authentication failed, can not turn on tap!!!'
    else:
        if noOfSecondsAsFloat > maxTimeToKeepPumpOnInSeconds:
            noOfSecondsAsFloat = 1.0

        turnOnWaterPumpForNSecondsStandAloneMode(noOfSecondsAsFloat)
        message = "Plant watered for {0} seconds".format(str(noOfSecondsAsFloat))

    return render_template('turnOnTap.html',message=message)

if __name__ == "__main__":
    context = (ssl_certfile_location, ssl_keyfile_location)
    app.run(host=server_host, port=server_port, ssl_context=context, debug=True, threaded=True)
