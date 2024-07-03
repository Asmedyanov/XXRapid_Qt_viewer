from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Density'
        default = self.test_key(key, 8.9)

        self.DensitySettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0.01, 1e6],
            comment='g/cm^3',
            step=0.01
        )
        self.QVBoxLayout.addWidget(self.DensitySettingLine)
        self.DensitySettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Thickness'
        default = self.test_key(key, 15)

        self.ThicknessSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='um',
            step=1
        )
        self.QVBoxLayout.addWidget(self.ThicknessSettingLine)
        self.ThicknessSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Length'
        default = self.test_key(key, 40.0)

        self.LengthSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=0.5
        )
        self.QVBoxLayout.addWidget(self.LengthSettingLine)
        self.LengthSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Width'
        default = self.test_key(key, 50.0)

        self.WidthSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=0.5
        )
        self.QVBoxLayout.addWidget(self.WidthSettingLine)
        self.WidthSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Waist'
        default = self.test_key(key, 3.0)

        self.WaistSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            comment='mm',
            step=0.5
        )
        self.QVBoxLayout.addWidget(self.WaistSettingLine)
        self.WaistSettingLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Density'] = self.DensitySettingLine.value
        self.SettingsDict['Thickness'] = self.ThicknessSettingLine.value
        self.SettingsDict['Length'] = self.LengthSettingLine.value
        self.SettingsDict['Width'] = self.WidthSettingLine.value
        self.SettingsDict['Waist'] = self.WaistSettingLine.value
        super().on_settings_line_changed()
