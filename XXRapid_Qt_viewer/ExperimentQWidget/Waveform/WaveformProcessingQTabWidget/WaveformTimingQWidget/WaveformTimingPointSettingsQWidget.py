from XXRapid_Qt_viewer.utility.SettingsBoxQWidget import *


class WaveformTimingPointSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)

        try:
            default = settings_dict['Time']
        except:
            default = 0
        self.TimeSettingsQWidget = SettingsLineQWidget(
            name='Time',
            default=default,
            limit=[-1e6, 1e6],
            step=1.0,
            comment='ns'
        )

        self.SettingsDict['Time'] = self.TimeSettingsQWidget.value

        self.TimeSettingsQWidget.changed.connect(self.OnTimeSettingsQWidget)
        self.QVBoxLayout.addWidget(self.TimeSettingsQWidget)

    def OnTimeSettingsQWidget(self):
        self.SettingsDict['Time'] = self.TimeSettingsQWidget.value
        self.changed.emit()
