# ---------------------------------------------------------------------------------------------------------------------
# This file contains all GPIO pin configurations used in this experiment.
# You can change this file to match your pin settings.
# ---------------------------------------------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import Adafruit_MCP3008
from dbFunctions import *
from EventNames import *
import datetime

# ---------------------------------------------------------------------------------------------------------------------
# GPIO pins used for stepper motor in the sequence IN1, IN2, IN3, IN4
# ---------------------------------------------------------------------------------------------------------------------
StepPins = [22, 23, 24, 25]

# ---------------------------------------------------------------------------------------------------------------------
# GPIO pin used by water pump
# ---------------------------------------------------------------------------------------------------------------------
WaterPumpPin = 22

# ---------------------------------------------------------------------------------------------------------------------
# GPIO pin used by proximity sensor for triggering the sensor
# ---------------------------------------------------------------------------------------------------------------------
ProximityTriggerPin = 21

# ---------------------------------------------------------------------------------------------------------------------
# GPIO pin used by proximity sensor for detecting water level in container
# ---------------------------------------------------------------------------------------------------------------------
ProximityEchoPin = 26

# ---------------------------------------------------------------------------------------------------------------------
# GPIO pin used by DHT11 sensor for detecting temperature and humidity
# ---------------------------------------------------------------------------------------------------------------------
DhtDataPin = 12

# ---------------------------------------------------------------------------------------------------------------------
# DHT sensor type
# ---------------------------------------------------------------------------------------------------------------------

DHT_Sensor_Type = 11

# ---------------------------------------------------------------------------------------------------------------------
# Configuration to enable / disable email notifications
# ---------------------------------------------------------------------------------------------------------------------
EnableEmailNotifications = True

# ---------------------------------------------------------------------------------------------------------------------
# Configuration to enable / disable sms notifications
# ---------------------------------------------------------------------------------------------------------------------
EnableSMSNotifications = False

# ---------------------------------------------------------------------------------------------------------------------
# Configuration to enable / disable water pump functions
# ---------------------------------------------------------------------------------------------------------------------
EnablePumpFunctions = True

# ---------------------------------------------------------------------------------------------------------------------
# Empty water container depth in cms, this will be used to detect actual water level
# ---------------------------------------------------------------------------------------------------------------------
ContainerDepth = float(18.00)

# ---------------------------------------------------------------------------------------------------------------------
# Water safety level is set to 2 cms, if container has less than 2 cms of water then tap will not open
# ---------------------------------------------------------------------------------------------------------------------

WaterSafetyLevel = float(3.00)

# ---------------------------------------------------------------------------------------------------------------------
# Analog input channels for moisture sensors
# ---------------------------------------------------------------------------------------------------------------------
Moisture_ADC_Channels = [0, 1]

# ---------------------------------------------------------------------------------------------------------------------
# Moisture off set value for graphs
# ---------------------------------------------------------------------------------------------------------------------
Moisture_Offset_Value = float(100.00)

# ---------------------------------------------------------------------------------------------------------------------
# Critical value for moisture
# ---------------------------------------------------------------------------------------------------------------------
Moisture_Low_Value = (float(200.00) - Moisture_Offset_Value)

# ---------------------------------------------------------------------------------------------------------------------
# Critical value for water in container
# ---------------------------------------------------------------------------------------------------------------------
Water_Low_Value_Percentage = (WaterSafetyLevel / ContainerDepth) * 100

# ---------------------------------------------------------------------------------------------------------------------
# Software SPI configuration:
# ---------------------------------------------------------------------------------------------------------------------
CLK = 18
MISO = 23
MOSI = 24
CS = 25

# Set ADC variables
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# ---------------------------------------------------------------------------------------------------------------------
# configuration to generate graph for last how many number of hours
# ---------------------------------------------------------------------------------------------------------------------
graph_no_of_hours = 120

# ---------------------------------------------------------------------------------------------------------------------
# configuration to generate data for last how many number of hours
# ---------------------------------------------------------------------------------------------------------------------
data_no_of_hours = 1

# ---------------------------------------------------------------------------------------------------------------------
# Time to keep pump on in seconds
# ---------------------------------------------------------------------------------------------------------------------
timeToKeepPumpOnInSecondsForFullWaterCapacity = 1

# ---------------------------------------------------------------------------------------------------------------------
# Web App Max Time to keep pump on in seconds
# ---------------------------------------------------------------------------------------------------------------------
maxTimeToKeepPumpOnInSeconds = float(5.0)

project_description = """
<p>
<br/>

This is automated irrigation system for one plant.

<br/>
</p>
<p>
<br/>

The aim of the project is to water the plant on need basis, not based on schedule.
Soil moisture sensors record the soil moisture regularly and note the readings.
Pi performs the analysis of the moisture data and triggers the water motor when moisture level goes down certain value.
DHT11 sensor records the current temperature and relative humidity.
Proximity sensor is placed on top of water container, which monitors the water level in container.

<br/>
</p>
<p>
<br/>

Plotly graphs are integrated to show trends of moisture, humidity, temperature, and current water level in the container.
It also displays the moisture low reference line, water level critical line and water release events.

<br/>
</p>
<p>
<br/>

Twilio APIs are integrated to send SMS notifications when moisture level falls below critical value, water container
has less water, and when moisture is restored back. Also standard email APIs are integrated to send emails
for these events.

<br/>
</p>
<p>
<br/>

The Project is built using Raspberry Pi, soil moisture sensors, humidity and temperature sensor (DHT11),
Proximity sensor (HC-SR04), and other supporting elements.

<br/>
</p>
<p>
<br/>

For more information reach me at omkarjava0103@gmail.com

<br/>
</p>
"""



# ---------------------------------------------------------------------------------------------------------------------
# PLEASE NOTE:
# Don't change code beyond this line, following part contains util methods used by other files
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
# Util method to setup GPIO for experiment
# ---------------------------------------------------------------------------------------------------------------------

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    # setupGPIOForStepperMotor(StepPins) -- Not using stepper motor now

    # Set water pump pin as output
    GPIO.setup(WaterPumpPin, GPIO.OUT)

    setupGPIOForProximitySensor()

    # Set DhtDataPin as input
    GPIO.setup(DhtDataPin, GPIO.IN)


# ---------------------------------------------------------------------------------------------------------------------
# Util method to setup GPIO for Proximity Sensor
# ---------------------------------------------------------------------------------------------------------------------

def setupGPIOForProximitySensor():
    GPIO.setmode(GPIO.BCM)

    # Set Proximity sensor trigger pin as output
    GPIO.setup(ProximityTriggerPin, GPIO.OUT)

    # Set Proximity sensor echo pin as input
    GPIO.setup(ProximityEchoPin, GPIO.IN)

    # Set ProximityTriggerPin to false before we start the experiment
    GPIO.output(ProximityTriggerPin, False)


# ---------------------------------------------------------------------------------------------------------------------
# Util method to setup GPIO for Stepper Motor
# ---------------------------------------------------------------------------------------------------------------------

def setupGPIOForStepperMotor(StepPins):
    # Use BCM GPIO references
    # instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)

    # Set all stepper motor pins as output
    for pin in StepPins:
        logging.info("Setting up pin ", pin)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)


# ---------------------------------------------------------------------------------------------------------------------
# Util method to clean up  GPIO after experiment
# ---------------------------------------------------------------------------------------------------------------------

def cleanupGPIO():
    logging.info("Cleaning up IO ...")
    GPIO.cleanup()


# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------

def shouldSendEmail(statusType):
    if EnableEmailNotifications and (statusType != getLatestEventEmailNotification() or
                                             MoistureLevelLowStatus == statusType or
                                             MoistureLevelLowAndWaterLevelLowStatus == statusType):
        createEventNotification(statusType, True, False)
        return True
    else:
        return False


# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------

def shouldSendSMS(statusType):
    if EnableSMSNotifications and statusType != getLatestEventSMSNotification():
        createEventNotification(statusType, False, True)
        return True
    else:
        return False

# Load configuration from DB
def getOrSetValueFromDB(propertyName, currentValue):
    value = getConfigValue(propertyName)
    if value is None:
        updateConfigValue(propertyName,currentValue,datetime.datetime.now())
        return currentValue
    else:
        return value


EnableEmailNotifications = str(getOrSetValueFromDB('EnableEmailNotifications',EnableEmailNotifications))
EnableSMSNotifications = str(getOrSetValueFromDB('EnableSMSNotifications',EnableSMSNotifications))
EnablePumpFunctions = str(getOrSetValueFromDB('EnablePumpFunctions',EnablePumpFunctions))
data_no_of_hours = int(getOrSetValueFromDB('data_no_of_hours',data_no_of_hours))
graph_no_of_hours = int(getOrSetValueFromDB('graph_no_of_hours',graph_no_of_hours))
maxTimeToKeepPumpOnInSeconds = float(getOrSetValueFromDB('maxTimeToKeepPumpOnInSeconds',maxTimeToKeepPumpOnInSeconds))
timeToKeepPumpOnInSecondsForFullWaterCapacity = float(getOrSetValueFromDB(
    'timeToKeepPumpOnInSecondsForFullWaterCapacity',timeToKeepPumpOnInSecondsForFullWaterCapacity))


