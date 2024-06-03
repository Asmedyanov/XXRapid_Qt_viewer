from SettingsQWidgets.SettingsBoxQWidget import *


class WaveformIdotSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key = 'Smoothing'
        default = dict()
        if key in settings_dict.keys():
            default = int(float(settings_dict[key]))
        self.SmoothingSettingsLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 2000],
            step=1,
            comment='ns'
        )
        self.QVBoxLayout.addWidget(self.SmoothingSettingsLine)
        self.SettingsDict[key] = self.SmoothingSettingsLine.value
        self.SmoothingSettingsLine.changed.connect(self.OnSettingsLineChanged)

    def OnSettingsLineChanged(self):
        self.SettingsDict['Smoothing'] = self.SmoothingSettingsLine.value
        super().OnSettingsLineChanged()
