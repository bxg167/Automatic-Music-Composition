REST = 0
BEAT = 1
BEGIN = 9
END = 8


class TimeSlice:
    def __init__(self, pitch, volume, message):
        self.pitch = pitch
        self.volume = volume
        self.message = message
