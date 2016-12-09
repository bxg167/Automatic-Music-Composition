import os
from unittest.case import TestCase

import midi

from File_Conversion.Converter import Converter

file_path = os.path.dirname(__file__)

class TestConverter(TestCase):
    def test_extract_data_from_track_with_no_useful_info(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "mary.mid")))

        self.assertEquals(2, len(pattern))

        instrument, notes = Converter.__extract_data__(pattern[0])
        self.assertEquals(-1, instrument)
        self.assertEquals(0, len(notes))

    def test_extract_data_from_track_with_exception_thrown(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "mary.mid")))

        self.assertRaises(RuntimeError, Converter.__extract_data__, pattern[1])

    def test_extract_data_from_file_with_useful_info(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "bsax2.mid")))
        self.assertEquals(15, len(pattern))

        instrument, notes = Converter.__extract_data__(pattern[10]) #First 9 patterns threw errors due to multiple voices.

        self.assertEquals(65, instrument)
        self.assertEquals(294, len(notes))
