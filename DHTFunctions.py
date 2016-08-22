from GPIOConfig import *

import Adafruit_DHT


def getTemperatureAndHumidity():
    return Adafruit_DHT.read_retry(DHT_Sensor_Type, DhtDataPin)


def recordTemperatureAndHumidity(eventTime):
    humidity, temperature = getTemperatureAndHumidity()

    if humidity is not None:
        createEvent(CheckHumidityEvent, humidity, True, eventTime)
    if temperature is not None:
        createEvent(CheckTemperatureEvent, temperature, True, eventTime)
