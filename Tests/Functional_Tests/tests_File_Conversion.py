from unittest import TestCase
import os

from File_Conversion.Converter import Converter

CURRENT_DIRECTORY = os.path.dirname(__file__)
SAX_INSTRUMENT_ID = 65
OBOE_INSTRUMENT_ID = 68


class FileConversionFunctionalTests(TestCase):

    # Case 2.1.1
    def test_header_list(self):
        rcff_files = self.create_rcff_files("Sax.mid")

        num_notes = 16

        # TODO: BUG 1.1
        self.assertEquals(1, len(rcff_files))
        self.assertEquals(SAX_INSTRUMENT_ID, rcff_files[0].instrument)
        self.assertEquals(num_notes, len(rcff_files[0].body))

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
        expected_rcff_files_created = 1
        expected_num_notes = 8

        # 1 for start, 1 for sustained and 1 for end
        expected_num_timeslices_per_note = 3

        rcff_files = self.create_rcff_files( "SaxFormat0.mid")

        sax_rcff = rcff_files[0]

        self.assertEquals(expected_rcff_files_created, len(rcff_files))

        sax_rcff = rcff_files[0]

        self.assertEquals(SAX_INSTRUMENT_ID, sax_rcff.instrument)

        self.assertEquals(expected_num_notes * expected_num_timeslices_per_note, len(sax_rcff.body))

        self.assertEquals(150, sax_rcff.tempo)

        if expected_rcff_files_created == 2:
            oboe_rcff = rcff_files[1]
            self.assertEquals(OBOE_INSTRUMENT_ID, oboe_rcff.instrument)
            self.assertEquals(expected_num_notes, len(oboe_rcff.body))

            self.assertEquals(150, oboe_rcff.tempo)

    # Case 2.1.7a
    def test_midi_format_type_1(self):
        expected_rcff_files_created = 2
        expected_num_notes = 12

        # 1 for start, 1 for sustained and 1 for end
        expected_num_timeslices_per_note = 3

        rcff_files = self.create_rcff_files("OboeAndSaxFormat1.mid")

        self.assertEquals(expected_rcff_files_created, len(rcff_files))

        sax_rcff = rcff_files[0]

        self.assertEquals(SAX_INSTRUMENT_ID, sax_rcff.instrument)


        self.assertEquals(expected_num_notes * expected_num_timeslices_per_note, len(sax_rcff.body))

        self.assertEquals(150, sax_rcff.tempo)

        if expected_rcff_files_created == 2:
            oboe_rcff = rcff_files[1]
            self.assertEquals(OBOE_INSTRUMENT_ID, oboe_rcff.instrument)
            self.assertEquals(expected_num_notes * LENGTH_OF_NOTE, len(oboe_rcff.body))

            self.assertEquals(150, oboe_rcff.tempo)

    # Test  case 2.1.7b cancelled for now (Apparently, these are tough to find/make)
    # ["2", "OboeAndSaxFormat2.mid", 2, 12],  # Case 2.1.7b

    # Case 2.1.10
    def test_exception_with_bad_file(self):
        self.assertRaises(TypeError, self.create_rcff_files, "TextDocument.mid")

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

