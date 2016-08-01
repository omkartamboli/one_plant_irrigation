# Import required libraries
import smtplib
from smtplib import SMTPException
from EmailConfig import *


# ----------------------------------------------------------------------------------------------------------------------

# This is our sendEmail function

def send_email(smtp_message):
    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_sender, smtp_receivers, smtp_message)
        server.quit()

        print "Successfully sent email"

    except SMTPException:
        print "Error: unable to send email"

# ----------------------------------------------------------------------------------------------------------------------

