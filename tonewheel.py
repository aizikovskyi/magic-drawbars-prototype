# Parameters for a tonewheel engine. Currently hardcoded
# using imprecise data from my stage keyboard.
# Support for different models will be straightforward to add when required.

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
        # These were listed backwards, so reverse them...
        for volList in self.drawbarVolumes:
            volList.reverse()
        # Now self.drawbarVolumes[0][0] corresponds to drawbar 1, setting 1.
