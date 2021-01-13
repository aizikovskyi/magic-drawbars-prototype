import math

C4 = 60

def amplitudeToVolume(amp):
    """Converts amplitude (0-1) to volume (-inf-0)dB"""
    if amp == 0:
        return float('-inf')
    return 20 * math.log(amp)