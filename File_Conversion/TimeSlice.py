REST = 0
BEAT = 1
BEGIN = 9
END = 8


class TimeSlice(object):
    def __init__(self, pitch, volume, message):
        self.pitch = pitch
        self.volume = volume
        self.message = message
    
    def __str__(self):
        message_str = 'INVALID'
        if self.message == 0:
            message_str = 'REST'
        elif self.message == 1:
            message_str = 'BEAT'
        elif self.message == 9:
            message_str = 'BEGIN'
        elif self.message == 8:
            message_str = 'END'
        message_str += ' '
        message_str += str(self.pitch)
        message_str += ' at '
        message_str += str(self.volume)
        return message_str
        
