from unittest import TestCase
import os
import uuid
from Training.tflstm import NeuralNetwork
from File_Conversion.RCFF import RCFF


CURRENT_DIRECTORY = os.path.dirname(__file__)


class TrainingFunctionalTests(TestCase):

    nn = NeuralNetwork()
    
    # Case 3.1.1b
    def test_log_generation(self):
        random_name = os.path.join(CURRENT_DIRECTORY, str(uuid.uuid4()) + ".snapshot")
        rcff_name = os.path.join(CURRENT_DIRECTORY, 'Sax_0.rcff')

        initial_log_files = self.get_log_files(CURRENT_DIRECTORY)

        # Run code
        with open(rcff_name, 'rb') as rcff:
            self.nn.train(RCFF.unpickle(rcff), 1)

        current_existing_log_files = self.get_log_files('.')

        self.assertTrue(len(initial_log_files) < len(current_existing_log_files), "No log file was created, even though it should have been.")

    # Case 3.1.2
    def test_snapshot_creation(self):
        random_name = os.path.join(CURRENT_DIRECTORY, str(uuid.uuid4()) + ".snapshot")

        # Run code
        self.nn.save(random_name)
        self.nn.load(random_name)

    # Case 3.1.3
    def test_bad_file_input(self):
        rcff_name = os.path.join(CURRENT_DIRECTORY, 'Fake.rcff')
        
        with open(rcff_name, 'rb') as rcff:
            with self.assertRaises(Exception):
                RCFF.unpickle(rcff)



    def get_log_files(self, path):
        log_files = []

        for file_name in os.listdir(path):
            if file_name.endswith(".log"):
                log_files.append(file_name)

        return log_files

if __name__ == '__main__':
    t = TrainingFunctionalTests()
    t.test_log_generation()
    t.test_snapshot_creation()
    t.test_bad_file_input()
