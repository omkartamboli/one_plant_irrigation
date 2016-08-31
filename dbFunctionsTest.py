import unittest
from dbFunctions import *


class DbFunctionsTest(unittest.TestCase):

    def test_getConfigValue_apiKey(self):
        logging.info("test_getConfigValue_apiKey: START")
        apikey = getConfigValue("data_no_of_hours")
        logging.info("Api key is {0}".format(apikey))
        logging.info("test_getConfigValue_apiKey: END")
