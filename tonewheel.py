# Parameters for a tonewheel engine. Currently hardcoded
# using imprecise data from my stage keyboard.
# Support for different models will be straightforward to add when required.
# This data is VERY inaccurate; but at the same time, having only 8 discrete settings
# per drawbar means that we can get away with low accuracy.

class Tonewheel:
    def __init__(self):
        self.numDrawbars = 9
        self.numSettings = 8 # not including setting 0, which is always -inf dB
        self.drawbarOffsets = [0, 19, 12, 24, 31, 36, 40, 43, 48]
        self.drawbarVolumes = [
            [-0.33, -1.9, -3.4, -5.1, -7.5, -10.0, -12.6, -15.5],
            [-3.16, -4.7, -6.2, -7.65, -10.0, -12.7, -15.3, -18.2],
            [-2.25, -3.7, -5.24, -6.93, -9.36, -11.8, -14.4, -17.3],
            [-3.25, -4.74, -6.09, -7.78, -10.2, -12.6, -15.4, -18.3],
            [-3.72, -5.2, -6.7, -8.23, -10.6, -13.2, -15.8, -18.8],
            [-5.24, -6.7, -8.23, -9.7, -12.2, -14.8, -17.3, -20.1],
            [-6.93, -8.4, -9.92, -11.4, -13.9, -16.45, -18.9, -21.6],
            [-6.7, -8.5, -10.0, -11.7, -14.1, -16.5, -19.1, -21.9],
            [-9.6, -11.1, -12.7, -14.3, -16.7, -19.0, -21.6, -24.0]
        ]
        self.highestVolume = -0.33
        # These were listed backwards, so reverse them...
        for volList in self.drawbarVolumes:
            volList.reverse()
        # Now self.drawbarVolumes[0][0] corresponds to drawbar 1, setting 1.
    
    def approximateChromaticSpectrumAtNote(self, spectrum, note):
        """Will normalize the output so that the "loudest" drawbar is at max setting"""
        spectrumVolumes = [spectrum.value(note + offset) for offset in self.drawbarOffsets]
        excessVolumes = [spectrumVolumes[x] - self.drawbarVolumes[x][-1] for x in range(self.numDrawbars)]
        largestExcess = max(excessVolumes)
        spectrumVolumes = [vol - largestExcess for vol in spectrumVolumes]
        drawbarSettings = []
        for i in range(self.numDrawbars):
            vol = spectrumVolumes[i]
            # Find the closest drawbar setting to this volume. How do we decide between settings 1 and 0?
            # For now, let's hardcode a 6dB threshhold (below the min drawbar volume)
            if vol < self.drawbarVolumes[i][0]:
                if (self.drawbarVolumes[i][0] - vol < 6):
                    drawbarSettings.append(1)
                else:
                    drawbarSettings.append(0)
                continue
            lower = 0
            for setting in range(1, self.numSettings):
                drawbarVol = self.drawbarVolumes[i][setting]
                if drawbarVol < vol:
                    lower = setting
                else:
                    upper = setting
                    lowerDiff = vol - self.drawbarVolumes[i][lower]
                    upperDiff = self.drawbarVolumes[i][upper] - vol
                    if lowerDiff < upperDiff:
                        drawbarSettings.append(lower + 1)
                    else:
                        drawbarSettings.append(upper + 1)
                    break
        return TonewheelSettings(self, drawbarSettings)




class TonewheelSettings:
    def __init__(self, tonewheel, drawbarValues):
        """DrawbarValues is indexed from 1 relative to Tonewheel. Drawbar value 0 is -inf"""
        self.tonewheel = tonewheel
        self.drawbarValues = drawbarValues
    def __str__(self):
        return ''.join([x and str(x) or '.' for x in self.drawbarValues])
