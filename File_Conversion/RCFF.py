import pickle

from File_Conversion.TimeSlice import *


class RCFF:
    def __init__(self, midi_file, tempo, instrument):
        self.midi_file = midi_file
        self.tempo = tempo
        self.instrument = instrument
        self.body = []

    def add_time_slice_to_body(self, time_slice):
        self.body.append(time_slice)

    def check_for_excessive_rest(self):
        beat_count = 0
        rest_count = 0

        for body_slice in self.body:
            if body_slice.message == BEAT:
                beat_count += 1
            elif body_slice.message == REST:
                rest_count += 1
        return beat_count >= rest_count and beat_count != 0

    def pickle(self, file_handler):
        pickle.dump(self, file_handler)

    @staticmethod
    def unpickle(file_handler):
        rcff = pickle.load(file_handler)
        return rcff
