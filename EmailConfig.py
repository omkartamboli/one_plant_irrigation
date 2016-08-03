
# ---------------------------------------------------------------------------------------------------------------------
#
# PLEASE NOTE:
#
# If you are using gmail smtp server and your gmail account to send emails, please make sure that you allow access to
# less secure apps to log in to your account by using following url
# https://www.google.com/settings/security/lesssecureapps
#
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
smtp_username = "enter_username_here"  # This is the username used to login to your SMTP provider
smtp_password = "enter_password_here"  # This is the password used to login to your SMTP provider

smtp_host = "enter_host_here"  # This is the host of the SMTP provider
smtp_port = 25  # This is the port that your SMTP provider uses

smtp_sender = "sender@email.com"  # This is the FROM email address
smtp_receivers = ['receiver@email.com']  # This is the TO email address

# The next three variables use triple quotes, these allow us to preserve the line breaks in the string.


# This is the message that will be sent when moisture is detected again

message_alive = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification - All OK !!!

Enough moisture in soil. No need to water plant.

"""


# This is the message that will be sent when NO moisture is detected, and opening the tap to water plant

message_opening_tap = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification - Opening Tap !!!

Warning, no moisture detected!
Opening tap to water plant!!!
"""


# This is the message that will be sent when no moisture is detected

message_dead = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification - No Water !!!

Warning, no moisture detected, and no enough water in container.
Please check water levels.

Plant death imminent!!! :'(
"""

# ---------------------------------------------------------------------------------------------------------------------
