import unittest
import os

from File_Conversion.Converter import Converter

FILE_PATH = os.path.dirname(__file__)
SAX_INSTRUMENT_ID = 65


class FileConversionFunctionalTestSuite(unittest.TestCase):

    # Case 2.1.1
    def header_list_test(self):
        test_file = os.path.abspath(os.path.join(FILE_PATH, "../Functional_Test_Files/SaxFormat1.mid"))
        # test_file = os.path.abspath(os.path.join(FILE_PATH, "C:\Users\Bryce\PycharmProjects\Automatic-Music-Composition\Automatic-Music-Composition\Tests\Music Files\sball1.mid"))

        converter = Converter(test_file)

        rcff_files = converter.create_rcff_files()

        num_notes = 16
        length_of_notes = 120

        # TODO: BUG 1.5
        # self.assertEquals(1, len(rcff_files))
        # self.assertEquals(SAX_INSTRUMENT_ID, rcff_files[0].instrument)
        # self.assertEquals(num_notes * length_of_notes,, len(rcff_file[0].body))

        # TODO: BUG 1.2
        # TODO: BUG 1.5
        # self.assertEquals(150, rcff_files[0].tempo)
