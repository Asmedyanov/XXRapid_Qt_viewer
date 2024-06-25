from .WaveformOriginalQWidget import *
from .WaveformProcessingQTabWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class WaveformQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Waveform')
        self.folder_path = self.parent.folder_path
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
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
        if self.parent.auto_refresh:
            self.changed.emit()
        else:
            self.parent.statusBar.showMessage(f'Waveform processing is changed. Please rebuild')

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.WaveformOriginalQWidget.save_report()
        except Exception as ex:
            print(ex)
        try:
            self.WaveformProcessingQTabWidget.save_report()
        except Exception as ex:
            print(ex)
