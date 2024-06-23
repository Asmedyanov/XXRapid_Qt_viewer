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

        key = 'Foil_width'
        default = self.test_key(key, 50)
        self.WidthSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=1
        )
        self.QVBoxLayout.addWidget(self.WidthSettingLine)
        self.WidthSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Foil_length'
        default = self.test_key(key, 40)
        self.LengthSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=1
        )
        self.QVBoxLayout.addWidget(self.LengthSettingLine)
        self.LengthSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Foil_waist'
        default = self.test_key(key, 3.0)

        self.WaistSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=1
        )
        self.QVBoxLayout.addWidget(self.WaistSettingLine)
        self.WaistSettingLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Scale'] = self.ScaleSettingLine.value
        self.SettingsDict['Foil_width'] = self.WidthSettingLine.value
        self.SettingsDict['Foil_length'] = self.LengthSettingLine.value
        self.SettingsDict['Foil_waist'] = self.WaistSettingLine.value
        super().on_settings_line_changed()
