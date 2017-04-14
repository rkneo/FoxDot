""" Module for converting streams and frequencies """

import rtmidi
from rtmidi import midiconstants

TIMING_CLOCK          = midiconstants.TIMING_CLOCK
SONG_POSITION_POINTER = midiconstants.SONG_POSITION_POINTER
SONG_START            = midiconstants.SONG_START

def miditofreq(midinote):
    """ Converts a midi number to frequency """
    return 440 * (2 ** ((midinote - 69.0)/12.0))

midi2cps = miditofreq

def midi(scale, octave, degree, root=0, stepsPerOctave=12):
    """ Calculates a midinote from a scale, octave, degree, and root """

    # Force float
    try:
        degree = float(degree)
    except TypeError as e:
        print degree, type(degree)
        raise TypeError(e)

    # Floor val
    lo = int(degree)
    hi = lo + 1

    octave = octave + (lo / len(scale))

    chroma = range(stepsPerOctave)

    scale_val = (scale[hi % len(scale)] - scale[lo % len(scale)]) * ((degree-lo)) + scale[lo % len(scale)]

    return scale_val + (octave * len(chroma)) + float(root)


class MidiIn:
    metro = None
    def __init__(self, port_id=0):
        """ Class for listening for MIDI clock messages
            from a midi device """
        self.device = rtmidi.MidiIn()

        self.available_ports = self.device.get_ports()

        if not self.available_ports:

            raise MIDIDeviceNotFound

        else:

            print("MidiIn: Connecting to " + self.available_ports[port_id])

        self.device.open_port(port_id)
        self.device.ignore_types(timing=False)

        self.pulse = 0
        self.delta = 0.0
        self.bpm   = 120.0
        self.ppqn  = 24
        self.beat  = 0

    def update(self):
        data = self.device.get_message()
        if data is not None:
            datatype, delta = data
            if TIMING_CLOCK in datatype:
                self.pulse += 1
                self.delta += delta
                if self.pulse == self.ppqn:
                    self.bpm = 60.0 / self.delta
                    self.pulse = 0
                    self.delta = 0.0
            elif SONG_POSITION_POINTER in datatype:
                self.metro.set_time(datatype[1] / 4)
        return

    def get_beat(self):
        """ If a beat value has been set, return it, otherwise return None """
        val, self.beat = self.beat, None
        return val

    def close(self):
        """ Closes the active port """
        self.device.close_port()
        return
                
            

class MidiOut:
    pass


class MIDIDeviceNotFound(Exception):
    def __str__(self):
        return self.__class__.__name__ + " Error"


if __name__ == "__main__":

    a = MidiIn()

    


        
