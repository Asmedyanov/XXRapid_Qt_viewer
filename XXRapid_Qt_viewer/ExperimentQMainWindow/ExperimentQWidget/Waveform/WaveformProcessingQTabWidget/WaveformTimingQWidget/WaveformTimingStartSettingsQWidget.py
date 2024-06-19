from .WaveformTimingPointSettingsQWidget import *


class WaveformTimingStartSettingsQWidget(WaveformTimingPointSettingsQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Start'
        super().__init__(self.parent)
