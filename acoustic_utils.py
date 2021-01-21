import math

C4 = 60

def amplitudeToVolume(amp):
    """Converts amplitude (0-1) to volume (-inf-0)dB"""
    if amp == 0:
        return float('-inf')
    return 20 * math.log10(amp)

def noteToFrequency(note):
    """Converts MIDI note number (c4=60) to frequency in Hz"""
    #a3 = note 57 = 220Hz
    return 220 * (2 ** ((note-57) / 12.0))