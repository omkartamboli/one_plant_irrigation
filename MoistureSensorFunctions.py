# Import required libraries
from EmailFunctions import *
from SMSFunctions import *
from ProximitySensorFunctions import *
from EventNames import *
from WaterPumpFunctions import turnOnWaterPumpForNSeconds
from dbFunctions import getAvgAnalogValueOfLastNHours
from DHTFunctions import recordTemperatureAndHumidity
import datetime


# ---------------------------------------------------------------------------------------------------------------------
# Callback function to be invoked when MoisturePin status changes
# ---------------------------------------------------------------------------------------------------------------------

def callback():
    total_channels = 0
    total_analog_value = 0

    for channel in Moisture_ADC_Channels:
        channel_analog_value = mcp.read_adc(channel) - Moisture_Offset_Value
        total_analog_value += channel_analog_value
        print "Moisture Sensors : Channel {0} analog value : {1}".format(str(channel), str(channel_analog_value))
        total_channels += 1

    avg_analog_value = float(total_analog_value) / float(total_channels)
    digital_value = avg_analog_value > Moisture_Low_Value

    print "Moisture Sensors : Average analog value : {0} , Digital Value : {1}".format(str(avg_analog_value),
                                                                                       str(digital_value))

    eventTime = datetime.datetime.now()

    # Record temperature and humidity
    recordTemperatureAndHumidity(eventTime)

    # Record water level event and check if there is enough water to open tap if required
    enoughWater = isEnoughWaterToOpenTap(eventTime)

    if (0 - Moisture_Offset_Value) < avg_analog_value < (1023 - Moisture_Offset_Value):
        createEvent(CheckMoistureLevelEvent, avg_analog_value, digital_value, eventTime)

    # If analog value is greater than threshold, check the avg analog value of last one hour, before opening tap,
    # as there could be slight fluctuations in sensor readings

    if digital_value:
        avg_analog_value_of_last_hour = getAvgAnalogValueOfLastNHours(1, CheckMoistureLevelEvent)
        if avg_analog_value_of_last_hour is None or avg_analog_value_of_last_hour <= (0.95 * Moisture_Low_Value):
            digital_value = False


    if digital_value:

        if enoughWater:

            # Send email about watering plant
            if shouldSendEmail(MoistureLevelLowStatus):
                send_email(message_opening_tap)

            # Send sms about watering plant
            if shouldSendSMS(MoistureLevelLowStatus):
                sendOpeningTapSMS()

            # Open tap for configured time second
            turnOnWaterPumpForNSeconds(timeToKeepPumpOnInSecondsForFullWaterCapacity, eventTime)

        else:

            # Send email if moisture level is not restored
            if shouldSendEmail(MoistureLevelLowAndWaterLevelLowStatus):
                send_email(message_dead)

            # Send sms if moisture level is not restored
            if shouldSendSMS(MoistureLevelLowAndWaterLevelLowStatus):
                sendDeadSMS()

    else:

        # Send email if moisture level is ok and no watering is required
        if shouldSendEmail(MoistureLevelOKStatus):
            send_email(message_alive)

        # Send sms if moisture level is ok and no watering is required
        if shouldSendSMS(MoistureLevelOKStatus):
            sendLiveSMS()

# ---------------------------------------------------------------------------------------------------------------------
