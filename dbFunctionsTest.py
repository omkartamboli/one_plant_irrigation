import unittest
from dbFunctions import *


class DbFunctionsTest(unittest.TestCase):

    def test_getConfigValue_apiKey(self):
        print "test_getConfigValue_apiKey: START"
        apikey = getConfigValue("apiKey")
        print "Api key is {0}".format(apikey)
        print "test_getConfigValue_apiKey: END"
