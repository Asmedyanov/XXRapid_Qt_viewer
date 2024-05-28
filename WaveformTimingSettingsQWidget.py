from PyQt5.QtWidgets import QTabWidget
from WaveformTimingShutterSettingsQWidget import *


class WaveformTimingSettingsQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, settings_dict=dict()):
        super().__init__()
        self.SettingsDict = dict()
        try:
            settings = settings_dict['Pulse_start']
        except:
            settings = dict()
        self.PulseStartTimeTab = WaveformTimingPointSettingsQWidget(settings_dict=settings)
        self.SettingsDict['Pulse_start'] = self.PulseStartTimeTab.SettingsDict
        self.PulseStartTimeTab.changed.connect(self.OnPulseStartTimeTab)
        self.addTab(self.PulseStartTimeTab, 'Pulse_start')
        self.n_shutters = 8
        self.ShutterTabDict = dict()
        for i in range(self.n_shutters):
            key = f'Shutter_{i + 1}'
            try:
                settings = settings_dict[key]
            except:
                settings = dict()
            self.ShutterTabDict[key] = WaveformTimingShutterSettingsQWidget(settings)
            self.addTab(self.ShutterTabDict[key], key)
            self.SettingsDict[key] = self.ShutterTabDict[key].SettingsDict
            self.ShutterTabDict[key].changed.connect(self.OnShutterTab)

    def OnPulseStartTimeTab(self):
        self.SettingsDict['Pulse_start'] = self.PulseStartTimeTab.SettingsDict
        self.changed.emit()

    def OnShutterTab(self):
        for i in range(self.n_shutters):
            key = f'Shutter_{i + 1}'
            self.SettingsDict[key] = self.ShutterTabDict[key].SettingsDict
        self.changed.emit()
