# Import required libraries
from EmailFunctions import *
from SMSFunctions import *
from StepperFunctions import *
from ProximitySensorFunctions import *
from EventNames import *


# ---------------------------------------------------------------------------------------------------------------------
# Callback function to be invoked when MoisturePin status changes
# ---------------------------------------------------------------------------------------------------------------------

def callback(MoisturePin):

    moisturePinStatus = GPIO.input(MoisturePin)
    createEvent(CheckMoistureLevelEvent, -100.00, moisturePinStatus)

    if moisturePinStatus:

        print "LED off"

        if isEnoughWaterToOpenTap():

            # Send email about watering plant
            if shouldSendEmail(MoistureLevelLowStatus) or EnableEmailNotifications:
                send_email(message_opening_tap)

            # Send sms about watering plant
            if shouldSendSMS(MoistureLevelLowStatus):
                sendOpeningTapSMS()

            # Open tap for 1 second
            openAndCloseTap(1)

        else:

            # Send email if moisture level is not restored
            if shouldSendEmail(MoistureLevelLowAndWaterLevelLowStatus) or EnableEmailNotifications:
                send_email(message_dead)

            # Send sms if moisture level is not restored
            if shouldSendSMS(MoistureLevelLowAndWaterLevelLowStatus):
                sendDeadSMS()

    else:

        print "LED on"

        # Send email if moisture level is ok and no watering is required
        if shouldSendEmail(MoistureLevelOKStatus):
            send_email(message_alive)

        # Send sms if moisture level is ok and no watering is required
        if shouldSendSMS(MoistureLevelOKStatus):
            sendLiveSMS()


# ---------------------------------------------------------------------------------------------------------------------
