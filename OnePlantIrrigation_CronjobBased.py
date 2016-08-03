# ---------------------------------------------------------------------------------------------------------------------
# This is main file which will use all other utilities to detect the moisture and turn on the tap if moisture is less.
# This will also send email notifications about current status of the plant.
# ---------------------------------------------------------------------------------------------------------------------


from MoistureSensorFunctions import *
import sys
import traceback
import logging


# ---------------------------------------------------------------------------------------------------------------------
# Call this python file at scheduled intervals using cron job utility.
# ---------------------------------------------------------------------------------------------------------------------


try:
    # Setup GPIO for experiment
    setup_gpio()

    # Just call callback function which checks sensor, and does required actions.
    callback(MoisturePin)

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
