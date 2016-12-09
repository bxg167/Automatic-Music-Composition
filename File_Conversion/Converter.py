from __future__ import print_function
import os

import midi
import math

from RCFF import RCFF
from TimeSlice import *

MIN_SINGLE_VOICE_RANGE = 57
MAX_SINGLE_VOICE_RANGE = 80


class Converter:
    def __init__(self, midi_file):
        self.__midi_file = midi_file

        self.__pattern = []
        if os.path.isfile(midi_file):
            self.__pattern = midi.read_midifile(self.__midi_file)
            fr = midi.FileReader()
            self.resolution = self.__pattern.resolution
        else:
            raise Exception("The file passed doesn't exist")

    def create_rcff_files(self):
        rcff_files = []

        num_tracks = 0

        tempo = self.__extract_tempo__(self.__pattern[0])
        print("tempo: " + str(tempo))

        for track in self.__pattern:
            print("\nNEXT TRACK")
            num_tracks += 1

            new_rcff = self.__create_rcff_file__(track, tempo)

            if new_rcff.check_for_excessive_rest():
                rcff_files.append(new_rcff)
                print("RCFF successfully created")
            else:
                print("FAILED: RCFF not generated")

        return rcff_files

    def __create_rcff_file__(self, track, tempo):
        instrument = -1
        notes = []
        try:
            instrument, notes = self.__extract_data__(track)

        except RuntimeError as e:
            print(e.message)
            pass
        
        new_rcff = RCFF(self.__midi_file, tempo, instrument)

        self.__add_rest_before_first_note__(new_rcff, notes)

        for note_pos in range(0, len(notes)):
            note = notes[note_pos]
            if note_pos > 0:
                last_note = notes[note_pos - 1]
                self.__create_rest_time_slices__(new_rcff, last_note, note)

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
        pitch_started = {}
        volume = -1
        instrument = -1
        found_instrument = False

        for event in track:
            time += event.tick
            if not found_instrument and (type(event) is midi.ProgramChangeEvent):
                found_instrument = True
                if event.data[0] < MIN_SINGLE_VOICE_RANGE or event.data[0] > MAX_SINGLE_VOICE_RANGE:
                    raise RuntimeError('not a single voice instrument')
                instrument = event.data[0]

            if type(event) is midi.NoteOnEvent:
                pitch_started[event.pitch] = time
                volume = event.get_velocity.im_self.velocity

            if type(event) is midi.NoteOffEvent:
                if event.pitch in pitch_started:
                    start_time = pitch_started[event.pitch]
                    length = time - start_time
                    notes.append((time, length, event.pitch, volume))
                    pitch_started.pop(event.pitch)

        return instrument, notes

    def __create_time_slice__(self, rcff, num_timeslices, pitch, volume, timeslice_type):
        rcff.add_time_slice_to_body(TimeSlice(pitch, volume, BEGIN))
        for i in range(0, num_timeslices):
            rcff.add_time_slice_to_body(TimeSlice(pitch, volume, timeslice_type))

        rcff.add_time_slice_to_body(TimeSlice(pitch, volume, END))

        return rcff

    def __create_time_slices_from_note__(self, rcff, note):
        time, length, pitch, volume = note

        tick_increment = self.__get_tick_increment__(rcff)
        num_slices = int(math.ceil(length / tick_increment))

        note_type = BEAT
        if volume == 0:
            note_type = REST

        rcff = self.__create_time_slice__(rcff, num_slices, pitch, volume, note_type)


        return rcff

    def __create_rest_time_slices__(self, rcff, previous_note, next_note):
        prev_time, prev_length, prev_pitch, prev_volume = previous_note
        next_time, next_length, next_pitch, next_volume = next_note

        rest_start_time = prev_time
        rest_end_time = next_time - next_length

        length = rest_end_time - rest_start_time
        if length > 0:
            tick_increment = self.__get_tick_increment__(rcff)
            num_slices = int(math.ceil(length / tick_increment))
            rcff = self.__create_time_slice__(rcff, num_slices, 0, 0, REST)

        return rcff

    def __add_rest_before_first_note__(self, rcff, notes):
        if len(notes) == 0:
            return

        time, length, pitch, volume = notes[0]

        # The time variable indicates the time the song is at after the note has been played (length of note).
        if time != length:
            tick_increment = self.__get_tick_increment__(rcff)
            num_slices = int(math.ceil(time / tick_increment))
            rcff = self.__create_time_slice__(rcff, num_slices, 0, 0, REST)

        return rcff

    def __get_tick_increment__(self, rcff): 
        return self.resolution /4

