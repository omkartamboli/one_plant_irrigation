# Import required libraries
import time
from GPIOConfig import *

# ------------------------------------------------------------------------------------------------------------------------

# Define GPIO signals to use

speed = [0.008, 0.004, 0.002, 0.001]
oneCycleCount = 512


# ------------------------------------------------------------------------------------------------------------------------

def resetAllPins(StepPins):
    # Set all pins to false
    for pin in StepPins:
        GPIO.output(pin, False)


# ------------------------------------------------------------------------------------------------------------------------

def get_speed_very_slow():
    return speed[0]


# ------------------------------------------------------------------------------------------------------------------------

def get_speed_slow():
    return speed[1]


# ------------------------------------------------------------------------------------------------------------------------

def get_speed_medium():
    return speed[2]


# ------------------------------------------------------------------------------------------------------------------------

def get_speed_fast():
    return speed[3]


# ------------------------------------------------------------------------------------------------------------------------

def rotateMotorClockWise(speedForRotation, numberOfCycles):
    mainloopcounter = 0
    totalCount = numberOfCycles * oneCycleCount
    resetAllPins(StepPins)
    # Start main loop
    while True:

        GPIO.output(StepPins[0], True)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], True)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], True)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], True)
        GPIO.output(StepPins[1], True)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], True)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], True)
        GPIO.output(StepPins[2], True)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], True)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], True)
        GPIO.output(StepPins[3], True)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], True)
        time.sleep(speedForRotation)

        mainloopcounter += 1

        if (mainloopcounter > totalCount):
            break


# ------------------------------------------------------------------------------------------------------------------------

def rotateMotorAntiClockWise(speedForRotation, numberOfCycles):
    mainloopcounter = 0
    totalCount = numberOfCycles * oneCycleCount
    resetAllPins(StepPins)
    # Start main loop
    while True:

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], True)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], True)
        GPIO.output(StepPins[3], True)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], True)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], True)
        GPIO.output(StepPins[2], True)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], False)
        GPIO.output(StepPins[1], True)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], True)
        GPIO.output(StepPins[1], True)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], True)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], False)
        time.sleep(speedForRotation)

        GPIO.output(StepPins[0], True)
        GPIO.output(StepPins[1], False)
        GPIO.output(StepPins[2], False)
        GPIO.output(StepPins[3], True)
        time.sleep(speedForRotation)

        mainloopcounter += 1

        if (mainloopcounter > totalCount):
            break

# ------------------------------------------------------------------------------------------------------------------------
