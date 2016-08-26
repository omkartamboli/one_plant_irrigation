from GPIOConfig import *
import sys
import datetime
from ProximitySensorFunctions import isEnoughWaterToOpenTap

def turnOnWaterPumpForNSeconds(secondsInFloat, eventTime):
    GPIO.output(WaterPumpPin, True)
    time.sleep(secondsInFloat)
    GPIO.output(WaterPumpPin, False)
    if(eventTime is not None):
        createEvent(WaterPlantEvent, secondsInFloat, True, eventTime)


def turnOnWaterPumpForNSecondsStandAloneMode(secondsInFloat):

    try:
        # Setup GPIO for experiment
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(WaterPumpPin, GPIO.OUT)

        turnOnWaterPumpForNSeconds(secondsInFloat, None)

    except KeyboardInterrupt:
        print "Program terminated on user interrupt."

    except Exception as e:
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        cleanupGPIO()

def turnOnWaterForCorrectSeconds(eventTime, overrideSeconds):

    if eventTime is None:
        eventTime = datetime.datetime.now()

    enoughWater, water_percentage = isEnoughWaterToOpenTap(eventTime)

    if enoughWater:
        if overrideSeconds is None:
            timeToKeepPumpOn = timeToKeepPumpOnInSecondsForFullWaterCapacity + ((100.00 - water_percentage) * 0.1)
            turnOnWaterPumpForNSeconds(timeToKeepPumpOn, eventTime)
        else:
            turnOnWaterPumpForNSeconds(overrideSeconds, eventTime)

    return enoughWater


# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    try:
        timeToKeepPumpOn = 1

        if len(sys.argv) > 1:
            newTime = float(sys.argv[1])
            if newTime > 0:
                timeToKeepPumpOn = newTime

        turnOnWaterPumpForNSecondsStandAloneMode(timeToKeepPumpOn)

    except KeyboardInterrupt:
        print "Program terminated on user interrupt."

    except Exception as e:
        logging.error(traceback.format_exc())
        print e.__doc__
        print e.message

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
