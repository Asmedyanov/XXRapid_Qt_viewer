from SettingsQWidgets.SettingsBoxQWidget import *


class XXRapidOverlappedCameraSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        try:
            default = settings_dict['Scale']
        except:
            default = 50
        self.ScaleSettingLine = SettingsLineQWidget(
            name='Scale',
            default=default,
            limit=[0.1, 1e6],
            step=1,
            comment='Pix/mm'
        )
        self.QVBoxLayout.addWidget(self.ScaleSettingLine)
        self.SettingsDict['Scale'] = self.ScaleSettingLine.value
        self.ScaleSettingLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['Mask_threshold']
        except:
            default = 2
        self.MaskThresholdSettingLine = SettingsLineQWidget(
            name='Mask_threshold',
            default=default,
            limit=[0.1, 10],
            step=0.01,
            comment='x Median'
        )
        self.QVBoxLayout.addWidget(self.MaskThresholdSettingLine)
        self.SettingsDict['Mask_threshold'] = self.MaskThresholdSettingLine.value
        self.MaskThresholdSettingLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['Sigma_before']
        except:
            default = 1
        self.SigmaBeforeLine = SettingsLineQWidget(
            name='Sigma_before',
            default=default,
            limit=[0.1, 100],
            step=0.05,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.SigmaBeforeLine)
        self.SettingsDict['Sigma_before'] = self.SigmaBeforeLine.value
        self.SigmaBeforeLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['Sigma_shot']
        except:
            default = 1
        self.SigmaShotLine = SettingsLineQWidget(
            name='Sigma_shot',
            default=default,
            limit=[0.1, 100],
            step=0.05,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.SigmaShotLine)
        self.SettingsDict['Sigma_shot'] = self.SigmaShotLine.value
        self.SigmaShotLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['Sigma_overlapped']
        except:
            default = 1
        self.SigmaOverlappedLine = SettingsLineQWidget(
            name='Sigma_overlapped',
            default=default,
            limit=[0.1, 100],
            step=0.05,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.SigmaOverlappedLine)
        self.SettingsDict['Sigma_overlapped'] = self.SigmaOverlappedLine.value
        self.SigmaOverlappedLine.changed.connect(self.OnSettingsLineChanged)

    def OnSettingsLineChanged(self):
        super().OnSettingsLineChanged()
        self.SettingsDict['Scale'] = self.ScaleSettingLine.value
        self.SettingsDict['Sigma_before'] = self.SigmaBeforeLine.value
        self.SettingsDict['Sigma_shot'] = self.SigmaShotLine.value
        self.SettingsDict['Sigma_overlapped'] = self.SigmaOverlappedLine.value
        self.SettingsDict['Mask_threshold'] = self.MaskThresholdSettingLine.value

        self.changed.emit()
