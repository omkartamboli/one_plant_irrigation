# ---------------------------------------------------------------------------------------------------------------------
# This file contains all GPIO pin configurations used in this experiment.
# You can change this file to match your pin settings.
# ---------------------------------------------------------------------------------------------------------------------

import RPi.GPIO as GPIO
from dbFunctions import *


# ---------------------------------------------------------------------------------------------------------------------
# GPIO pins used for stepper motor in the sequence IN1, IN2, IN3, IN4
# ---------------------------------------------------------------------------------------------------------------------
StepPins = [22, 23, 24, 25]


# ---------------------------------------------------------------------------------------------------------------------
# GPIO pin used by moisture sensor for detecting moisture level
# ---------------------------------------------------------------------------------------------------------------------
MoisturePin = 17


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
EnableSMSNotifications = True


# ---------------------------------------------------------------------------------------------------------------------
# Empty water container depth in cms, this will be used to detect actual water level
# ---------------------------------------------------------------------------------------------------------------------
ContainerDepth = 30


# ---------------------------------------------------------------------------------------------------------------------
# PLEASE NOTE:
# Don't change code beyond this line, following part contains util methods used by other files
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# Util method to setup GPIO for experiment
# ---------------------------------------------------------------------------------------------------------------------

def setup_gpio():
    setupGPIOForStepperMotor(StepPins)

    # Set Moisture sensor pin as input
    GPIO.setup(MoisturePin, GPIO.IN)

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
    if EnableEmailNotifications and statusType != getLatestEventEmailNotification():
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