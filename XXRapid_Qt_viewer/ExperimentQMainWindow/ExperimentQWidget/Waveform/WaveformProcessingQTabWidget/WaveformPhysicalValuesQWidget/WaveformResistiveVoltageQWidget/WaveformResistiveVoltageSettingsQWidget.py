from SettingsQWidgets.SettingsBoxQWidget import *


class WaveformResistiveVoltageSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key = 'Peak'
        default = 1
        if key in settings_dict.keys():
            default = int(float(settings_dict[key]))
        self.PeakSettingsLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 2000],
            step=1,
            comment='ns'
        )
        self.QVBoxLayout.addWidget(self.PeakSettingsLine)
        self.SettingsDict[key] = self.PeakSettingsLine.value
        self.PeakSettingsLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Peak'] = self.PeakSettingsLine.value
        super().on_settings_line_changed()
