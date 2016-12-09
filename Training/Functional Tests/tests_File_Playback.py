import pickle
import uuid
from unittest import TestCase
import os

from File_Conversion.RCFF import RCFF

CURRENT_DIRECTORY = os.path.dirname(__file__)
EXISTING_RNN_FILE = CURRENT_DIRECTORY + "test.snapshot"


class PlaybackFunctionalTests(TestCase):

    # Will be changed to the correct number when the Playback class has been implemented
    DEFAULT_NUMBER_OF_TIMESLICES = 300

    # Case 4.1.3a
    def test_timeslices_match_default_amount(self):
        new_rcff = RCFF("", 0, "")
        # new_rcff = Playback.create_rcff(RNN=EXISTING_RNN_FILE)

        self.assertEquals(self.DEFAULT_NUMBER_OF_TIMESLICES, len(new_rcff.body))

    # Case 4.1.3b
    def test_timeslices_match_custom_amount(self):
        new_rcff = RCFF("", 0, "")
        # new_rcff = Playback.create_rcff(RNN=EXISTING_RNN_FILE, num_timeslices=5000)

        self.assertEquals(5000, len(new_rcff.body))

    # Case 4.1.4
    def test_exception_raised_with_bad_file(self):
        bad_snapshot = os.path.join(CURRENT_DIRECTORY, "Functional_Test_Files\Text.snapshot")

        # If we try to create an rcff file with a bad snapshot, an exception should be raised.
        self.assertRaises(Exception,  # Playback.create_rcff(RNN=bad_snapshot)
                          )
