import os
from types import NoneType
from unittest import TestCase

import midi

from File_Conversion.RCFF import RCFF
from File_Conversion.Converter import Converter


class TestConverter(TestCase):
    def test_extract_data_from_track_with_no_useful_info(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join("./File_Conversion", "mary.mid")))

        self.assertEquals(2, len(pattern))

        instrument, tempo, notes = Converter.extract_data(pattern[0])
        self.assertEquals(-1, instrument)
        self.assertEquals(0, tempo)
        self.assertEquals(0, len(notes))

    def test_extract_data_from_track_with_exception_thrown(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join("./File_Conversion", "mary.mid")))

        self.assertRaises(RuntimeError, Converter.extract_data, pattern[1])

    def test_extract_data_from_file_with_useful_info(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join("./File_Conversion", "bsax2.mid")))
        self.assertEquals(15, len(pattern))

        instrument, tempo, notes = Converter.extract_data(pattern[10]) #First 9 patterns threw errors due to multiple voices.

        self.assertEquals(65, instrument)
        self.assertEquals(0, tempo)
        self.assertEquals(296, len(notes))
