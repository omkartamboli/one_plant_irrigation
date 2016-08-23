import unittest
from ProximitySensorFunctions import *
from GPIOConfig import setupGPIOForProximitySensor



class ProximitySensorFunctionsTest(unittest.TestCase):

    def test_getDistance(self):

        print "test_getDistance: START"
        i = 0
        totalDistance = float(0.0);
        while (i<100):
            setupGPIOForProximitySensor()
            distance = getDistance()
            totalDistance += float(distance)
            i+=1
            time.sleep(.5)

        print "Avg distance is {0} cms".format(float(totalDistance/float(100.00)))

        print "test_getDistance: END"

    def test_getWaterLevel(self):

        print "test_getWaterLevel: START"
        i = 0
        totalWaterLevel = float(0.0);
        while (i<100):
            setupGPIOForProximitySensor()
            waterLevel = getWaterLevel()
            totalWaterLevel += float(waterLevel)
            i+=1
            time.sleep(.5)

        print "Avg water level is {0} cms".format(float(totalWaterLevel/float(100.00)))

        print "test_getWaterLevel: END"