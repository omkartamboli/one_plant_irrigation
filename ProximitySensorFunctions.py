# Import required libraries
import time
from GPIOConfig import *
from dbFunctions import *
from EventNames import *

# ---------------------------------------------------------------------------------------------------------------------
# Water safety level is set to 2 cms, if container has less than 2 cms of water then tap will not open
# ---------------------------------------------------------------------------------------------------------------------

WaterSafetyLevel = 2


# ---------------------------------------------------------------------------------------------------------------------
# Function to get the distance of the water level from sensor
# ---------------------------------------------------------------------------------------------------------------------

def getDistance(ProximityEchoPin):

    start_time = time.time()
    breakPulseForStart = start_time + 2.01
    distance = None

    while GPIO.input(ProximityEchoPin) == 0:
        pulse_start = time.time()
        if pulse_start > breakPulseForStart:
            break

    if pulse_start - start_time > 2:
        distance = 1000

    else:
        while GPIO.input(ProximityEchoPin) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)

    print ('Distance: ' + str(distance) + ' cm')
    return distance

# ---------------------------------------------------------------------------------------------------------------------
# Function to send trigger to sensor
# ---------------------------------------------------------------------------------------------------------------------

def sendTrigger(ProximityTriggerPin):
    GPIO.output(ProximityTriggerPin, True)
    time.sleep(0.00001)
    GPIO.output(ProximityTriggerPin, False)


# ---------------------------------------------------------------------------------------------------------------------
# Function to get amount of water in container by using formula (container depth without water - current water level)
# ---------------------------------------------------------------------------------------------------------------------

def getWaterLevel():
    sendTrigger(ProximityTriggerPin)
    water_level_distance = getDistance(ProximityEchoPin)

    if water_level_distance < ContainerDepth:
        return ContainerDepth - water_level_distance
    else:
        return 0


# ---------------------------------------------------------------------------------------------------------------------
# Function to find out if container has water more than safety level
# ---------------------------------------------------------------------------------------------------------------------

def isEnoughWaterToOpenTap():
    waterLevel = getWaterLevel()
    createEvent(CheckWaterLevelEvent, waterLevel, waterLevel >= WaterSafetyLevel)
    return waterLevel >= WaterSafetyLevel

# ---------------------------------------------------------------------------------------------------------------------
