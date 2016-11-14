class TimeSlice:
    def __init__(self, pitch, volume, message):
        self.pitch = pitch
        self.volume = volume
        self.message = message

    # TODO: Test
    def equals(self, other_timeslice):
        if type(other_timeslice) != TimeSlice:
            return False
        isEqual = self.pitch == other_timeslice.pitch
        isEqual &= self.volume == other_timeslice.volume
        isEqual &= self.message == other_timeslice.message

        return isEqual
