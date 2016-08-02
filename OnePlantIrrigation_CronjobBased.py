# ---------------------------------------------------------------------------------------------------------------------
# This is main file which will use all other utilities to detect the moisture and turn on the tap if moisture is less
# This will also send email notifications about current status of the plant
# ---------------------------------------------------------------------------------------------------------------------


from MoistureSensorFunctions import *

# ---------------------------------------------------------------------------------------------------------------------
# Just call callback function which checks sensor, and does required actions.
# Call this python file at scheduled intervals using cron job utility
# ---------------------------------------------------------------------------------------------------------------------

callback(MoisturePin)
