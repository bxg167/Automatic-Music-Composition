from TimeSlice import TimeSlice

class RCFF(): 
	
	def _init_(self, midi_file, tempo, instrument): 
		self.midi_file=midi_file
		self.tempo=tempo
		self.instrument=instrument
		self.body = []

	def add_time_slice_to_body(self, timeslice):
		self.body.append(timeslice)

	def check_for_excessive_rest(self):
		count = 0
		for slice in self.body:
			if(slice.message == 8):
				count = count +1
		return count > (.5 * len(self.body))
		