from WaveformTimingPointSettingsQWidget import *


class WaveformTimingShutterSettingsQWidget(WaveformTimingPointSettingsQWidget):
    def __init__(self, settings_dict=None):
        super().__init__(settings_dict)
        if settings_dict is None:
            self.CameraNumber = MySettingsQWidget(
                name='Camera',
                default=1,
                limit=[1, 4],
                step=1
            )
            self.ShutterNumber = MySettingsQWidget(
                name='Shutter',
                default=1,
                limit=[1, 2],
                step=1
            )

        else:
            self.CameraNumber = MySettingsQWidget(
                name='Camera',
                default=settings_dict['Camera'],
                limit=[1, 4],
                step=1
            )
            self.ShutterNumber = MySettingsQWidget(
                name='Shutter',
                default=settings_dict['Shutter'],
                limit=[1, 2],
                step=1
            )
        self.SettingsDict['Camera'] = self.CameraNumber.value
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
