from XXRapid_Qt_viewer.utility.SettingsBoxQWidget import *


class WaveformResistiveVoltageSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key = 'Peak'
        default = 1
        if key in settings_dict.keys():
            default = settings_dict['Peak']
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
        self.SettingsDict['Peak'] = self.PeakSettingsLine.value
        super().OnSettingsLineChanged()
