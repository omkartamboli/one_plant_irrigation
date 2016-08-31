import unittest
from EmailFunctions import *


class EmailFunctionsTest(unittest.TestCase):
    def test_send_mail_dead(self):
        logging.info("Send dead email: START")
        send_email(message_dead)
        logging.info("Send dead email: END")

    def test_send_mail_alive(self):
        logging.info("Send alive email: START")
        send_email(message_alive)
        logging.info("Send alive email: END")


if __name__ == '__main__':
    unittest.main()
