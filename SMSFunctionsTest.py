import unittest
from SMSFunctions import *
import logging


class SMSFunctionsTest(unittest.TestCase):

    def test_send_sms_live(self):
        logging.info("test_send_sms_live: START")
        sendLiveSMS()
        logging.info("test_send_sms_live: END")

    def test_send_sms_dead(self):
        logging.info("test_send_sms_dead: START")
        sendDeadSMS()
        logging.info("test_send_sms_dead: END")

    def test_send_sms_opening_tap(self):
        logging.info("test_send_sms_opening_tap: START")
        sendOpeningTapSMS()
        logging.info("test_send_sms_opening_tap: END")
