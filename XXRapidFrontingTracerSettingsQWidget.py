from SettingsBoxQWidget import *


class XXRapidFrontingTracerSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, parent, settings_dict=None):
        super().__init__(settings_dict)
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

        x_max = parent.camera_data['before'].shape[1]
        y_max = parent.camera_data['before'].shape[0]

        try:
            default = settings_dict['X_min']
        except:
            default = 0
        self.XMinLine = SettingsLineQWidget(
            name='X_min',
            default=default,
            limit=[0, x_max],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.XMinLine)
        self.SettingsDict['X_min'] = self.XMinLine.value
        self.XMinLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['Y_min']
        except:
            default = 0
        self.YMinLine = SettingsLineQWidget(
            name='Y_min',
            default=default,
            limit=[0, y_max],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.YMinLine)
        self.SettingsDict['Y_min'] = self.YMinLine.value
        self.YMinLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['X_max']
        except:
            default = x_max
        self.XMaxLine = SettingsLineQWidget(
            name='X_max',
            default=default,
            limit=[0, x_max],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.XMaxLine)
        self.SettingsDict['X_max'] = self.XMaxLine.value
        self.XMaxLine.changed.connect(self.OnSettingsLineChanged)

        try:
            default = settings_dict['Y_max']
        except:
            default = y_max
        self.YMaxLine = SettingsLineQWidget(
            name='Y_max',
            default=default,
            limit=[0, y_max],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.YMaxLine)
        self.SettingsDict['Y_max'] = self.YMaxLine.value
        self.YMaxLine.changed.connect(self.OnSettingsLineChanged)

    def OnSettingsLineChanged(self):
        super().OnSettingsLineChanged()
        self.SettingsDict['Sigma_before'] = self.SigmaBeforeLine.value
        self.SettingsDict['Sigma_shot'] = self.SigmaShotLine.value
        self.SettingsDict['Sigma_overlapped'] = self.SigmaOverlappedLine.value
        self.SettingsDict['Mask_threshold'] = self.MaskThresholdSettingLine.value
        self.SettingsDict['X_min'] = self.XMinLine.value
        self.SettingsDict['Y_min'] = self.YMinLine.value
        self.SettingsDict['X_max'] = self.XMaxLine.value
        self.SettingsDict['Y_max'] = self.YMaxLine.value

        self.changed.emit()

    def SetLine(self, x_min, y_min, x_max, y_max):
        self.XMinLine.setValue(x_min)
        self.XMaxLine.setValue(x_max)
        self.YMinLine.setValue(y_min)
        self.YMaxLine.setValue(y_max)
        self.OnSettingsLineChanged()
