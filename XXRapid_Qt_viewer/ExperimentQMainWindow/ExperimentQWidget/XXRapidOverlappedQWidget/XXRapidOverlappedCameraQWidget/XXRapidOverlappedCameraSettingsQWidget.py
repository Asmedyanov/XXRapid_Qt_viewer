from SettingsQWidgets.SettingsBoxQWidget import *


class XXRapidOverlappedCameraSettingsQWidget(SettingsBoxQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key = 'Scale'
        default = 50
        if key in settings_dict.keys():
            default = int(float(settings_dict[key]))
        self.ScaleSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 1e6],
            step=1,
            comment='Pix/mm'
        )
        self.QVBoxLayout.addWidget(self.ScaleSettingLine)
        self.SettingsDict[key] = self.ScaleSettingLine.value
        self.ScaleSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Mask_threshold'
        default = 50
        if key in settings_dict.keys():
            default = int(float(settings_dict[key]))
        self.MaskThresholdSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 100],
            step=1,
            comment='% Max'
        )
        self.QVBoxLayout.addWidget(self.MaskThresholdSettingLine)
        self.SettingsDict[key] = self.MaskThresholdSettingLine.value
        self.MaskThresholdSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Sigma_before'
        default = 1.0
        if key in settings_dict.keys():
            default = float(settings_dict[key])
        self.SigmaBeforeLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0.1, 100],
            step=0.05,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.SigmaBeforeLine)
        self.SettingsDict[key] = self.SigmaBeforeLine.value
        self.SigmaBeforeLine.changed.connect(self.on_settings_line_changed)

        key = 'Sigma_shot'
        default = 1.0
        if key in settings_dict.keys():
            default = float(settings_dict[key])
        self.SigmaShotLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0.1, 100],
            step=0.05,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.SigmaShotLine)
        self.SettingsDict[key] = self.SigmaShotLine.value
        self.SigmaShotLine.changed.connect(self.on_settings_line_changed)

        key = 'Sigma_overlapped'
        default = 1.0
        if key in settings_dict.keys():
            default = float(settings_dict[key])
        self.SigmaOverlappedLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0.1, 100],
            step=0.05,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.SigmaOverlappedLine)
        self.SettingsDict[key] = self.SigmaOverlappedLine.value
        self.SigmaOverlappedLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        super().on_settings_line_changed()
        self.SettingsDict['Scale'] = self.ScaleSettingLine.value
        self.SettingsDict['Sigma_before'] = self.SigmaBeforeLine.value
        self.SettingsDict['Sigma_shot'] = self.SigmaShotLine.value
        self.SettingsDict['Sigma_overlapped'] = self.SigmaOverlappedLine.value
        self.SettingsDict['Mask_threshold'] = self.MaskThresholdSettingLine.value

        self.changed.emit()
