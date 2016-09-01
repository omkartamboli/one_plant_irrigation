import plotly.plotly as py
import plotly.graph_objs as go
from GPIOConfig import graph_no_of_hours, Moisture_Low_Value, Water_Low_Value_Percentage, ContainerDepth, getOrSetValueFromDB
from dbFunctions import *
from GraphConfig import *
from EventNames import *


def plot_graph(isOnline):

    graph_no_of_hours_val = int(getOrSetValueFromDB('graph_no_of_hours', graph_no_of_hours))

    result1 = getEventLogOfLastNHours(graph_no_of_hours_val, CheckMoistureLevelEvent)
    result2 = getEventLogOfLastNHours(graph_no_of_hours_val, WaterPlantEvent)
    result3 = getEventLogOfLastNHours(graph_no_of_hours_val, CheckTemperatureEvent)
    result4 = getEventLogOfLastNHours(graph_no_of_hours_val, CheckHumidityEvent)
    result5 = getEventLogOfLastNHours(graph_no_of_hours_val, CheckWaterLevelEvent)

    trace0 = None
    trace00 = None
    trace1 = None
    trace2 = None
    trace3 = None
    trace4 = None
    trace5 = None

    try:
        if result1 is not None:

            i = 0
            x1 = [None] * len(result1)
            y1 = [None] * len(result1)
            y0 = [None] * len(result1)
            for row in result1:
                x1[i] = row[0]
                y1[i] = float(row[1])
                y0[i] = Moisture_Low_Value
                i += 1

            trace0 = go.Scatter(
                x=x1,
                y=y0,
                name='Moisture low reference line',
                text='Moisture low reference line',
                hoverinfo='Moisture low reference line',
                line=dict(color='rgb(255, 0, 0)', width=1, dash='dot')
            )

            trace1 = go.Scatter(
                x=x1,
                y=y1,
                name="Soil Moisture",
                text="Soil Moisture",
                hoverinfo="Soil Moisture",
                line=dict(shape='spline', color='rgb(0, 255, 0)')
            )

        if result2 is not None:
            j = 0
            x2 = [None] * len(result2)
            y2 = [None] * len(result2)
            z2 = [None] * len(result2)

            for row2 in result2:
                x2[j] = row2[0]
                y2[j] = Moisture_Low_Value + 10
                z2[j] = float(row2[1])*1.5
                j += 1


            trace2 = go.Scatter(
                x=x2,
                y=y2,
                name='Water Release Events',
                text='Water Release Events',
                hoverinfo='Water Release Events',
                mode='markers',
                marker=dict(
                    color='rgb(0, 0, 255)',
                    size=z2
                )
            )

        if result3 is not None:
            k = 0
            x3 = [None] * len(result3)
            y3 = [None] * len(result3)

            for row3 in result3:
                x3[k] = row3[0]
                y3[k] = float(row3[1])
                k += 1

            trace3 = go.Scatter(
                x=x3,
                y=y3,
                name="Temperature Celsius",
                text="Temperature Celsius",
                hoverinfo="Temperature Celsius",
                line=dict(shape='spline', color='rgb(255,99,71)')
            )

        if result4 is not None:
            l = 0
            x4 = [None] * len(result4)
            y4 = [None] * len(result4)

            for row4 in result4:
                x4[l] = row4[0]
                y4[l] = float(row4[1])
                l += 1

            trace4 = go.Scatter(
                x=x4,
                y=y4,
                name="Humidity %",
                text="Humidity %",
                hoverinfo="Humidity %",
                line=dict(shape='spline', color='rgb(148, 0, 211)')
            )

        if result5 is not None:

            m = 0

            x5 = [None] * len(result5)
            y5 = [None] * len(result5)
            y00 = [None] * len(result5)
            for row5 in result5:
                x5[m] = row5[0]
                y5[m] = (float(row5[1]) / ContainerDepth) * 100
                y00[m] = Water_Low_Value_Percentage
                m += 1

            trace00 = go.Scatter(
                x=x5,
                y=y00,
                name='Water low reference line',
                text='Water low reference line',
                hoverinfo='Water low reference line',
                line=dict(color='rgb(0, 0, 255)', width=1, dash='dot')
            )

            trace5 = go.Scatter(
                x=x5,
                y=y5,
                name="Container Water %",
                text="Container Water %",
                hoverinfo="Container Water %",
                line=dict(shape='spline', color='rgb(0,191,255)')
            )


        if result2 is not None and len(result2) > 0:
            data = [trace0, trace00, trace1, trace2, trace3, trace4, trace5]
        else:
            data = [trace0, trace00, trace1, trace3, trace4, trace5]

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
            logging.info("Plotting online graph")
            py.plot(fig, filename='OnePlantIrrigation')

        else:
            logging.info("Plotting offline graph")

        py.image.save_as(fig, "./static/graph.png")

    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)
        logging.error("Some exception while creating graph for last {0} hours".format(str(graph_no_of_hours_val)))

    except:
        logging.error(traceback.format_exc())
        logging.error("Some exception while creating graph for last {0} hours".format(str(graph_no_of_hours_val)))


if __name__ == "__main__":
    plot_graph(True)
