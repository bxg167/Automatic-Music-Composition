import os
from unittest.case import TestCase
import copy_reg
import midi
from File_Conversion.RCFF import RCFF
from File_Conversion.TimeSlice import TimeSlice

from File_Conversion.ConvertRcffToMidi import ConvertRcffToMidi

file_path = os.path.dirname(__file__)


class TestConvertRcffToMidi(TestCase):

    # Needed to fix a bug with coverage.py. Coverage.py neglected to import copy_reg,
    # which is used in unpickle. This dummy test forces the import and allows the tests to run
    def test_rcff_build(self):
        rcff_path = os.path.abspath(os.path.join(file_path, "empty.rcff"))
        file_handler = open(rcff_path)
        RCFF.unpickle(rcff_path)
        file_handler.close()

    # pattern holds tracks hold events
    def test_create_midi_from_track_with_no_useful_info(self):
        # convert empty rcff
        convertR2M = ConvertRcffToMidi(os.path.abspath(os.path.join(file_path, "empty.rcff")))
        pattern = convertR2M.create_midi()

        self.assertEquals(1, pattern.format)
        self.assertEquals(480, pattern.resolution)
        self.assertEquals(1, len(pattern))
        self.assertEquals(midi.EndOfTrackEvent(tick=1), pattern[0][0])

    def test_create_midi_with_one_note(self):
        # We just need to instantiate a convert object. empty.rcff will be overridden
        convertR2M = ConvertRcffToMidi(os.path.abspath(os.path.join(file_path, "empty.rcff")))
        test_rcff = RCFF("one_note.rcff", 120, 0)
        test_rcff.add_time_slice_to_body(TimeSlice(60, 100, 9))
        test_rcff.add_time_slice_to_body(TimeSlice(60, 100, 1))
        test_rcff.add_time_slice_to_body(TimeSlice(60, 100, 8))
        print "test_rcff.body = ", test_rcff.body
        convertR2M.__set_rcff__(test_rcff)
        pattern = convertR2M.create_midi()

        self.assertEquals(1, len(pattern))
        self.assertEquals(3, len(pattern[0]))
        self.assertEquals(midi.NoteOnEvent(tick=0, velocity=100, pitch=60), pattern[0][0])
        self.assertEquals(midi.NoteOffEvent(tick=120, pitch=60), pattern[0][1])
        self.assertEquals(midi.EndOfTrackEvent(tick=1), pattern[0][2])

    def test_create_midi_from_longer_file(self):
        # instrument, rests,
        convertR2M = ConvertRcffToMidi(os.path.abspath(os.path.join(file_path, "empty.rcff")))
        test_rcff = RCFF("several_notes.rcff", 120, 66)      # volume = 120, inst = alto sax
        test_rcff.add_time_slice_to_body(TimeSlice(72, 80, 9))
        test_rcff.add_time_slice_to_body(TimeSlice(72, 80, 1))
        test_rcff.add_time_slice_to_body(TimeSlice(72, 80, 1))
        test_rcff.add_time_slice_to_body(TimeSlice(72, 80, 8))
        test_rcff.add_time_slice_to_body(TimeSlice(0, 0, 9))
        test_rcff.add_time_slice_to_body(TimeSlice(0, 0, 0))
        test_rcff.add_time_slice_to_body(TimeSlice(0, 0, 0))
        test_rcff.add_time_slice_to_body(TimeSlice(0, 0, 8))
        test_rcff.add_time_slice_to_body(TimeSlice(69, 100, 9))
        test_rcff.add_time_slice_to_body(TimeSlice(69, 100, 1))
        test_rcff.add_time_slice_to_body(TimeSlice(69, 100, 1))
        test_rcff.add_time_slice_to_body(TimeSlice(69, 100, 1))
        test_rcff.add_time_slice_to_body(TimeSlice(69, 100, 8))
        test_rcff.add_time_slice_to_body(TimeSlice(0, 0, 9))
        test_rcff.add_time_slice_to_body(TimeSlice(0, 0, 0))
        test_rcff.add_time_slice_to_body(TimeSlice(0, 0, 8))
        convertR2M.__set_rcff__(test_rcff)
        pattern = convertR2M.create_midi()
        #pattern.

        self.assertEquals(1, len(pattern))
        self.assertEquals(10, len(pattern[0]))
        self.assertEquals(midi.ProgramChangeEvent(value=66), pattern[0][0])
        self.assertEquals(midi.NoteOnEvent(tick=0, velocity=80, pitch=72), pattern[0][1])
        self.assertEquals(midi.NoteOffEvent(tick=240, pitch=72), pattern[0][2])
        self.assertEquals(midi.NoteOnEvent(tick=0, velocity=0, pitch=0), pattern[0][3])
        self.assertEquals(midi.NoteOffEvent(tick=240, pitch=0), pattern[0][4])
        self.assertEquals(midi.NoteOnEvent(tick=0, velocity=100, pitch=69), pattern[0][5])
        self.assertEquals(midi.NoteOffEvent(tick=360, pitch=69), pattern[0][6])
        self.assertEquals(midi.NoteOnEvent(tick=0, velocity=0, pitch=0), pattern[0][7])
        self.assertEquals(midi.NoteOffEvent(tick=120, pitch=0), pattern[0][8])
        self.assertEquals(midi.EndOfTrackEvent(tick=1), pattern[0][9])