import argparse
import os
import uuid

from Training.tflstm import *

DEFAULT_RNN_SNAPSHOT_NAME = "default"


def print_error_and_terminate(error_message):
    print(error_message)
    sys.exit()


def file_check(file_path, var_name):
    if file_path is not None:
        if file_path != "" and not os.path.isfile(file_path):
            print_error_and_terminate("The file path given to " + var_name + " does not exist.")


def get_rcff_files():
    temp_files = []

    for file_name in os.listdir(teach):
        if file_name.endswith(".rcff"):
            temp_files.append(os.path.join(teach, file_name))
    return temp_files

parser = argparse.ArgumentParser(prog="Teacher")

# Optional Parameters
parser.add_argument("-T", "--teach", help="RCFF Folder that will be taught to the RNN.\nCannot be used with the --create command", metavar="RCFF_FOLDER_PATH")
parser.add_argument("-U", "--use", help="The location of an already existing RNN (Ends with .index", metavar="RNN_NAME")
parser.add_argument("-S", "--save", help="The desired location and name given to the new RNN snapshot", metavar="SAVE_PATH", default=DEFAULT_RNN_SNAPSHOT_NAME)
parser.add_argument("-C", "--create", help="The Number of RCFF files that should be made\nCannot be used with the --teach command", metavar="NUMBER_OF_RCFF_TO_MAKE", type=int, default=-1)

args = parser.parse_args()

create = args.create
save = args.save
use = args.use
teach = args.teach

if create == -1 and teach is None:
    print_error_and_terminate("No action commands were given. To use this program, use the either the --teach or the --create arguments, but not both")

elif create != -1 and teach is not None:
    print_error_and_terminate("Two action command were given. To use this program, only use --teach or only use --create, not both")


def teach_rnn(save_name):
    file_check(use, "use")

    if not os.path.isdir(teach):
        print_error_and_terminate("The passed directory containing RCFF files does not exist.")

    rcff_files = get_rcff_files()
    if len(rcff_files) == 0:
        print_error_and_terminate("The passed directory containing RCFF has no rcff files in it.")

    # The RNN should be saved with the rcff files, if it isn't otherwise specified.
    if save_name == DEFAULT_RNN_SNAPSHOT_NAME:
        save_name = os.path.join(teach, save_name)

    if not os.path.exists(os.path.dirname(save_name)):
        print_error_and_terminate(
            "The directory provided for save does not exist. Please save the RNN in an already existing directory ")

    # If --save has been specified and --update has not been, then the user cannot specify a save location that already exists.
    if use is None and os.path.exists(save_name):
        print_error_and_terminate("The save name and location given already exists. "
                                  "If you wish to use the already existing RNN snapshot, "
                                  "please use the --use flag, instead of the --save flag.")

    network = NeuralNetwork()

    for rcff_file in rcff_files:
        file_name = os.path.basename(rcff_file)

        if use is not None:
            use = use.replace(".index", "")
            network.load(use)

        file_handler = open(rcff_file, 'rb')

        network.train(RCFF.RCFF.unpickle(file_handler), 100)

        file_handler.close()

        if save_name is not None:
            network.save(save_name)
        elif use is not None:
            network.save(use)

        print("Current File: " + file_name)


def create_rcffs():
    if create <= 0:
        print_error_and_terminate("The requested number of rcff files to make is less than 1.")

    network = NeuralNetwork()
    if use is not None:
        network.load(use)
    else:
        print_error_and_terminate("Input a valid RNN file.")
    for i in range(0, create):
        network.sample(os.path.join(os.path.dirname(use), str(uuid.uuid4()), ".rcff"))


if create == -1:
    teach_rnn(save)
else:
    create_rcffs()
