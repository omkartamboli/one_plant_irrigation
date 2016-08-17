from flask import *
from dbFunctions import getEventLogOfLastNHours
from GPIOConfig import data_no_of_hours,graph_no_of_hours
from WebAppConfig import *

app = Flask(__name__, static_url_path='')

@app.route("/moistureStatus")
def moistureStatus():
    result = getEventLogOfLastNHours(data_no_of_hours)
    data = [dict(eventTime=row[0],
                 eventAnalogValue=row[1]) for row in result]

    return render_template('index.html',graph_no_of_hours=graph_no_of_hours,data_no_of_hours=data_no_of_hours,data=data)


if __name__ == "__main__":
    context = (ssl_certfile_location, ssl_keyfile_location)
    app.run(host=server_host, port=server_port, ssl_context=context, debug=True, threaded=True)
