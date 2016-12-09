import os
from unittest.case import TestCase

from File_Conversion.Converter import Converter
from File_Conversion.RCFF import RCFF
from File_Conversion.TimeSlice import *

file_path = os.path.dirname(__file__)


class TestConverter(TestCase):
    def test_create_time_slices_from_note(self):
        # Mary may be passed in, but we are going to override the pattern saved by it.
        # This is just so we can create the Converter Object
        c = Converter(os.path.abspath(os.path.join(file_path, "mary.mid")))

        time = 0
        note_length = 100
        rcff_length = 3    # begin, beat, end
        pitch = 15
        volume = 20
        note = (time, note_length, pitch, volume)

        rcff = RCFF("C:\\Users\\Bryce", 10, "Sax")

        rcff = c.__create_time_slices_from_note__(rcff, note)

        self.assertEqual(rcff_length, len(rcff.body))
        for timeslice in rcff.body:
            self.assertEqual(pitch, timeslice.pitch)
            self.assertEqual(volume, timeslice.volume)

        self.assertEqual(BEGIN, rcff.body[0].message)
        self.assertEqual(BEAT, rcff.body[1].message)
        self.assertEqual(END, rcff.body[2].message)

