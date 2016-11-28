import os

import midi

from RCFF import RCFF


class ConvertRcffToMidi:
    def __init__(self, rcff_file):
        self.__rcff_file = rcff_file

        self.__rcff = []

        if os.path.isfile(rcff_file):
            self.__rcff = RCFF.unpickle(open(self.__rcff_file))
        else:
            raise Exception("The file passed doesn't exist")

    def create_midi(self):
        r = self.__rcff

        # Instantiate a MIDI Pattern (contains a list of tracks)
        pattern = midi.Pattern(format=1, resolution=480)
        # TODO: We need to know resolution to get it to play at the right pace
        # TODO: Resolution defaults to 220
        # Instantiate a MIDI Track (contains a list of MIDI events)
        track = midi.Track()
        # Append the track to the pattern
        pattern.append(track)

        # Assign instrument information. If we don't do this, it would default to piano
        inst = midi.ProgramChangeEvent(value=r.instrument)
        track.append(inst)

        # counters for loop
        last_message = -1
        slice_count = 0
        pitch = 60  # Concert C
        # see ticks/slice explanation in Converter.__create_time_slices_from_note__
        ticks_per_time_slice = 125     # set default to 120 bpm
        if r.tempo > 0:
            ticks_per_time_slice = 15000 / r.tempo

        # Iterate over timeslices in RCFF, creating midi note events as appropriate
        for timeSlice in r.body:
            if timeSlice.message == 9:
                # we're at a new note, so we should write the old one off
                if last_message != -1:
                    # Instantiate a MIDI note off event, append it to the track
                    net_ticks = slice_count * ticks_per_time_slice
                    off = midi.NoteOffEvent(tick=net_ticks, pitch=pitch)
                    track.append(off)
                # now start the new note
                pitch = timeSlice.pitch
                slice_count = 1
                # Instantiate a MIDI note on event, append it to the track
                on = midi.NoteOnEvent(tick=0, velocity=timeSlice.volume, pitch=pitch)
                track.append(on)
            else:   # message==0, the note is being sustained
                slice_count += 1
            last_message = timeSlice.message

        # After the last timeSlice is read, add one last off event
        net_ticks = slice_count * ticks_per_time_slice
        off = midi.NoteOffEvent(tick=net_ticks, pitch=pitch)
        track.append(off)

        # Signal the end of the track
        eot = midi.EndOfTrackEvent(tick=1)
        track.append(eot)

        return pattern


# The run function does the work that the gui should do: It collects a path for an rcff, makes an RCFF object,
# creates a midi file from it, and saves that midi in a file
def run(rcff_file_path, save_in_dir_path):
    c = ConvertRcffToMidi(rcff_file_path)
    midi_object = c.create_midi()
    # The midi file should be written from the GUI, just as rcff files are. For now, we'll leave it here
    midi.write_midifile(os.path.join(save_in_dir_path, "example.mid"), midi_object)
    # TODO: Check that we don't override midi files


# hardcoded right now, sorry
run("C:\\Users\\Cassidy\\PycharmProjects\\Automatic-Music-Composition\\RCFF_Test\\RCFF_Files\\output_4notes_1.rcff",
    "C:\\Users\\Cassidy\\PycharmProjects\\Automatic-Music-Composition\\RCFF_Test\\RCFF_Files")


# CONSIDERATIONS
#
# 1. create_midi_file takes an RCFF object and makes a corresponding midi object
#      - Do we want to retrieve that RCFF from self? Or just pass it in as an argument?
# 2. Should we expect an RCFF file or object? (in __init__)
#      - The RNN gives us an object, right? So we may as well take an object here and save ourselves the pickling
