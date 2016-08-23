import unittest
import RPi.GPIO as GPIO
import time


class TwoChannelRelayTest(unittest.TestCase):
    def test_TwoChannelRelay(self):
        print "test_TwoChannelRelay: START"

        relayChannel1 = 5

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(relayChannel1, GPIO.OUT, initial=True)


        time.sleep(3)
        print "Setting : False1"
        GPIO.output(relayChannel1, False)
        time.sleep(3)
        GPIO.output(relayChannel1, True)
        #
        # i = 0
        #
        # while i < 10:
        #     GPIO.output(relayChannel1, True)
        #     time.sleep(.5)
        #     GPIO.output(relayChannel1, False)
        #     time.sleep(.5)
        #     i += 1

        GPIO.cleanup()

        print "test_TwoChannelRelay: END"
