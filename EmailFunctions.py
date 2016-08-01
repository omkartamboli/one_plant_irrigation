# Import required libraries
import smtplib
from smtplib import SMTPException
from emailconfig import *


# ----------------------------------------------------------------------------------------------------------------------

# This is our sendEmail function

def send_email(smtp_message):
    try:
        smtpObj = smtplib.SMTP(smtp_host, smtp_port)
        smtpObj.login(smtp_username,
                      smtp_password)  # If you don't need to login to your smtp provider, simply remove this line
        smtpObj.sendmail(smtp_sender, smtp_receivers, smtp_message)
        print "Successfully sent email"

    except SMTPException:
        print "Error: unable to send email"

send_email(message_alive)
send_email(message_dead)