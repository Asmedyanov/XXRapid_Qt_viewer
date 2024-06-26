from PyQt5.QtWidgets import QTabWidget
from .WaveformTimingShutterSettingsQWidget import *
from .WaveformTimingStartSettingsQWidget import *


class WaveformTimingSettingsQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        self.SettingsDict = self.parent.SettingsDict
        super().__init__()
        try:
            self.PulseStartTimeTab = WaveformTimingStartSettingsQWidget(self)
            self.addTab(self.PulseStartTimeTab, self.PulseStartTimeTab.settings_key)
        except Exception as ex:
            print(ex)

        '''key = 'Pulse_start'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        self.PulseStartTimeTab = WaveformTimingPointSettingsQWidget(settings_dict=settings)
        self.SettingsDict['Pulse_start'] = self.PulseStartTimeTab.SettingsDict
        self.PulseStartTimeTab.changed.connect(self.OnPulseStartTimeTab)
        self.addTab(self.PulseStartTimeTab, 'Pulse_start')
        self.n_shutters = 8
        self.ShutterTabDict = dict()
        for i in range(self.n_shutters):
            key = f'Shutter_{i + 1}'
            settings = dict()
            if key in settings_dict.keys():
                settings = settings_dict[key]
            self.ShutterTabDict[key] = WaveformTimingShutterSettingsQWidget(settings)
            self.addTab(self.ShutterTabDict[key], key)
            self.SettingsDict[key] = self.ShutterTabDict[key].SettingsDict
            self.ShutterTabDict[key].changed.connect(self.OnShutterTab)'''

    def test_settings_key(self, key_line):
        if key_line not in self.SettingsDict.keys():
            self.SettingsDict[key_line] = dict()

    def OnPulseStartTimeTab(self):
        self.SettingsDict['Pulse_start'] = self.PulseStartTimeTab.SettingsDict
        self.changed.emit()

    def OnShutterTab(self):
        for i in range(self.n_shutters):
            key = f'Shutter_{i + 1}'
            self.SettingsDict[key] = self.ShutterTabDict[key].SettingsDict
        self.changed.emit()
