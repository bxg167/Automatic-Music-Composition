import os
from unittest.case import TestCase

import midi

from File_Conversion.Converter import Converter


class TestConverter(TestCase):
    def test_create_rcff_file_from_track_with_no_useful_info(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join("./File_Conversion_Tests", "mary.mid")))

        self.assertEquals(2, len(pattern))

        c = Converter("Dummy")

        rcff = c.create_rcff_file(pattern[0])
        self.assertEquals(0, len(rcff.body))
        self.assertEquals(-1, rcff.instrument)
        self.assertEquals(0, rcff.tempo)
        self.assertEquals("Dummy", rcff.midi_file)

        self.assertRaises(RuntimeError, Converter.extract_data, pattern[1])

    def test_create_rcff_file_from_track_with_exception_thrown(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join("./File_Conversion_Tests", "mary.mid")))

        self.assertRaises(RuntimeError, Converter.extract_data, pattern[1])

    def test_create_rcff_file_from_file_with_useful_info(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join("./File_Conversion_Tests", "bsax2.mid")))

        c = Converter("Dummy")

        rcff = c.create_rcff_file(pattern[10])

        instrument, tempo, notes = Converter.extract_data(pattern[10])

        expected_body_length = 0
        for note in notes:
            time, length, pitch, volume = note
            expected_body_length += length

        self.assertEquals(expected_body_length, len(rcff.body))

        self.assertEquals(65, rcff.instrument)
        self.assertEquals(0, rcff.tempo)
        self.assertEquals("Dummy", rcff.midi_file)

