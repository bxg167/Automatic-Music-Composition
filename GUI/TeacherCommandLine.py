import argparse
import os

import sys

DEFAULT_RNN_SNAPSHOT_NAME = "default.snapshot"


def print_error_and_terminate(error_message):
    print(error_message)
    sys.exit()


def file_check(file_path, var_name):
    if file_path is not None:
        if file_path != "" and not os.path.isfile(file_path):
            print_error_and_terminate("The file path given to " + var_name + " does not exist.")


def get_rcff_files():
    temp_files = []

    for file_name in os.listdir(rcff):
        if file_name.endswith(".rcff"):
            temp_files.append(os.path.join(rcff, file_name))
    return temp_files

parser = argparse.ArgumentParser(prog="Teacher")

# Optional Parameters
parser.add_argument("-R", "--rcff", help="RCFF Folder", metavar="RCFF_FOLDER_PATH", required=True)

# Required Parameters
parser.add_argument("-U", "--update", help="The location of an already existing RNN", metavar="RNN_NAME")
parser.add_argument("-S", "--save", help="The desired location and name given to the new RNN snapshot", metavar="SAVE_PATH", default=DEFAULT_RNN_SNAPSHOT_NAME)

# MAY NOT NEED
parser.add_argument("-N", "--name", help="The location of the RNN snapshot", metavar="RNN_NAME")

args = parser.parse_args()
name = args.name
rcff = args.rcff
save = args.save
update = args.update

file_check(name, "name")
file_check(update, "update")

if not os.path.isdir(rcff):
    print_error_and_terminate("The passed directory containing RCFF files does not exist.")

rcff_files = get_rcff_files()

if len(rcff_files) == 0:
    print_error_and_terminate("The passed directory containing RCFF has no rcff files in it.")

# The RNN should be saved with the rcff files, if it isn't otherwised specified.
if save == DEFAULT_RNN_SNAPSHOT_NAME:
    save = os.path.join(rcff, save)

if not os.path.exists(os.path.dirname(save)):
    print_error_and_terminate("The directory provided for save does not exist. Please save the RNN in an already existing directory ")

# If save has been specified and update has not been, then the user cannot specify a save location that already exists.
if update is None and os.path.exists(save):
        print_error_and_terminate("The save name and location given already exists. "
                                  "If you wish to alter the already existing RNN snapshot, "
                                  "please use the --update flag, instead of the --save flag.")

for rcff_file in rcff_files:
    # Insert the actual Instructor code here
    file_name = os.path.basename(rcff_file)

    dummy_file = 0
    if update is not None:
        dummy_file = open(update, 'a')
        dummy_file.write("Hello")
    else:
        dummy_file = open(save, 'w')


    print("Current File: " + file_name)

print("\nSuccessful input.")
