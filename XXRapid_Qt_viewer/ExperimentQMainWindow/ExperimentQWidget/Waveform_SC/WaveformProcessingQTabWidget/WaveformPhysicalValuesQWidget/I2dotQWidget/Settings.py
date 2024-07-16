from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Smoothing'
        default = self.test_key(key, 5)  # ns
        self.SmoothingSettingsLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 2000],
            step=1,
            comment='ns'
        )
        self.QVBoxLayout.addWidget(self.SmoothingSettingsLine)
        self.SettingsDict[key] = self.SmoothingSettingsLine.value
        self.SmoothingSettingsLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Smoothing'] = self.SmoothingSettingsLine.value
        super().on_settings_line_changed()
