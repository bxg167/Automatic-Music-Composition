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

    @staticmethod
    def unpickle(file_handler):
        rcff = pickle.load(file_handler)
        return rcff
