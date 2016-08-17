import plotly.plotly as py
import plotly.graph_objs as go
from GPIOConfig import graph_no_of_hours, Moisture_Low_Value
from dbFunctions import *
from GraphConfig import *


def plot_graph(isOnline):
    result = getEventLogOfLastNHours(graph_no_of_hours)

    try:
        if result is not None:

            i = 0
            x1 = [None] * len(result)
            x2 = [None] * len(result)
            y1 = [None] * len(result)
            y2 = [None] * len(result)
            for row in result:
                x1[i] = row[0]
                x2[i] = i
                y1[i] = float(row[1])
                y2[i] = Moisture_Low_Value
                i += 1

            trace1 = go.Scatter(
                x=x1,
                y=y1,
                name="Moisture data for last {0} hours".format(str(graph_no_of_hours)),
                text="Moisture data for last {0} hours".format(str(graph_no_of_hours)),
                hoverinfo="Moisture data for last {0} hours".format(str(graph_no_of_hours)),
                line=dict(shape='linear', color='rgb(0, 255, 0)')
            )

            trace2 = go.Scatter(
                x=x1,
                y=y2,
                name='Moisture Low reference line',
                text='Moisture Low reference line',
                hoverinfo='Moisture Low reference line',
                line=dict(color='rgb(255, 0, 0)', width=1, dash='dot')
            )

            data = [trace1, trace2]
            layout = dict(
                legend=dict(
                    y=5,
                    traceorder='reversed',
                    font=dict(
                        size=16
                    )
                )
            )

            fig = dict(data=data, layout=layout)
            py.sign_in(plotly_username, plotly_api_key)

            if isOnline:
                print "Plotting online graph"
                py.plot(fig, filename='line-shapes')

            else:
                print "Plotting offline graph"

            py.image.save_as(fig, "./static/graph.png")

        else:
            logging.warn("No Event log data for last {0} hours".format(str(graph_no_of_hours)))

    except Exception as e:
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message
        print "Some exception while creating graph for last {0} hours".format(str(graph_no_of_hours))

    except:
        logging.error(traceback.format_exc())
        print "Some exception while creating graph for last {0} hours".format(str(graph_no_of_hours))

if __name__ == "__main__":
    plot_graph(True)
