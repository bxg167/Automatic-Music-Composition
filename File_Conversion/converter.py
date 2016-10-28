import pickle
import array
from TimeSlice import TimeSlice
from RCFF import RCFF
import midi
import os

class converter():
        def __init__(self, midi_file):
                self.midi_file = midi_file
                self.files = []

        def create_rcff_files(self):
                pattern = midi.read_midifile(self.midi_file)
                num_tracks = 0
                for track in pattern:
                        print("track")
                        num_tracks += 1
                        instrument = -1
                        notes = []
                        tempo = -1
                        try:
                                instrument, tempo, notes = self.extract_data(track)
                        except RuntimeError as e:
                                pass #print(e.message)
                        self.new_rcff = RCFF(self.midi_file, tempo, instrument)
                        for note in notes:
                                print("note")
                                self.new_rcff = self.create_time_slices_from_note(self.new_rcff, note)
                        #if not( self.new_rcff.check_for_excessive_rest):
                        self.files.append(self.new_rcff)
                i =0
                print(self.files)
                for file in self.files:
                        print("file")
                        f = open(self.midi_file + str(i), "w")
                        pickle.dump(file,f)
                        i+=1

        def extract_data(self,track):
                notes = [] # [(time, length, pitch, velocity)]
                time = 0
                tempo = 0
                pitch_started = {}
                volume=-1
                instrument = -1
                found_instrument = False
                for event in track:
                        time += event.tick
                        if not found_instrument and (type(event) is midi.ProgramChangeEvent):
                                found_instrument = True
                                if event.data[0] < 57 or event.data[0] > 80 :
                                        raise RuntimeError('not a single voice instrument')
                                instrument = event.data[0]
                                print("a")
                        if(type(event) is midi.NoteEvent):
                                volume = event.get_velocity
                                print("b")
                        if (type(event) is midi.NoteOnEvent):
                                pitch_started[event.pitch] = time
                        if (type(event) is midi.NoteOffEvent):
                                print("c")
                                try:
                                        start_time = pitch_started[event.pitch]
                                        length = time - start_time
                                        notes.append((time, length, event.pitch, volume))
                                except KeyError:
                                        pass
                        if(type (event) is midi.SetTempoEvent):
                                tempo = event.get_bpm()
                return instrument, tempo, notes

        def create_time_slices_from_note(self,rcff,note):
                time, length, pitch, volume = note
                for i in range (0, length):
                        if i == 0:
                                rcff.add_time_slice_to_body(TimeSlice(pitch,volume,9))
                        else:
                                rcff.add_time_slice_to_body(TimeSlice(pitch,volume,0))
                        i = i + 0.125
                return rcff
