import pickle
import uuid
from unittest import TestCase
import os

from Training.tflstm import NeuralNetwork

CURRENT_DIRECTORY = os.path.dirname(__file__)
EXISTING_RNN_FILE = CURRENT_DIRECTORY + "test.snapshot"


class PlaybackFunctionalTests(TestCase):

    nn = NeuralNetwork()

    # Will be changed to the correct number when the Playback class has been implemented
    DEFAULT_NUMBER_OF_TIMESLICES = 300

    # Case 4.1.3a
    def test_timeslices_match_default_amount(self):
        new_rcff = self.nn.sample('badfile')
        self.assertEquals(self.DEFAULT_NUMBER_OF_TIMESLICES, len(new_rcff.body))

    # Case 4.1.3b
    def test_timeslices_match_custom_amount(self):
        new_rcff = self.nn.sample('badfile', 5)
        self.assertEquals(5, len(new_rcff.body))

    # Case 4.1.4
    def test_exception_raised_with_bad_file(self):
        bad_snapshot = os.path.join(CURRENT_DIRECTORY, "Text.snapshot")
        # If we try to create an rcff file with a bad snapshot, an exception should be raised.
        with self.assertRaises(Exception):
            self.nn.load(bad_snapshot)

if __name__ == '__main__':
    t = PlaybackFunctionalTests()
    t.test_timeslices_match_default_amount()
    t.test_timeslices_match_custom_amount()
    t.test_exception_raised_with_bad_file()