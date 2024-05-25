from WaveformTimingPointSettingsQWidget import *


class WaveformTimingShutterSettingsQWidget(WaveformTimingPointSettingsQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        try:
            default = settings_dict['Camera']
        except:
            default = 1
        self.CameraNumber = SettingsLineQWidget(
            name='Camera',
            default=default,
            limit=[1, 4],
            step=1
        )
        self.SettingsDict['Camera'] = self.CameraNumber.value
        try:
            default = settings_dict['Shutter']
        except:
            default = 1
        self.ShutterNumber = SettingsLineQWidget(
            name='Shutter',
            default=default,
            limit=[1, 2],
            step=1
        )
        self.SettingsDict['Shutter'] = self.ShutterNumber.value
        self.CameraNumber.changed.connect(self.OnCameraNumberChanged)
        self.ShutterNumber.changed.connect(self.OnShutterNumberChanged)
        self.QVBoxLayout.addWidget(self.CameraNumber)
        self.QVBoxLayout.addWidget(self.ShutterNumber)

    def OnCameraNumberChanged(self):
        self.SettingsDict['Camera'] = self.CameraNumber.value
        self.changed.emit()

    def OnShutterNumberChanged(self):
        self.SettingsDict['Shutter'] = self.ShutterNumber.value
        self.changed.emit()
