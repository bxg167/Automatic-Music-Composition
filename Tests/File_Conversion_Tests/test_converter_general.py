from unittest.case import TestCase

from File_Conversion.Converter import Converter
from File_Conversion.RCFF import RCFF


class TestConverter(TestCase):
    def test_create_time_slices_from_note(self):

        time = 5
        length = 10
        pitch = 15
        volume = 20
        self.fail()
        note = (time, length, pitch, volume)

        rcff = RCFF("C:\\Users\\Bryce", 10, "Sax")

        rcff = Converter.__create_time_slices_from_note__(rcff, note)

        self.assertEqual(length, len(rcff.body))
        for timeslice in rcff.body:
            self.assertEqual(pitch, timeslice.pitch)
            self.assertEqual(volume, timeslice.volume)

        self.assertEqual(9, rcff.body[0].message)

        for i in range(1, length):
            self.assertEqual(0, rcff.body[i].message)
