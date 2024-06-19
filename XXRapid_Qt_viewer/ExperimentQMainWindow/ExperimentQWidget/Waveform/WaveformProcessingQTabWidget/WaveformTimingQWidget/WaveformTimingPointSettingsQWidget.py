from SettingsQWidgets.SettingsBoxQWidget import *


class WaveformTimingPointSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        key = 'Time'
        default = 0
        if key in settings_dict.keys():
            default = int(float(settings_dict[key]))
        self.TimeSettingsQWidget = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[-1e6, 1e6],
            step=1.0,
            comment='ns'
        )
        self.SettingsDict[key] = self.TimeSettingsQWidget.value
        self.TimeSettingsQWidget.changed.connect(self.OnTimeSettingsQWidget)
        self.QVBoxLayout.addWidget(self.TimeSettingsQWidget)

    def OnTimeSettingsQWidget(self):
        self.SettingsDict['Time'] = self.TimeSettingsQWidget.value
        self.changed.emit()
