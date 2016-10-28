import os
import pickle

import midi

from RCFF import RCFF
from TimeSlice import TimeSlice


class Converter:
    def __init__(self, midi_file):
        self.midi_file = midi_file
        self.rcff_files = []

    def create_rcff_files(self):
        pattern = midi.read_midifile(self.midi_file)
        num_tracks = 0

        for track in pattern:
            # print("track")
            num_tracks += 1

            new_rcff = self.create_rcff_file(track)

            # TODO: Ignore songs with excessive rests.
            # if not( new_rcff.check_for_excessive_rest):
            self.rcff_files.append(new_rcff)

        # TODO: Remove this call and move it to the GUI.
        # TODO: This needs to be moved for testing purposes, so it will be moved when we need to worry about code coverage.
        self.pickle_files()

    #TODO: Make this method pickle the file at index i to a passed in file.
    # The below method is what I would like, but it would be annoying to do it this way, since we will need to know
    # how many files we have in rcff_files. May have to add a .length() method, or something like that.
    # Again, this will be to help with code coverage and with mocking. When I work on the code coverage part,
    # I will play around with how to get this to work nicely later.
    # def pickle_files(self, file_handler, file_num)
    def pickle_files(self):
        i = 0

        for rcff_file in self.rcff_files:
            # print("file")
            new_file_name = os.path.splitext(self.midi_file)[0]

            # TODO: Move this part out of this method, and force the user to pass in the file.
            f = open(new_file_name + str(i) + ".rcff", "w")
            pickle.dump(rcff_file, f)
            i += 1

    def create_rcff_file(self, track):
        instrument = -1
        notes = []
        tempo = -1
        try:
            instrument, tempo, notes = self.extract_data(track)
        except RuntimeError as e:
            # print(e.message)
            pass
        new_rcff = RCFF(self.midi_file, tempo, instrument)
        for note in notes:
            # print("note")
            new_rcff = self.create_time_slices_from_note(new_rcff, note)
        return new_rcff

    @staticmethod
    def extract_data(track):
        notes = []  # [(time, length, pitch, velocity)]
        time = 0
        tempo = 0
        pitch_started = {}
        volume = -1
        instrument = -1
        found_instrument = False
        for event in track:
            # Used to find event types for tests. Don't remove.
            # print event

            time += event.tick
            if not found_instrument and (type(event) is midi.ProgramChangeEvent):
                found_instrument = True
                # TODO: Replace these magic numbers with consts
                if event.data[0] < 57 or event.data[0] > 80:
                    raise RuntimeError('not a single voice instrument')
                instrument = event.data[0]

            if type(event) is midi.NoteEvent:
                # print("b")
                volume = event.get_velocity

            if type(event) is midi.NoteOnEvent:
                pitch_started[event.pitch] = time

            if type(event) is midi.NoteOffEvent:
                # print("c")
                try:
                    start_time = pitch_started[event.pitch]
                    length = time - start_time
                    notes.append((time, length, event.pitch, volume))
                except KeyError:
                    pass
            if type(event) is midi.SetTempoEvent:
                tempo = event.get_bpm()

        return instrument, tempo, notes

    @staticmethod
    def create_time_slices_from_note(rcff, note):
        time, length, pitch, volume = note
        for i in range(0, length):
            if i == 0:
                rcff.add_time_slice_to_body(TimeSlice(pitch, volume, 9))
            else:
                rcff.add_time_slice_to_body(TimeSlice(pitch, volume, 0))
            # TODO: This i += .125 currently doesn't do anything (According to the tests)
            i += 0.125
        return rcff
