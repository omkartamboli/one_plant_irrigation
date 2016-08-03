# ---------------------------------------------------------------------------------------------------------------------
# We are using twilio SMS gateway to send SMS, if you dont want this feature remove the SMS code.
# If you want to use twilio, register free at https://www.twilio.com/
# We don't support or advise using this service, it's user preference
# ---------------------------------------------------------------------------------------------------------------------


ACCOUNT_SID = '<Your Account SID provided by twilio>'
AUTH_TOKEN = '<Your auth token provided by twilio>'


TO_NUMBER = '<Your verified number with twilio>'
FROM_NUMBER = '<Number Provided by twilio to you>'



# The next three variables use triple quotes, these allow us to preserve the line breaks in the string.


# This is the message that will be sent when moisture IS detected again

sms_message_alive = """Enough moisture in soil. No need to water plant."""


# This is the message that will be sent when NO moisture is detected, and opening the tap to water plant

sms_message_opening_tap = """Warning, no moisture detected!
Opening tap to water plant!!!
"""


# This is the message that will be sent when NO moisture is detected evenafter watering plant

sms_message_dead = """Warning, no moisture detected, and no enough water in container.
Please check water levels.

Plant death imminent!!! :'(
"""
