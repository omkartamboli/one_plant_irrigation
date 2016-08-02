# Import required libraries
from EmailFunctions import *
from StepperFunctions import *


# ---------------------------------------------------------------------------------------------------------------------
# Callback function to be invoked when MoisturePin status changes
# ---------------------------------------------------------------------------------------------------------------------

def callback(MoisturePin):

    if GPIO.input(MoisturePin):
        print "LED off"

        # Send email about watering plant
        send_email(message_opening_tap)

        # Open tap for 1 second
        openAndCloseTap(1)

        # Wait for 10 seconds for water to be absorbed by soil
        time.sleep(10)

        # check the soil moisture level after watering the plant, send email if moisture level is not restored
        if GPIO.input(MoisturePin):
            send_email(message_dead)


    else:
        print "LED on"
        # Send email if moisture level is ok and no watering is required
        send_email(message_alive)


# ---------------------------------------------------------------------------------------------------------------------
