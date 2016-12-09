import os
from unittest.case import TestCase
import math
import midi

from File_Conversion.Converter import Converter

file_path = os.path.dirname(__file__)

class TestConverter(TestCase):
    def test_create_rcff_file_from_track_with_no_useful_info(self):

        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "mary.mid")))

        # pattern = midi.read_midifile(os.path.abspath(os.path.join("./File_Conversion_Tests", "mary.mid")))

        self.assertEquals(2, len(pattern))

        # Mary may be passed in, but we are going to override the pattern saved by it. This is just so we can create the Converter Object
        c = Converter(os.path.abspath(os.path.join(file_path, "mary.mid")))

        rcff = c.__create_rcff_file__(pattern[0],0)
        self.assertEquals(0, len(rcff.body))
        self.assertEquals(-1, rcff.instrument)
        self.assertEquals(0, rcff.tempo)
        self.assertEquals(os.path.abspath(os.path.join(file_path, "mary.mid")), rcff.midi_file)

        self.assertRaises(RuntimeError, Converter.__extract_data__, pattern[1])

    def test_create_rcff_file_from_track_with_exception_thrown(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "mary.mid")))

        self.assertRaises(RuntimeError, Converter.__extract_data__, pattern[1])

    def test_create_rcff_file_from_file_with_useful_info(self):
        pattern = midi.read_midifile(os.path.abspath(os.path.join(file_path, "bsax2.mid")))

        # Mary may be passed in, but we are going to override the pattern saved by it. This is just so we can create the Converter Object
        c = Converter(os.path.abspath(os.path.join(file_path, "mary.mid")))

        rcff = c.__create_rcff_file__(pattern[10],0)

        instrument, notes = Converter.__extract_data__(pattern[10])

        expected_body_length = 0
        for note in notes:
            time, length, pitch, volume = note
            expected_body_length += length

        #self.assertEquals(expected_body_length, len(rcff.body)*c.resolution) #now includes rests so this wont work, checked in single note midi file test

        self.assertEquals(65, rcff.instrument)
        self.assertEquals(0, rcff.tempo)
        self.assertEquals(os.path.abspath(os.path.join(file_path, "mary.mid")), rcff.midi_file)

    def test_create_rcff_file_from_midi_with_single_note(self):
        c = Converter(os.path.abspath(os.path.join(file_path, "SaxOneNote.mid")))
        rcff = c.create_rcff_files()
        note = 35
        vol = 127
        count = 0
        length = 120
        res = 480
        print "length ", len(rcff)
        for ts in rcff[0].body:
            self.assertEquals(ts.pitch, note)
            self.assertEquals(ts.volume,vol)
            count = count +1
        self.assertTrue(len(rcff[0].body),int(math.ceil(length/(res/4))))

    
            
