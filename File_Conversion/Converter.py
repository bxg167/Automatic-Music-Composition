import os

import midi

from RCFF import RCFF
from TimeSlice import TimeSlice
REST = 8
SUSTAINED=0
BEGIN =9
MIN_SINGLE_VOICE_RANGE=57
MAX_SINGLE_VOICE_RANGE=80

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
        tempo = self.__extract_tempo__(self.__pattern[0])
        print(tempo)
        for track in self.__pattern:
            print("track")
            num_tracks += 1

            new_rcff = self.__create_rcff_file__(track,tempo)

            # TODO: BUG 1.2
            if ( new_rcff.check_for_excessive_rest):
                rcff_files.append(new_rcff)

        return rcff_files

    def __create_rcff_file__(self, track,tempo):
        instrument = -1
        notes = []
        try:
            instrument, notes = self.__extract_data__(track)

            # TODO: BUG 1.2
            #print tempo
        except RuntimeError as e:
            print(e.message)
            pass
        # Do we want to give the RCFF a unique name here? Like RCFF(self.__midi_file + ID, tempo, instrument)?
        # This will allow us to test for 2.1.8 automatically, if not, then we can just run this test case manually
        new_rcff = RCFF(self.__midi_file, tempo, instrument)

        for note in notes:
            new_rcff = self.__create_time_slices_from_note__(new_rcff, note)
        return new_rcff

    @staticmethod
    def __extract_tempo__(track):
       for event in track:
            if type(event) is midi.SetTempoEvent:
                return event.get_bpm()

    @staticmethod
    def __extract_data__(track):
        notes = []  # [(time, length, pitch, velocity)]
        time = 0
        #tempo = 0
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
                if event.data[0] < MIN_SINGLE_VOICE_RANGE or event.data[0] > MAX_SINGLE_VOICE_RANGE:
                    raise RuntimeError('not a single voice instrument')
                instrument = event.data[0]

            # This never activates because type(xxx) is yyy doesn't work with inheritance, which is what I think this method was going for.
            # Along with that, the volume is specified in the NoteOnEvent, NoteOffEvent does have a volume, but it is always 0
            # if type(event) is midi.NoteEvent:
            #     # print("b")
            #     volume = event.get_velocity

            if type(event) is midi.NoteOnEvent:
                pitch_started[event.pitch] = time
                volume = event.get_velocity.im_self.velocity

            if type(event) is midi.NoteOffEvent:
                # print("c")
                try:
                    start_time = pitch_started[event.pitch]
                    length = time - start_time
                    notes.append((time, length, event.pitch, volume))
                except KeyError:
                    pass
            #if type(event) is midi.SetTempoEvent:
                #tempo = event.get_bpm()

        return instrument, notes

    @staticmethod
    def __create_time_slices_from_note__(rcff, note):
        time, length, pitch, volume = note

        # note length is in ticks (milliseconds),but we want a TimeSlice for each quarter of a beat (a 16th note, generally)
        # (.25 beats/TimeSlice * 60000 ticks/minute) / (tempo bpm) ==> ticks per TimeSlice
        tickIncrement = 125     # default to 120 bpm
        if rcff.tempo != 0:
            tickIncrement = int(15000 / (rcff.tempo))

        # Begin note
        rcff.add_time_slice_to_body(TimeSlice(pitch, volume, 9))
        for i in range(0, length, tickIncrement):
            # Sustain note
            rcff.add_time_slice_to_body(TimeSlice(pitch, volume, 0))
        # End note
        rcff.add_time_slice_to_body(TimeSlice(pitch, volume, 8))

        return rcff