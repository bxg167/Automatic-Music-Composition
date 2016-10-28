import os
from unittest import TestCase

import midi

from File_Conversion.RCFF import RCFF
from File_Conversion.Converter import Converter


class TestConverter(TestCase):
    def test_create_time_slices_from_note(self):

        time = 5
        length = 10
        pitch = 15
        volume = 20

        note = (time, length, pitch, volume)

        rcff = RCFF("C:\\Users\\Bryce", 10, "Sax")

        rcff = Converter.create_time_slices_from_note(rcff, note)

        self.assertEqual(length, len(rcff.body))
        for timeslice in rcff.body:
            self.assertEqual(pitch, timeslice.pitch)
            self.assertEqual(volume, timeslice.volume)

        self.assertEqual(9, rcff.body[0].message)

        for i in range(1, length):
            self.assertEqual(0, rcff.body[i].message)

    def test_create_rcff_file_with_no_useful_info(self):
        c = Converter(os.path.abspath(os.path.join("./", "mary.mid")))
        # rcff = c.pattern
        #
        # rcff = Converter.create_rcff_file(pattern[1])
        # self.assertTrue(NoneType, rcff)

    def test_extract_data_from_file_with_no_useful_info(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join("./", "mary.mid")))

        self.assertEquals(2, len(pattern))

        instrument, tempo, notes = Converter.extract_data(pattern[0])
        self.assertEquals(-1, instrument)
        self.assertEquals(0, tempo)
        self.assertEquals(0, len(notes))

        self.assertRaises(RuntimeError, Converter.extract_data, pattern[1])
