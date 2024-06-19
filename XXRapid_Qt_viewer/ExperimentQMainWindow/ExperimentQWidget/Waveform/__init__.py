from .WaveformOriginalQWidget import *
from .WaveformProcessingQTabWidget import *


class WaveformQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Waveform'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.folder_path = self.parent.folder_path
        self.folder_list = self.parent.folder_list
        super().__init__()
        try:
            self.WaveformOriginalQWidget = WaveformOriginalQWidget(self)
            self.addTab(self.WaveformOriginalQWidget, self.WaveformOriginalQWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.WaveformProcessingQTabWidget = WaveformProcessingQTabWidget(self)
            self.addTab(self.WaveformProcessingQTabWidget, self.WaveformProcessingQTabWidget.settings_key)
        except Exception as ex:
            print(ex)

    def test_settings_key(self, key_line):
        if key_line not in self.SettingsDict.keys():
            self.SettingsDict[key_line] = dict()
