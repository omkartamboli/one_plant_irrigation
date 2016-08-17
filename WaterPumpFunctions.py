from GPIOConfig import *
import sys


def turnOnWaterPumpForNSeconds(secondsInFloat):
    GPIO.output(WaterPumpPin, True)
    time.sleep(secondsInFloat)
    GPIO.output(WaterPumpPin, False)


# Standard boilerplate to call the main() function to begin the program.
if __name__ == '__main__':
    try:
        # Setup GPIO for experiment
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(WaterPumpPin, GPIO.OUT)

        timeToKeepPumpOn = 1

        if len(sys.argv) > 1:
            newTime = float(sys.argv[1])
            if newTime > 0:
                timeToKeepPumpOn = newTime

        turnOnWaterPumpForNSeconds(timeToKeepPumpOn)

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
