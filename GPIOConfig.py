# ---------------------------------------------------------------------------------------------------------------------
# This file contains all GPIO pin configurations used in this experiment.
# You can change this file to match your pin settings.
# ---------------------------------------------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import Adafruit_MCP3008
from dbFunctions import *
from EventNames import *


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
ProximityTriggerPin = 11


# ---------------------------------------------------------------------------------------------------------------------
# GPIO pin used by proximity sensor for detecting water level in container
# ---------------------------------------------------------------------------------------------------------------------
ProximityEchoPin = 13


# ---------------------------------------------------------------------------------------------------------------------
# Configuration to enable / disable email notifications
# ---------------------------------------------------------------------------------------------------------------------
EnableEmailNotifications = True


# ---------------------------------------------------------------------------------------------------------------------
# Configuration to enable / disable sms notifications
# ---------------------------------------------------------------------------------------------------------------------
EnableSMSNotifications = False


# ---------------------------------------------------------------------------------------------------------------------
# Empty water container depth in cms, this will be used to detect actual water level
# ---------------------------------------------------------------------------------------------------------------------
ContainerDepth = 30


# ---------------------------------------------------------------------------------------------------------------------
# Analog input channels for moisture sensors
# ---------------------------------------------------------------------------------------------------------------------
Moisture_ADC_Channels = [0,1]


# ---------------------------------------------------------------------------------------------------------------------
# Analog input channels for moisture sensors
# ---------------------------------------------------------------------------------------------------------------------
Moisture_Low_Value = float(200.00)


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
timeToKeppPumpOnInSeconds = 3


# ---------------------------------------------------------------------------------------------------------------------
# Web App Max Time to keep pump on in seconds
# ---------------------------------------------------------------------------------------------------------------------
maxTimeToKeepPumpOnInSeconds = float(5.0)


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
        print "Setting up pin ", pin
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)


# ---------------------------------------------------------------------------------------------------------------------
# Util method to clean up  GPIO after experiment
# ---------------------------------------------------------------------------------------------------------------------

def cleanupGPIO():
    print "Cleaning up IO ..."
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
