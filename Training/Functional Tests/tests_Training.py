from unittest import TestCase
import os
import uuid


CURRENT_DIRECTORY = os.path.dirname(__file__)


class TrainingFunctionalTests(TestCase):

    # Case 3.1.1a
    def test_no_log_generated(self):
        random_name = os.path.join(CURRENT_DIRECTORY, str(uuid.uuid4()) + ".snapshot")

        initial_log_files = self.get_log_files(CURRENT_DIRECTORY)

        #Run code

        current_existing_log_files = self.get_log_files(CURRENT_DIRECTORY)

        self.assertListEqual(initial_log_files, current_existing_log_files, "A log file was created, even though it shouldn't have been.")

    # Case 3.1.1b
    def test_log_generation(self):
        random_name = os.path.join(CURRENT_DIRECTORY, str(uuid.uuid4()) + ".snapshot")

        initial_log_files = self.get_log_files(CURRENT_DIRECTORY)

        # Run code

        current_existing_log_files = self.get_log_files(CURRENT_DIRECTORY)

        self.assertTrue(len(initial_log_files) < len(current_existing_log_files), "No log file was created, even though it should have been.")

    # Case 3.1.2
    def test_snapshot_creation(self):
        random_name = os.path.join(CURRENT_DIRECTORY, str(uuid.uuid4()) + ".snapshot")
        working_rcff_file = os.path.join(CURRENT_DIRECTORY, "./Functional_Test_Files/RCFF_Files/OboeAndSax_1.rcff")

        # Run code

        self.assertTrue(os.path.exists(random_name), "The snapshot was not created.")

    # Case 3.1.3
    def test_bad_file_input(self):
        blank_rcff_file = os.path.join(CURRENT_DIRECTORY, "./Functional_Test_Files/Teacher RCFF files/Fake.rcff")

        self.assertRaises(Exception, uuid.uuid4())



    def get_log_files(self, path):
        log_files = []

        for file_name in os.listdir(path):
            if file_name.endswith(".log"):
                log_files.append(file_name)

        return log_files
