from unittest import TestCase

from File_Conversion.RCFF import RCFF
from File_Conversion.TimeSlice import TimeSlice


class TestRCFF(TestCase):
    def test_add_time_slice_to_body(self):
        rcff = RCFF("C:\\Users\\Bryce", 10, "Sax")

        timeslice = TimeSlice("pitch", "100", "message")

        rcff.add_time_slice_to_body(timeslice)

        self.assertEqual(1, len(rcff.body))
        self.assertEqual(timeslice.message, rcff.body[0].message)
        self.assertEqual(timeslice.pitch, rcff.body[0].pitch)
        self.assertEqual(timeslice.volume, rcff.body[0].volume)
