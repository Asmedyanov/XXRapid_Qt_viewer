from SettingsQWidgets.SettingsBoxQWidget import *


class Settings(SettingsBoxQWidget):
    def __init__(self, parent):
        super().__init__(parent)
        key = 'Mask_threshold'
        default = self.test_key(key, 10)
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

        x_max = parent.camera_data['before'].shape[1]
        y_max = parent.camera_data['before'].shape[0]

        key = 'X_min'
        default = self.test_key(key, 0)
        self.XMinLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 1e6],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.XMinLine)
        self.SettingsDict[key] = self.XMinLine.value
        self.XMinLine.changed.connect(self.on_settings_line_changed)

        key = 'Y_min'
        default = self.test_key(key, 0)
        self.YMinLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 1e6],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.YMinLine)
        self.SettingsDict[key] = self.YMinLine.value
        self.YMinLine.changed.connect(self.on_settings_line_changed)

        key = 'X_max'
        default = self.test_key(key, x_max)
        self.XMaxLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 1e6],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.XMaxLine)
        self.SettingsDict[key] = self.XMaxLine.value
        self.XMaxLine.changed.connect(self.on_settings_line_changed)

        key = 'Y_max'
        default = self.test_key(key, y_max)
        self.YMaxLine = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[0, 1e6],
            step=1,
            comment='pix'
        )
        self.QVBoxLayout.addWidget(self.YMaxLine)
        self.SettingsDict[key] = self.YMaxLine.value
        self.YMaxLine.changed.connect(self.on_settings_line_changed)

    def on_settings_line_changed(self):
        self.SettingsDict['Sigma_before'] = self.SigmaBeforeLine.value
        self.SettingsDict['Sigma_shot'] = self.SigmaShotLine.value
        self.SettingsDict['Sigma_overlapped'] = self.SigmaOverlappedLine.value
        self.SettingsDict['Mask_threshold'] = self.MaskThresholdSettingLine.value
        self.SettingsDict['X_min'] = self.XMinLine.value
        self.SettingsDict['Y_min'] = self.YMinLine.value
        self.SettingsDict['X_max'] = self.XMaxLine.value
        self.SettingsDict['Y_max'] = self.YMaxLine.value
        super().on_settings_line_changed()

    def set_line(self, x_min, y_min, x_max, y_max):
        self.XMinLine.setValue(x_min)
        self.XMaxLine.setValue(x_max)
        self.YMinLine.setValue(y_min)
        self.YMaxLine.setValue(y_max)
        self.on_settings_line_changed()
