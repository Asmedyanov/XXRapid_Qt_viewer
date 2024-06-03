from .WaveformTimingPointSettingsQWidget import *


class WaveformTimingShutterSettingsQWidget(WaveformTimingPointSettingsQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        key = 'Camera'
        default = dict()
        if key in settings_dict.keys():
            default = int(float(settings_dict[key]))
        self.CameraNumber = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 4],
            step=1
        )
        self.SettingsDict[key] = self.CameraNumber.value

        key = 'Shutter'
        default = dict()
        if key in settings_dict.keys():
            default = int(float(settings_dict[key]))
        self.ShutterNumber = SettingsLineQWidget(
            name=key,
            default=default,
            limit=[1, 2],
            step=1
        )
        self.SettingsDict[key] = self.ShutterNumber.value
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
