from SettingsQWidgets.SettingsBoxQWidget import *


class XXRapidFrontingFrontSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key='Threshold'
        try:
            default = settings_dict[key]
        except:
            default = 10
        self.ThresholdSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 500],
            step=1,
            comment='% x Max'
        )
        self.QVBoxLayout.addWidget(self.ThresholdSettingLine)
        self.SettingsDict[key] = self.ThresholdSettingLine.value
        self.ThresholdSettingLine.changed.connect(self.OnSettingsLineChanged)

        key='Approximation'
        try:
            default = settings_dict[key]
        except:
            default = 'line'
        self.ApproximationSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            options_list=[
                'line',
                'curve',
                '1st_order',
                '2nd_order',
                '0_order',
                'rest',
            ]
        )
        self.QVBoxLayout.addWidget(self.ApproximationSettingLine)
        self.SettingsDict[key] = self.ApproximationSettingLine.value
        self.ApproximationSettingLine.changed.connect(self.OnSettingsLineChanged)
        key = 'Shutter_order'
        try:
            default = settings_dict[key]
        except:
            default = '0'
        self.ShutterSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            options_list=[
                '0', '1', '2', '3', '4', '5', '6', '7', '8'
            ]
        )
        self.QVBoxLayout.addWidget(self.ShutterSettingLine)
        self.SettingsDict[key] = self.ShutterSettingLine.value
        self.ShutterSettingLine.changed.connect(self.OnSettingsLineChanged)

    def OnSettingsLineChanged(self):
        super().OnSettingsLineChanged()
        self.SettingsDict['Threshold'] = self.ThresholdSettingLine.value
        self.SettingsDict['Approximation'] = self.ApproximationSettingLine.value
        self.SettingsDict['Shutter_order'] = self.ShutterSettingLine.value

        self.changed.emit()
