from SettingsBoxQWidget import *


class XXRapidFrontingFrontSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        try:
            default = settings_dict['Threshold']
        except:
            default = 10
        self.ThresholdSettingLine = SettingsLineQWidget(
            name='Threshold',
            default=default,
            limit=[1, 100],
            step=1,
            comment='% x Max'
        )
        self.QVBoxLayout.addWidget(self.ThresholdSettingLine)
        self.SettingsDict['Threshold'] = self.ThresholdSettingLine.value
        self.ThresholdSettingLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['Approximation']
        except:
            default = 'line'
        self.ApproximationSettingLine = SettingsLineQWidget(
            name='Approximation',
            default=default,
            options_list=[
                'horizont',
                'line',
                'curve'
            ]
        )
        self.QVBoxLayout.addWidget(self.ApproximationSettingLine)
        self.SettingsDict['Approximation'] = self.ApproximationSettingLine.value
        self.ApproximationSettingLine.changed.connect(self.OnSettingsLineChanged)

    def OnSettingsLineChanged(self):
        super().OnSettingsLineChanged()
        self.SettingsDict['Threshold'] = self.ThresholdSettingLine.value
        self.SettingsDict['Approximation'] = self.ApproximationSettingLine.value

        self.changed.emit()
