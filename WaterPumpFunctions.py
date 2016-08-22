from GPIOConfig import *
import sys


def turnOnWaterPumpForNSeconds(secondsInFloat, eventTime):
    GPIO.output(WaterPumpPin, True)
    time.sleep(secondsInFloat)
    GPIO.output(WaterPumpPin, False)
    createEvent(WaterPlantEvent, secondsInFloat, True, eventTime)


def turnOnWaterPumpForNSecondsStandAloneMode(secondsInFloat):

    try:
        # Setup GPIO for experiment
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(WaterPumpPin, GPIO.OUT)

        #turnOnWaterPumpForNSeconds(secondsInFloat)

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
