import unittest
from SMSFunctions import *


class SMSFunctionsTest(unittest.TestCase):

    def test_send_sms_live(self):
        print "test_send_sms_live: START"
        sendLiveSMS()
        print "test_send_sms_live: END"

    def test_send_sms_dead(self):
        print "test_send_sms_dead: START"
        sendDeadSMS()
        print "test_send_sms_dead: END"

    def test_send_sms_opening_tap(self):
        print "test_send_sms_opening_tap: START"
        sendOpeningTapSMS()
        print "test_send_sms_opening_tap: END"
