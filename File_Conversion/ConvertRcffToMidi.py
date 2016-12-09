import os

import midi
import TimeSlice

from RCFF import RCFF


class ConvertRcffToMidi:
    def __init__(self, rcff_file_path, instrument=0):
        self.__rcff_file = rcff_file_path

        self.__rcff = []

        if os.path.isfile(rcff_file_path):
            with open(self.__rcff_file, 'rb') as rcff_file:
                self.__rcff = RCFF.unpickle(rcff_file)
                self.__rcff.instrument = instrument
        else:
            raise Exception("The file passed doesn't exist")

    # for testing purposes
    def __set_rcff__(self,rcff):
        self.__rcff = rcff

    def create_midi(self):
        r = self.__rcff

        pattern = midi.Pattern(format=1, resolution=480)

        # Instantiate a MIDI Track (contains a list of MIDI events)
        track = midi.Track()

        pattern.append(track)

        # Assign instrument information. If we don't do this, it would default to piano
        if r.instrument > 0:
            inst = midi.ProgramChangeEvent(value=r.instrument)
            track.append(inst)

        # counters for loop
        slice_count = 0
        pitch = 60  # Concert C
        volume = 0
        ticks_per_time_slice = pattern.resolution / 4

        # Iterate over timeslices in RCFF, creating midi note events as appropriate
        for timeSlice in r.body:
            if timeSlice.message == TimeSlice.BEGIN:

                # Set up tracking variables
                slice_count = 0
            elif timeSlice.message == TimeSlice.END:
                # Create NoteOnEvent for the note now that we know the volume and pitch
                on = midi.NoteOnEvent(tick=0, velocity=volume, pitch=pitch)
                track.append(on)

                length = slice_count * ticks_per_time_slice

                # Add corresponding NoteOffEvent after appropriate ticks
                off = midi.NoteOffEvent(tick=length, pitch=pitch)
                track.append(off)

            elif timeSlice.message == TimeSlice.BEAT:
                slice_count += 1
                pitch = timeSlice.pitch
                volume = timeSlice.volume + 100
            else:   # timeSlice.message == TimeSlice.REST
                slice_count += 1
                volume = 0

        # Signal the end of the track
        eot = midi.EndOfTrackEvent(tick=1)
        track.append(eot)

        return pattern

# CONSIDERATIONS
#
# 1. create_midi_file takes an RCFF object and makes a corresponding midi object
#      - Do we want to retrieve that RCFF from self? Or just pass it in as an argument?
# 2. Should we expect an RCFF file or object? (in __init__)
#      - The RNN gives us an object, right? So we may as well take an object here and save ourselves the pickling
