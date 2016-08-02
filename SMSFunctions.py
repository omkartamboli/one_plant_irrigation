# ---------------------------------------------------------------------------------------------------------------------
# We are using twilio SMS gateway to send SMS, if you dont want this feature remove the SMS code.
# If you want to use twilio, register free at https://www.twilio.com/
# We don't support or advise using this service, it's user preference
# ---------------------------------------------------------------------------------------------------------------------


from twilio.rest import TwilioRestClient
from SMSConfig import *


# ---------------------------------------------------------------------------------------------------------------------
# Method to send SMS with given sms body
# ---------------------------------------------------------------------------------------------------------------------

def sendSMS(smsBody):

    # Initiate sms client
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

    # Send SMS
    client.messages.create(to=TO_NUMBER, from_=FROM_NUMBER, body=smsBody)


# ---------------------------------------------------------------------------------------------------------------------
# Method to send live status SMS
# ---------------------------------------------------------------------------------------------------------------------

def sendLiveSMS():
    sendSMS(sms_message_alive)


# ---------------------------------------------------------------------------------------------------------------------
# Method to send dead status SMS
# ---------------------------------------------------------------------------------------------------------------------

def sendDeadSMS():
    sendSMS(sms_message_dead)


# ---------------------------------------------------------------------------------------------------------------------
# Method to send opening tap status SMS
# ---------------------------------------------------------------------------------------------------------------------

def sendOpeningTapSMS():
    sendSMS(sms_message_opening_tap)


# ---------------------------------------------------------------------------------------------------------------------
