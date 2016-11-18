import pickle


class RCFF:
    def __init__(self, midi_file, tempo, instrument):
        self.midi_file = midi_file
        self.tempo = tempo
        self.instrument = instrument
        self.body = []

    def add_time_slice_to_body(self, time_slice):
        self.body.append(time_slice)

    def check_for_excessive_rest(self):
        count = 0
        for body_slice in self.body:
            if body_slice.message == 8:
                count += 1
        return count > (.5 * len(self.body))

    def pickle(self, file_handler):
        pickle.dump(self, file_handler)

    # Used for testing purposes only
    def equals(self, other_rcff):
        if type(other_rcff) != RCFF:
            return False
        is_equal = self.tempo == other_rcff.tempo
        is_equal &= self.instrument == other_rcff.instrument
        is_equal &= self.midi_file == other_rcff.midi_file
        for notePos in range(0, len(self.body)):
            # If there is a TimeSlice in self that doesn't match the other_rcff, then we can return False early.
            if self.body[notePos].equals(other_rcff[notePos]):
                return False

        return is_equal
