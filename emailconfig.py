

# ------------------------------------------------------------------------------------------------------------------------

smtp_username = "enter_username_here"  # This is the username used to login to your SMTP provider
smtp_password = "enter_password_here"  # This is the password used to login to your SMTP provider
smtp_host = "enter_host_here"  # This is the host of the SMTP provider
smtp_port = 25  # This is the port that your SMTP provider uses

smtp_sender = "sender@email.com"  # This is the FROM email address
smtp_receivers = ['receiver@email.com']  # This is the TO email address

# The next two variables use triple quotes, these allow us to preserve the line breaks in the string.

# This is the message that will be sent when NO moisture is detected

message_dead = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification

Warning, no moisture detected! Plant death imminent!!! :'(
"""

# This is the message that will be sent when moisture IS detected again

message_alive = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification

Panic over! Plant has water again :)
"""

