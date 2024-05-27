from SettingsBoxQWidget import *


class XXRapidFrontingSeparatorSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict):
        super().__init__(settings_dict)
        try:
            default = settings_dict['Rotation']
        except:
            default = '0'
        self.RotationSettingLine = SettingsLineQWidget(
            name='Rotation',
            default=default,
            options_list=[
                '0', '90'
            ],
            comment='degree'
        )
        self.QVBoxLayout.addWidget(self.RotationSettingLine)
        self.SettingsDict['Rotation'] = self.RotationSettingLine.value
        self.RotationSettingLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['X_center']
        except:
            default = 500
        self.XCenterSettingLine = SettingsLineQWidget(
            name='X_center',
            default=default,
            limit=[0, 2e3],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.XCenterSettingLine)
        self.SettingsDict['X_center'] = self.XCenterSettingLine.value
        self.XCenterSettingLine.changed.connect(self.OnSettingsLineChanged)
        try:
            default = settings_dict['Y_center']
        except:
            default = 500
        self.YCenterSettingLine = SettingsLineQWidget(
            name='Y_center',
            default=default,
            limit=[0, 2e3],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.YCenterSettingLine)
        self.SettingsDict['Y_center'] = self.YCenterSettingLine.value
        self.YCenterSettingLine.changed.connect(self.OnSettingsLineChanged)

    def set_center(self, x, y):
        self.XCenterSettingLine.QSpinBox.setValue(x)
        self.YCenterSettingLine.QSpinBox.setValue(y)
        self.OnSettingsLineChanged()

    def OnSettingsLineChanged(self):
        super().OnSettingsLineChanged()
        self.SettingsDict['Rotation'] = self.RotationSettingLine.value
        self.SettingsDict['X_center'] = self.XCenterSettingLine.value
        self.SettingsDict['Y_center'] = self.YCenterSettingLine.value
        self.changed.emit()
