import acoustic_utils

class ChromaticSpectrum:
    """For representing a sound spectrum that has a loudness value at each note
    (represented by an integer as in MIDI, C4=60).
    We can use this rather artificial construct to approximate basic waveforms
    in a way compatible with tonewheel organs. Tomewheel organ "harmonics" are not actually
    harmonic - they are equally tempered pitches. The ideal sawtooth wave matches
    drawbar frequencies only at the octaves (white drawbars)."""
    def value(self, note):
        return float('-inf')

class RootedWaveform(ChromaticSpectrum):
    def __init__(self, root):
        self.root = root
    def value(self, note):
        offset = note - self.root
        return self.valueAtOffset(offset)
    def valueAtOffset(self, offset):
        return float('-inf')

# The None values fall between notes and have to be ignored. Similarly, it's not very
# useful to go above 48 (the offset of the last drawbar) with this approach.
harmonicOffsets = [0, 12, 19, 24, 28, 31, 34, 36, 38, 40, None, 43, None, None, None, 48]

class SawtoothWave(RootedWaveform):
    def valueAtOffset(self, offset):
        if offset != None and offset in harmonicOffsets:
            harmIndex = harmonicOffsets.index(offset)
            amplitude = 1.0 / (harmIndex + 1)
            return acoustic_utils.amplitudeToVolume(amplitude)
        else:
            return float('-inf')

class SquareWave(RootedWaveform):
    def valueAtOffset(self, offset):
        if offset != None and offset in harmonicOffsets:
            harmIndex = harmonicOffsets.index(offset)
            if harmIndex % 2 == 1:
                return float('-inf')
            amplitude = 1.0 / (harmIndex + 1)
            return acoustic_utils.amplitudeToVolume(amplitude)
        else:
            return float('-inf')

class TriangleWave(RootedWaveform):
    def valueAtOffset(self, offset):
        if offset != None and offset in harmonicOffsets:
            harmIndex = harmonicOffsets.index(offset)
            amplitude = 1.0 / ((harmIndex + 1) ** 2)
            return acoustic_utils.amplitudeToVolume(amplitude)
        else:
            return float('-inf')

class InfiniteEnergy(RootedWaveform):
    def valueAtOffset(self, offset):
        return 0

class FullVolumeDrawbars(RootedWaveform):
    def valueAtOffset(self, offset):
        from tonewheel import Tonewheel
        organ = Tonewheel()
        if offset in organ.drawbarOffsets:
            i = organ.drawbarOffsets.index(offset)
            return organ.drawbarVolumes[i][organ.numSettings - 1]
        return float('-inf')


if __name__ == '__main__':
    import tonewheel
    from acoustic_utils import C4
    saw1 = SawtoothWave(C4)
    saw2 = SawtoothWave(C4 + 12)
    square1 = SquareWave(C4)
    square2 = SquareWave(C4 + 12)
    triangle1 = TriangleWave(C4)
    triangle2 = TriangleWave(C4 + 12)
    organ = tonewheel.Tonewheel()

    print "Representing basic waveforms using tonewheel drawbars"
    print "For each waveform, try two approaches: Using drawbar 1 as the fundamental, or drawbar 3"
    print "Sawtooth wave:"
    print organ.approximateChromaticSpectrumAtNote(saw1, C4)
    print organ.approximateChromaticSpectrumAtNote(saw2, C4)
    print "Square wave:"
    print organ.approximateChromaticSpectrumAtNote(square1, C4)
    print organ.approximateChromaticSpectrumAtNote(square2, C4)
    print "Triangle wave:"
    print organ.approximateChromaticSpectrumAtNote(triangle1, C4)
    print organ.approximateChromaticSpectrumAtNote(triangle2, C4)
    print "(Debugging)"
    print "Full energy spectrum:"
    print organ.approximateChromaticSpectrumAtNote(InfiniteEnergy(C4), C4)
    print organ.approximateChromaticSpectrumAtNote(InfiniteEnergy(C4+12), C4)
    print "Full drawbars:"
    print organ.approximateChromaticSpectrumAtNote(FullVolumeDrawbars(C4), C4)
    print organ.approximateChromaticSpectrumAtNote(FullVolumeDrawbars(C4+12), C4)   