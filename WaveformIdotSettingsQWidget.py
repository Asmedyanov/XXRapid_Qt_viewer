from SettingsBoxQWidget import *


class WaveformIdotSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        try:
            default = settings_dict['Smoothing']
        except:
            default = 1
        self.SmoothingSettingsLine = SettingsLineQWidget(
            name='Smoothing',
            default=default,
            limit=[0.2, 2000],
            step=0.2,
            comment='ns'
        )
        self.QVBoxLayout.addWidget(self.SmoothingSettingsLine)
        self.SettingsDict['Smoothing'] = self.SmoothingSettingsLine.value
        self.SmoothingSettingsLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['Peak']
        except:
            default = 1
        self.PeakSettingsLine = SettingsLineQWidget(
            name='Peak',
            default=default,
            limit=[0.2, 2000],
            step=0.2,
            comment='ns'
        )
        self.QVBoxLayout.addWidget(self.PeakSettingsLine)
        self.SettingsDict['Peak'] = self.PeakSettingsLine.value
        self.PeakSettingsLine.changed.connect(self.OnSettingsLineChanged)

    def OnSettingsLineChanged(self):
        self.SettingsDict['User_comment'] = self.User_comment.value
        self.SettingsDict['Smoothing'] = self.SmoothingSettingsLine.value
        self.SettingsDict['Peak'] = self.PeakSettingsLine.value
        self.changed.emit()
