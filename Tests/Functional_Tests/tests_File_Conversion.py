from unittest import TestCase
import os
from nose_parameterized import parameterized

from File_Conversion.Converter import Converter

CURRENT_DIRECTORY = os.path.dirname(__file__)
SAX_INSTRUMENT_ID = 65
OBOE_INSTRUMENT_ID = 68
LENGTH_OF_NOTE = 120


class FileConversionFunctionalTests(TestCase):

    # Case 2.1.1
    def test_header_list(self):
        rcff_files = self.create_rcff_files("Sax.mid")

        num_notes = 16

        # TODO: BUG 1.1
        self.assertEquals(1, len(rcff_files))
        self.assertEquals(SAX_INSTRUMENT_ID, rcff_files[0].instrument)
        self.assertEquals(num_notes * LENGTH_OF_NOTE, len(rcff_files[0].body))

        # TODO: BUG 1.3
        # TODO: BUG 1.1
        self.assertEquals(150, rcff_files[0].tempo)

    # Case 2.1.2
    # TODO: BUG 1.7
    # def test_timeslices(self):
    #     rcff_files = self.create_rcff_files("SaxOneNote.mid")
    #
    #     self.assertEquals(1, len(rcff_files))
    #     self.assertEquals()

    @parameterized.expand([["no_pitches", "Drums.mid"],  # Case 2.1.3
                           ["no_chords", "Piano.mid"],  # Case 2.1.4
                           ["long_rests", "SaxLongRest.mid"],  # Case 2.1.5a
                           ["empty", "SaxNoNotes.mid"], # Case 2.1.9
                           ])
    def test_voice_discard(self, name, test_file_name):
        rcff_files = self.create_rcff_files(test_file_name)

        self.assertEquals(0, len(rcff_files))

    @parameterized.expand([["0", "SaxFormat0.mid", 1, 8],  # Case 2.1.6
                           ["1", "OboeAndSaxFormat1.mid", 2, 12],  # Case 2.1.7a
                           # Format 2 test cancelled for now (Apparently, these are tough to find/make)
                           # ["2", "OboeAndSaxFormat2.mid", 2, 12],  # Case 2.1.7b
                           ])
    def test_midi_format_type(self, name, test_file_name, expected_rcff_files_created, num_notes):
        rcff_files = self.create_rcff_files(test_file_name)

        self.assertEquals(expected_rcff_files_created, len(rcff_files))

        sax_rcff = rcff_files[0]

        self.assertEquals(SAX_INSTRUMENT_ID, sax_rcff.instrument)
        self.assertEquals(num_notes * LENGTH_OF_NOTE, len(sax_rcff.body))

        self.assertEquals(150, sax_rcff.tempo)

        if expected_rcff_files_created == 2:
            oboe_rcff = rcff_files[1]
            self.assertEquals(OBOE_INSTRUMENT_ID, oboe_rcff.instrument)
            self.assertEquals(num_notes * LENGTH_OF_NOTE, len(oboe_rcff.body))

            self.assertEquals(150, oboe_rcff.tempo)

    # Case 2.1.10
    def test_exception_with_bad_file(self):
        self.assertRaises(TypeError, self.create_rcff_files, "TextDocument.mid")

    def test_midi_format_type(self, name, test_file_name, expected_rcff_files_created, num_notes):
        print "BOOM: " + test_file_name
        rcff_files = self.create_rcff_files("OboeAndSaxFormat1.mid")
        print "DONE: " + test_file_name

    #Helper Methods
    def create_rcff_files(self, file_name):
        test_file = os.path.abspath(os.path.join(CURRENT_DIRECTORY, "./Functional_Test_Files", file_name))

        converter = Converter(test_file)
        rcff_files = converter.create_rcff_files()
        return rcff_files

