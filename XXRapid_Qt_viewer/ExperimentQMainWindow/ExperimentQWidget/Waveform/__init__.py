from .WaveformOriginalQWidget import *
from .WaveformProcessingQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class WaveformQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Waveform')
        self.folder_path = self.parent.folder_path
        self.folder_list = self.parent.folder_list
        try:
            self.WaveformOriginalQWidget = WaveformOriginalQWidget(self)
            self.addTab(self.WaveformOriginalQWidget, self.WaveformOriginalQWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.WaveformProcessingQTabWidget = WaveformProcessingQTabWidget(self)
            self.addTab(self.WaveformProcessingQTabWidget, self.WaveformProcessingQTabWidget.settings_key)
            self.WaveformProcessingQTabWidget.changed.connect(self.on_waveform_processing_changed)
        except Exception as ex:
            print(ex)

    def on_waveform_processing_changed(self):
        self.changed.emit()
