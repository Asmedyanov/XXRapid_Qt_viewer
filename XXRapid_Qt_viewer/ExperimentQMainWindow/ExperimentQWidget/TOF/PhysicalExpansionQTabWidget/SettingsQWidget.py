from SettingsQWidgets.SettingsBoxQWidget import *


class SettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
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
        self.ScaleSettingLine.changed.connect(self.OnSettingsLineChanged)

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
        self.WidthSettingLine.changed.connect(self.OnSettingsLineChanged)

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
        self.LengthSettingLine.changed.connect(self.OnSettingsLineChanged)

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
        self.WaistSettingLine.changed.connect(self.OnSettingsLineChanged)

    def OnSettingsLineChanged(self):
        super().OnSettingsLineChanged()
        self.SettingsDict['Scale'] = self.ScaleSettingLine.value
        self.SettingsDict['Foil_width'] = self.WidthSettingLine.value
        self.SettingsDict['Foil_length'] = self.LengthSettingLine.value
        self.SettingsDict['Foil_waist'] = self.WaistSettingLine.value
        self.changed.emit()
