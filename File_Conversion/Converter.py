import os

import midi

from RCFF import RCFF
from TimeSlice import TimeSlice


class Converter:
    def __init__(self, midi_file):
        self.__midi_file = midi_file

        self.__pattern = []

        if os.path.isfile(midi_file):
            self.__pattern = midi.read_midifile(self.__midi_file)
        else:
            raise Exception("The file passed doesn't exist")

    def create_rcff_files(self):
        rcff_files = []

        num_tracks = 0

        for track in self.__pattern:
            # print("track")
            num_tracks += 1

            new_rcff = self.__create_rcff_file__(track)

            # TODO: BUG 1.2
            # if not( new_rcff.check_for_excessive_rest):
            rcff_files.append(new_rcff)

        return rcff_files

    def __create_rcff_file__(self, track):
        instrument = -1
        notes = []
        tempo = -1
        try:

            instrument, tempo, notes = self.__extract_data__(track)

            # TODO: BUG 1.2
            # print tempo
        except RuntimeError as e:
            # print(e.message)
            pass
        new_rcff = RCFF(self.__midi_file, tempo, instrument)

        print ("Start")
        for note in notes:
            new_rcff = self.__create_time_slices_from_note__(new_rcff, note)
        return new_rcff

    @staticmethod
    def __extract_data__(track):
        notes = []  # [(time, length, pitch, velocity)]
        time = 0
        tempo = 0
        pitch_started = {}
        volume = -1
        instrument = -1
        found_instrument = False
        for event in track:
            # Used to find event types for tests.
            # print event

            time += event.tick
            if not found_instrument and (type(event) is midi.ProgramChangeEvent):
                found_instrument = True
                # TODO: BUG 1.4
                if event.data[0] < 57 or event.data[0] > 80:
                    raise RuntimeError('not a single voice instrument')
                instrument = event.data[0]

            elif type(event) is midi.NoteEvent:
                # print("b")
                volume = event.get_velocity

            elif type(event) is midi.NoteOnEvent:
                pitch_started[event.pitch] = time

            elif type(event) is midi.NoteOffEvent:
                # print("c")
                try:
                    start_time = pitch_started[event.pitch]
                    length = time - start_time
                    notes.append((time, length, event.pitch, volume))
                except KeyError:
                    pass
            elif type(event) is midi.SetTempoEvent:
                tempo = event.get_bpm()

        return instrument, tempo, notes

    @staticmethod
    def __create_time_slices_from_note__(rcff, note):
        time, length, pitch, volume = note

        for i in range(0, length):

            #TODO: BUG 1.7
            if i == 0:
                rcff.add_time_slice_to_body(TimeSlice(pitch, volume, 9))
            else:
                rcff.add_time_slice_to_body(TimeSlice(pitch, volume, 0))

            #TODO: BUG 1.5
            i += .125

        return rcff
