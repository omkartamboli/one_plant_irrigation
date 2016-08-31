# ---------------------------------------------------------------------------------------------------------------------
# This is main file which will use all other utilities to detect the moisture and turn on the tap if moisture is less
# This will also send email notifications about current status of the plant
# ---------------------------------------------------------------------------------------------------------------------


from MoistureSensorFunctions import *
import sys
import traceback
import logging

# Setup GPIO for experiment
setup_gpio()

# # This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
# GPIO.add_event_detect(MoisturePin, GPIO.BOTH, bouncetime=300)
#
# # This line assigns a function to the GPIO pin so that when the above line tells us there is a change on the pin,
# # run this function
# GPIO.add_event_callback(MoisturePin, callback)


try:
    # This is an infinite loop to keep our script running
    while True:
        # This line simply tells our script to wait few seconds, this is so the script doesnt hog all of the CPU
        time.sleep(15)

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
