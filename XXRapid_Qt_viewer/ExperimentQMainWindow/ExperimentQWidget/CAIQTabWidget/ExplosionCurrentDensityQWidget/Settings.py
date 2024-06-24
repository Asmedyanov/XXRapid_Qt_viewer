from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'foil_thickness'
        default = self.test_key(key, 10)  # um
        self.ThicknessSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e3],
            step=1,
            comment='um'
        )
        self.QVBoxLayout.addWidget(self.ThicknessSettingLine)
        self.ThicknessSettingLine.changed.connect(self.on_settings_line_changed)
        self.SettingsDict['foil_thickness'] = self.ThicknessSettingLine.value

    def on_settings_line_changed(self):
        self.SettingsDict['foil_thickness'] = self.ThicknessSettingLine.value
        super().on_settings_line_changed()
