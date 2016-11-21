import pickle
import uuid
from unittest import TestCase
import os

from File_Conversion.RCFF import RCFF

CURRENT_DIRECTORY = os.path.dirname(__file__)
EXISTING_RNN_FILE = CURRENT_DIRECTORY + "test.snapshot"


class PlaybackFunctionalTests(TestCase):

    # Case 4.1.1 & 4.1.2a
    def test_midi_creation(self):
        unique_midi_name = os.path.join(CURRENT_DIRECTORY, str(uuid.uuid4()) + ".mid")

        # # Playback.make_file will use two methods, create_rcff and convert_rcff_to_midi.
        # Playback.make_file(RNN=EXISTING_RNN_FILE, file_name=unique_midi_name)

        self.assertTrue(os.path.exists(unique_midi_name))

    # Case 4.1.2b
    def test_midi_creation_with_seed(self):
        file_handler = open(os.path.join(CURRENT_DIRECTORY, "Functional_Test_Files/RCFF_Files/OboeAndSax_1.rcff"), "r")

        rcff_seed = pickle.load(file_handler)

        new_rcff = RCFF("", 0, "")
        # new_rcff = Playback.create_rcff(RNN=EXISTING_RNN_FILE, seed=rcff_seed)

        number_of_matching_timeslices = 0

        # The test is failing here because of the dummy rcff. This should fix itself when we create the actual playback class.
        for timeslice_index in range(0, len(rcff_seed.body)):
            if rcff_seed.body[timeslice_index].message == new_rcff.body[timeslice_index].message:
                number_of_matching_timeslices += 1

        self.assertTrue(len(rcff_seed.body) / 2 < number_of_matching_timeslices, "Less then half of the notes included in the seed were included in the newly created rcff file.")

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
