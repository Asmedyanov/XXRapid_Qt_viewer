from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Scale'
        default = self.test_key(key, 50)  # pix/mm
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

        key = 'Rotation'
        default = self.test_key(key, 0)  # degree
        self.RotationSettingLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[-180, 180],
            step=1,
            comment='°'
        )
        self.QVBoxLayout.addWidget(self.RotationSettingLine)
        self.SettingsDict[key] = self.RotationSettingLine.value
        self.RotationSettingLine.changed.connect(self.on_settings_line_changed)

        key = 'Mask_threshold'
        default = self.test_key(key, 50)
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
        default = self.test_key(key, 1.0)
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
        default = self.test_key(key, 1.0)
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
        default = self.test_key(key, 1.0)
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
        self.SettingsDict['Scale'] = self.ScaleSettingLine.value
        self.SettingsDict['Rotation'] = self.RotationSettingLine.value
        self.SettingsDict['Sigma_before'] = self.SigmaBeforeLine.value
        self.SettingsDict['Sigma_shot'] = self.SigmaShotLine.value
        self.SettingsDict['Sigma_overlapped'] = self.SigmaOverlappedLine.value
        self.SettingsDict['Mask_threshold'] = self.MaskThresholdSettingLine.value

        super().on_settings_line_changed()
