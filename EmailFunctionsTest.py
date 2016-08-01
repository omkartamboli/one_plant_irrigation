import unittest
from EmailFunctions import *


class EmailFunctionsTest(unittest.TestCase):
    def test_send_mail_dead(self):
        print "Send dead email: START"
        send_email(message_dead)
        print "Send dead email: END"

    def test_send_mail_alive(self):
        print "Send alive email: START"
        send_email(message_alive)
        print "Send alive email: END"


if __name__ == '__main__':
    unittest.main()
