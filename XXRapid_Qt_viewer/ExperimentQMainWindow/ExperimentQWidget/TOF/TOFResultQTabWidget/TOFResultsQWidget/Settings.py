from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Smoothing'
        default = self.test_key(key, 1.0)  # mm
        self.SmoothingSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0.1, 1e6],
            comment='mm',
            step=0.1
        )
        self.QVBoxLayout.addWidget(self.SmoothingSettingLine)
        self.SmoothingSettingLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Smoothing'] = self.SmoothingSettingLine.value
        super().on_settings_line_changed()
