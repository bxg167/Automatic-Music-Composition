import os
from unittest.case import TestCase

import midi

from File_Conversion.Converter import Converter

file_path = os.path.dirname(__file__)


class TestConverter(TestCase):
    def test_extract_data_from_track_with_no_useful_info(self):
        # Mary may be passed in, but we are going to override the pattern saved by it.
        # This is just so we can create the Converter Object
        c = Converter(os.path.abspath(os.path.join(file_path, "mary.mid")))
        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "mary.mid")))

        self.assertEquals(2, len(pattern))

        instrument, tempo, notes = c.__extract_data__(pattern[0])
        self.assertEquals(-1, instrument)
        self.assertEquals(0, tempo)
        self.assertEquals(0, len(notes))

    def test_extract_data_from_track_with_exception_thrown(self):
        c = Converter(os.path.abspath(os.path.join(file_path, "mary.mid")))
        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "mary.mid")))

        self.assertRaises(RuntimeError, c.__extract_data__, pattern[1])

    def test_extract_data_from_file_with_useful_info(self):
        c = Converter(os.path.abspath(os.path.join(file_path, "bsax2.mid")))
        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "bsax2.mid")))
        self.assertEquals(15, len(pattern))

        instrument, notes = c.__extract_data__(pattern[10]) #First 9 patterns threw errors due to multiple voices.

        self.assertEquals(65, instrument)
        self.assertEquals(296, len(notes))
