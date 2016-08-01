# Import required libraries
from StepperFunctions import *

# Setup GPIO mode and pins's mode
setupGPIO(StepPins)

try:
    rotateMotorClockWise(get_speed_fast(), 1)
    time.sleep(0.2)
    rotateMotorAntiClockWise(get_speed_fast(), 1)
    time.sleep(1)

    rotateMotorClockWise(get_speed_fast(), 2)
    time.sleep(0.2)
    rotateMotorAntiClockWise(get_speed_fast(), 2)
    time.sleep(1)

    rotateMotorClockWise(get_speed_medium(), 1)
    time.sleep(0.2)
    rotateMotorAntiClockWise(get_speed_medium(), 1)
    time.sleep(1)

    rotateMotorClockWise(get_speed_slow(), 1)
    time.sleep(0.2)
    rotateMotorAntiClockWise(get_speed_slow(), 1)
    time.sleep(1)

    rotateMotorClockWise(get_speed_very_slow(), 1)
    time.sleep(0.2)
    rotateMotorAntiClockWise(get_speed_very_slow(), 1)
    time.sleep(1)

except KeyboardInterrupt:
    print "Program terminated on user interrupt"

finally:
    cleanupGPIO()
