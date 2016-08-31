# Import required libraries
import time
from GPIOConfig import *
from dbFunctions import *
from EventNames import *

# ---------------------------------------------------------------------------------------------------------------------
# Function to get the distance of the water level from sensor
# ---------------------------------------------------------------------------------------------------------------------

def getDistance():

    sendTrigger()
    while GPIO.input(ProximityEchoPin) == 0:
        pulse_start = time.time()

    else:
        while GPIO.input(ProximityEchoPin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

    logging.info('Distance: ' + str(distance) + ' cms')
    return distance

# ---------------------------------------------------------------------------------------------------------------------
# Function to send trigger to sensor
# ---------------------------------------------------------------------------------------------------------------------

def sendTrigger():
    GPIO.output(ProximityTriggerPin, True)
    time.sleep(0.00001)
    GPIO.output(ProximityTriggerPin, False)


# ---------------------------------------------------------------------------------------------------------------------
# Function to get amount of water in container by using formula (container depth without water - current water level)
# ---------------------------------------------------------------------------------------------------------------------

def getWaterLevel():
    water_level_distance = getDistance()

    if water_level_distance < ContainerDepth:
        return ContainerDepth - water_level_distance
    else:
        return 0


# ---------------------------------------------------------------------------------------------------------------------
# Function to find out if container has water more than safety level
# ---------------------------------------------------------------------------------------------------------------------

def isEnoughWaterToOpenTap(eventTime):
    waterLevel = getWaterLevel()
    createEvent(CheckWaterLevelEvent, waterLevel, waterLevel >= WaterSafetyLevel, eventTime)
    water_percentage = (float(waterLevel)/float(ContainerDepth)) * 100.00
    return waterLevel >= WaterSafetyLevel , water_percentage

# ---------------------------------------------------------------------------------------------------------------------
