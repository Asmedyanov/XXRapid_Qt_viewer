from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Scale'
        default = self.test_key(key, 50)
        self.ScaleSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='pix/mm',
            step=1
        )
        self.QVBoxLayout.addWidget(self.ScaleSettingLine)
        self.ScaleSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Start_width'
        default = self.test_key(key, 3.0)  # mm
        self.StartWidthSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 1e6],
            comment='mm',
            step=0.5
        )
        self.QVBoxLayout.addWidget(self.StartWidthSettingLine)
        self.StartWidthSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'End_width'
        default = self.test_key(key, 20.0)  # mm
        self.EndWidthSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=0.5
        )
        self.QVBoxLayout.addWidget(self.EndWidthSettingLine)
        self.EndWidthSettingLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Scale'] = self.ScaleSettingLine.value
        self.SettingsDict['Start_width'] = self.StartWidthSettingLine.value
        self.SettingsDict['End_width'] = self.EndWidthSettingLine.value
        super().on_settings_line_changed()
