import unittest
from StepperFunctions import *


class StepperFunctionsTest(unittest.TestCase):

    def setUp(self):
        # Setup GPIO mode and pins's mode
        setupGPIOForStepperMotor(StepPins)

    def test_one_rev_high_speed(self):
        print "test_one_rev_high_speed: START"
        rotateMotorClockWise(get_speed_fast(), 1)
        time.sleep(0.2)
        rotateMotorAntiClockWise(get_speed_fast(), 1)
        time.sleep(1)
        print "test_one_rev_high_speed: END"

    def test_two_rev_high_speed(self):
        print "test_two_rev_high_speed: START"
        rotateMotorClockWise(get_speed_fast(), 2)
        time.sleep(0.2)
        rotateMotorAntiClockWise(get_speed_fast(), 2)
        time.sleep(1)
        print "test_two_rev_high_speed: END"

    def test_one_rev_medium_speed(self):
        print "test_one_rev_medium_speed: START"
        rotateMotorClockWise(get_speed_medium(), 1)
        time.sleep(0.2)
        rotateMotorAntiClockWise(get_speed_medium(), 1)
        time.sleep(1)
        print "test_one_rev_medium_speed: END"

    def test_one_rev_slow_speed(self):
        print "test_one_rev_slow_speed: START"
        rotateMotorClockWise(get_speed_slow(), 1)
        time.sleep(0.2)
        rotateMotorAntiClockWise(get_speed_slow(), 1)
        time.sleep(1)
        print "test_one_rev_slow_speed: END"

    def test_one_rev_very_slow_speed(self):
        print "test_one_rev_very_slow_speed: START"
        rotateMotorClockWise(get_speed_very_slow(), 1)
        time.sleep(0.2)
        rotateMotorAntiClockWise(get_speed_very_slow(), 1)
        time.sleep(1)
        print "test_one_rev_very_slow_speed: END"

    def tearDown(self):
        cleanupGPIO()

