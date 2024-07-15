from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Peak'
        default = self.test_key(key, 1)  # ns
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
