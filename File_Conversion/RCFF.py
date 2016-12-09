import pickle

from File_Conversion.TimeSlice import *


class RCFF(object):
    def __init__(self, midi_file, tempo, instrument):
        self.midi_file = midi_file
        self.tempo = tempo
        self.instrument = instrument
        self.body = []

    def add_time_slice_to_body(self, time_slice):
        self.body.append(time_slice)

    # Returns True if rests are NOT excessive (beat makes up at least 1/4 of time slices)
    def check_for_excessive_rest(self):
        beat_count = 0
        rest_count = 0

        for body_slice in self.body:
            if body_slice.message == BEAT:
                beat_count += 1
            elif body_slice.message == REST:
                rest_count += 1
        return beat_count >= rest_count / 2 and beat_count != 0
    
    def __str__(self):
        retval = 'RCFF: [\n'
        for ts in self.body:
            retval += '    ' + ts.__str__() + '\n'
        retval += ']\n'
        return retval

    def pickle(self, file_handler):
        pickle.dump(self, file_handler)

    @staticmethod
    def unpickle(file_handler):
        rcff = pickle.load(file_handler)
        return rcff
