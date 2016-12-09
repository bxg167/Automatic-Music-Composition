from unittest import TestCase
import os
import math
from File_Conversion.Converter import Converter

CURRENT_DIRECTORY = os.path.dirname(__file__)
SAX_INSTRUMENT_ID = 65
OBOE_INSTRUMENT_ID = 68

file_path = os.path.dirname(__file__)
class FileConversionFunctionalTests(TestCase):

    # Case 2.1.1
    def test_header_list(self):
        rcff_files = self.create_rcff_files("Sax.mid")

        num_notes = 16
        # 1 for BEGIN, 1 for BEAT (Each beat is a 16th note) and 1 for END
        expected_num_timeslices_per_note = 3

        self.assertEquals(1, len(rcff_files))
        self.assertEquals(SAX_INSTRUMENT_ID, rcff_files[0].instrument)
        self.assertEquals(num_notes * expected_num_timeslices_per_note, len(rcff_files[0].body))

        self.assertEquals(150, rcff_files[0].tempo)

    # Case 2.1.2
    def test_create_rcff_file_from_midi_with_single_note(self):
        c = Converter(os.path.abspath(os.path.join(file_path, "SaxOneNote.mid")))
        rcff = c.create_rcff_files()
        note = 35
        vol = 127
        count = 0
        length = 120
        res = 480
        for ts in rcff[0].body:
            self.assertEquals(ts.pitch, note)
            self.assertEquals(ts.volume,vol)
            count = count +1
        self.assertTrue(len(rcff[0].body),int(math.ceil(length/(res/4))))
        
    # Case 2.1.3
    def test_voice_discard_no_pitches(self):
        rcff_files = self.create_rcff_files("Drums.mid")

        self.assertEquals(0, len(rcff_files))

    # Case 2.1.4
    def test_voice_discard_no_chords(self):
        rcff_files = self.create_rcff_files("Piano.mid")

        self.assertEquals(0, len(rcff_files))

    # Case 2.1.5a
    def test_voice_discard_long_rests(self):
        rcff_files = self.create_rcff_files("SaxLongRest.mid")

        self.assertEquals(0, len(rcff_files))

    # Case 2.1.9 & Case 2.1.5b
    def test_voice_discard_empty(self):
        rcff_files = self.create_rcff_files("SaxNoNotes.mid")

        self.assertEquals(0, len(rcff_files))

    # Case 2.1.6
    def test_midi_format_type_0(self):
        expected_num_notes = 8

        # 1 for BEGIN, 2 for BEAT (Each beat is a 8th note) and 1 for END
        expected_num_timeslices_per_note = 4

        rcff_files = self.create_rcff_files("SaxFormat0.mid")

        self.assertEquals(1, len(rcff_files))

        sax_rcff = rcff_files[0]

        self.assertEquals(SAX_INSTRUMENT_ID, sax_rcff.instrument)

        self.assertEquals(expected_num_notes * expected_num_timeslices_per_note, len(sax_rcff.body))

        self.assertEquals(150, sax_rcff.tempo)

    # Case 2.1.7a
    def test_midi_format_type_1(self):
        expected_num_notes = 12
        expected_num_rests = 1

        # 1 for BEGIN, 1 for BEAT (the beats are each a 16th note) and 1 for END
        expected_num_timeslices_per_note = 3

        # 1 for BEGIN, 4 for REST (each rest is considered to be a 1/16th note) and 1 for END
        expected_num_timeslices_per_rest = 6

        rcff_files = self.create_rcff_files("OboeAndSaxFormat1.mid")

        self.assertEquals(2, len(rcff_files))

        sax_rcff = rcff_files[0]

        self.assertEquals(SAX_INSTRUMENT_ID, sax_rcff.instrument)

        self.assertEquals(expected_num_notes * expected_num_timeslices_per_note +
                          expected_num_rests * expected_num_timeslices_per_rest
                          , len(sax_rcff.body))

        self.assertEquals(150, sax_rcff.tempo)

        oboe_rcff = rcff_files[1]
        self.assertEquals(OBOE_INSTRUMENT_ID, oboe_rcff.instrument)
        self.assertEquals(expected_num_notes * expected_num_timeslices_per_note +
                          expected_num_rests * expected_num_timeslices_per_rest,
                          len(oboe_rcff.body))

        self.assertEquals(150, oboe_rcff.tempo)

    # Test  case 2.1.7b cancelled for now (Apparently, these are tough to find/make)
    # ["2", "OboeAndSaxFormat2.mid", 2, 12],  # Case 2.1.7b

    # Case 2.1.10
    def test_exception_with_bad_file(self):
        self.assertRaises(Exception, self.create_rcff_files, "TextDocument.mid")

    # No test case id.
    # This test was added to test what happens when a bad path is given to Converter's constructor.
    def test_file_not_exists_exception(self):
        self.assertRaises(Exception, lambda: Converter("bad_file.asdf.abc"))

    #Helper Methods
    def create_rcff_files(self, file_name):
        test_file = os.path.abspath(os.path.join(CURRENT_DIRECTORY, "./Functional_Test_Files", file_name))

        converter = Converter(test_file)
        rcff_files = converter.create_rcff_files()
        return rcff_files

