import os
from unittest.case import TestCase

from Training.tflstm import NeuralNetwork

file_path = os.path.dirname(__file__)

class TestTraining(TestCase):
    def test_makes_files(self):
        # setup
        nn = NeuralNetwork()
        snapshot_fake_path = os.path.join(file_path, 'abcd')
        snapshot_paths = [
            os.path.join(file_path, 'abcd.data-00000-of-00001'),
            os.path.join(file_path, 'abcd.index'),
            os.path.join(file_path, 'abcd.meta'),
            os.path.join(file_path, 'checkpoint'),
        ]
        sample_path = os.path.join(file_path, 'efgh')
        
        # ensure snapshot files don't exist
        for check_path in snapshot_paths:
            if os.path.isfile(check_path):
                os.remove(check_path)
        
        # save snapshot
        nn.save(snapshot_fake_path)
        
        # assert snapshot files exist
        for check_path in snapshot_paths:
            self.assertTrue(os.path.isfile(check_path))
        
        # load snapshot
        nn.load(snapshot_fake_path)
        
        # delete snapshot files
        for check_path in snapshot_paths:
            if os.path.isfile(check_path):
                os.remove(check_path)
            
        # ensure sample file doesn't exist
        if os.path.isfile(sample_path):
            os.remove(sample_path)
        
        # save sample
        nn.sample(sample_path, 1)
        
        # assert sample file exists
        self.assertTrue(os.path.isfile(sample_path))
        
        # delete sample file
        if os.path.isfile(sample_path):
            os.remove(sample_path)

if __name__ == '__main__':
    t = TestTraining()
    t.test_makes_files()