import os

import midi
import TimeSlice

from RCFF import RCFF


class ConvertRcffToMidi:
    def __init__(self, rcff_file, instrument=0):
        self.__rcff_file = rcff_file

        self.__rcff = []

        if os.path.isfile(rcff_file):
            self.__rcff = RCFF.unpickle(open(self.__rcff_file))
            self.__rcff.instrument = instrument
        else:
            raise Exception("The file passed doesn't exist")

    def create_midi(self):
        r = self.__rcff

        # Instantiate a MIDI Pattern (contains a list of tracks)
        pattern = midi.Pattern(format=1, resolution=480)
        # Instantiate a MIDI Track (contains a list of MIDI events)
        track = midi.Track()
        # Append the track to the pattern
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
        # print "volume\tpitch\tmessage"
        for timeSlice in r.body:
            # print timeSlice.volume, "\t", timeSlice.pitch, "\t\t", timeSlice.message
            if timeSlice.message == TimeSlice.BEGIN:
                # Set up tracking variables
                slice_count = 0
            elif timeSlice.message == TimeSlice.END:
                # Create NoteOnEvent for the note now that we know the volume and pitch
                on = midi.NoteOnEvent(tick=0, velocity=volume, pitch=pitch)
                track.append(on)
                # Calculate note length based on tracking variable
                length = slice_count * ticks_per_time_slice
                # Add corresponding NoteOffEvent after appropriate ticks
                off = midi.NoteOffEvent(tick=length, pitch=pitch)
                track.append(off)
            elif timeSlice.message == TimeSlice.BEAT:
                slice_count += 1
                pitch = timeSlice.pitch
                volume = timeSlice.volume
            else:   # timeSlice.message == TimeSlice.REST
                slice_count += 1
                volume = 0

        # Signal the end of the track
        eot = midi.EndOfTrackEvent(tick=1)
        track.append(eot)

        # print(pattern)
        return pattern


# The run function does the work that the gui should do: It collects a path for an rcff, makes an RCFF object,
# creates a midi file from it, and saves that midi in a file

def run(rcff_file_path, new_midi_location):
    c = ConvertRcffToMidi(rcff_file_path)
    midi_object = c.create_midi()

    # The midi file should be written from the GUI, just as rcff files are. For now, we'll leave it here
    if not os.path.exists(new_midi_location):
        midi.write_midifile(new_midi_location, midi_object)

# hardcoded right now, sorry
# run("C:\\Users\\Cassidy\\PycharmProjects\\Automatic-Music-Composition\\RCFF_Test\\RCFF_Files\\output_4notes_0.rcff",
#     "C:\\Users\\Cassidy\\PycharmProjects\\Automatic-Music-Composition\\RCFF_Test\\RCFF_Files\\converted4.mid")
# run("C:\\Users\\Cassidy\\PycharmProjects\\Automatic-Music-Composition\\2\\3_RCFF_Files\\3ravens3_0.rcff",
#     "C:\\Users\\Cassidy\\PycharmProjects\\Automatic-Music-Composition\\2\\3_RCFF_Files\\3ravens3_0.mid")


# CONSIDERATIONS
#
# 1. create_midi_file takes an RCFF object and makes a corresponding midi object
#      - Do we want to retrieve that RCFF from self? Or just pass it in as an argument?
# 2. Should we expect an RCFF file or object? (in __init__)
#      - The RNN gives us an object, right? So we may as well take an object here and save ourselves the pickling
