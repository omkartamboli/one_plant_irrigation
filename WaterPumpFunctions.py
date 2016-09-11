from GPIOConfig import *
import sys
import datetime
from ProximitySensorFunctions import isEnoughWaterToOpenTap


def turnOnWaterPumpForNSeconds(secondsInFloat, eventTime, waterPin):
    GPIO.output(waterPin, True)
    time.sleep(secondsInFloat)
    GPIO.output(waterPin, False)

    logging.info("turnOnWaterPumpForNSeconds-> Pump was on for {0} seconds, at {1}".format(secondsInFloat, eventTime))

    if (eventTime is not None):
        createEvent(WaterPlantEvent, secondsInFloat, True, eventTime)


def turnOnWaterPumpForNSecondsStandAloneMode(secondsInFloat, waterPin):
    try:
        # Setup GPIO for experiment
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(waterPin, GPIO.OUT)

        turnOnWaterPumpForNSeconds(secondsInFloat, None, waterPin)

    except KeyboardInterrupt:
        logging.error("Program terminated on user interrupt.")

    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    except:
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise

    finally:
        cleanupGPIO()


def turnOnRefillWaterPumpForNSecondsStandAloneMode(secondsInFloat):
    turnOnWaterPumpForNSecondsStandAloneMode(secondsInFloat, RefillWaterPumpPin)


def turnOnWaterForCorrectSeconds(eventTime, overrideSeconds):
    if eventTime is None:
        eventTime = datetime.datetime.now()

    setupGPIOForProximitySensor()

    enoughWater, water_percentage = isEnoughWaterToOpenTap(eventTime)

    if enoughWater:

        # Setup GPIO for experiment
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(WaterPumpPin, GPIO.OUT)

        if overrideSeconds is None:
            timeToKeepPumpOn = timeToKeepPumpOnInSecondsForFullWaterCapacity + ((100.00 - water_percentage) * 0.05)
            turnOnWaterPumpForNSeconds(timeToKeepPumpOn, eventTime, WaterPumpPin)
            logging.info("Plant watered for {0} seconds".format(timeToKeepPumpOn))
        else:
            turnOnWaterPumpForNSeconds(overrideSeconds, eventTime, WaterPumpPin)
            logging.info("Plant watered for {0} seconds".format(overrideSeconds))

    return enoughWater


# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    try:
        timeToKeepPumpOn = 1

        if len(sys.argv) > 1:
            newTime = float(sys.argv[1])
            if newTime > 0:
                timeToKeepPumpOn = newTime

        turnOnWaterPumpForNSecondsStandAloneMode(timeToKeepPumpOn, WaterPumpPin)

    except KeyboardInterrupt:
        logging.error("Program terminated on user interrupt.")

    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(e.__doc__)
        logging.error(e.message)

    except:
        logging.error("Unexpected error:", sys.exc_info()[0])
        raise
