# Import required libraries
from EmailFunctions import *
from SMSFunctions import *
from StepperFunctions import *


# ---------------------------------------------------------------------------------------------------------------------
# Callback function to be invoked when MoisturePin status changes
# ---------------------------------------------------------------------------------------------------------------------

def callback(MoisturePin):

    if GPIO.input(MoisturePin):
        print "LED off"

        # Send email about watering plant
        if EnableEmailNotifications:
            send_email(message_opening_tap)

        # Send sms about watering plant
        if EnableSMSNotifications:
            sendOpeningTapSMS()

        # Open tap for 1 second
        openAndCloseTap(1)

        # Wait for 10 seconds for water to be absorbed by soil
        time.sleep(10)

        # Check the soil moisture level after watering the plant,
        if GPIO.input(MoisturePin):

            # Send email if moisture level is not restored
            if EnableEmailNotifications:
                send_email(message_dead)

            # Send sms if moisture level is not restored
            if EnableSMSNotifications:
                sendDeadSMS()


    else:
        print "LED on"

        # Send email if moisture level is ok and no watering is required
        if EnableEmailNotifications:
            send_email(message_alive)

        # Send sms if moisture level is ok and no watering is required
        if EnableSMSNotifications:
            sendLiveSMS()


# ---------------------------------------------------------------------------------------------------------------------
