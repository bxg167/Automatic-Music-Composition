import os

import errno
from types import NoneType

from File_Conversion.Converter import Converter


class Mediator:

    @staticmethod
    def convert_file(file_name, folder_dir):
        try:
            c = Converter(os.path.join(folder_dir, file_name))
            rcff_files = c.create_rcff_files()
        except TypeError:
            return TypeError
        except Warning:
            return TypeError

        i = 0

        new_folder_dir = os.path.join(folder_dir, "RCFF_Files")
        Mediator.try_create_dir(new_folder_dir)

        for rcff_file in rcff_files:
            new_file_name = os.path.splitext(file_name)[0] + "_" + str(i) + ".rcff"

            file_handler = open(os.path.join(new_folder_dir, new_file_name), "w")

            rcff_file.pickle(file_handler)

            file_handler.close()
            i += 1
        return NoneType

    @staticmethod
    def try_create_dir(new_dir):
        try:
            os.makedirs(new_dir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
