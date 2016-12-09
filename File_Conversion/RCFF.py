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

    def check_for_excessive_rest(self):
        beat_count = 0
        rest_count = 0

        # print("volume\tpitch\tmessage")
        for body_slice in self.body:
            # print body_slice.volume, "\t", body_slice.pitch, "\t", body_slice.message
            if body_slice.message == BEAT:
                beat_count += 1
            elif body_slice.message == REST:
                rest_count += 1
        # print "beats: " + str(beat_count) + "; rests: " + str(rest_count)
        return beat_count >= rest_count / 2 and beat_count != 0
    
    def __str__(self):
        retval = 'RCFF: [\n'
        for ts in self.body:
            retval += '    ' + ts.__str__() + '\n'
        retval += ']\n'
        return retval

    def pickle(self, file_handler):
        pickle.dump(self, file_handler, protocol=2)

    @staticmethod
    def unpickle(file_handler):
        rcff = pickle.load(file_handler)
        return rcff
