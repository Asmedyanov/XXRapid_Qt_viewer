from .WaveformTimingQWidget import *
from .WaveformChannelsQTabWidget import *
from .WaveformPhysicalValuesQWidget import *
from SettingsQWidgets.ChildQTabWidget import *

import os


class WaveformProcessingQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Waveform_processing')
        self.folder_path = self.parent.folder_path
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.folder_list = self.parent.folder_list
        self.WaveformOriginalQWidget = self.parent.WaveformOriginalQWidget
        self.ChannelDFDict = self.WaveformOriginalQWidget.ChannelDFDict
        try:
            self.WaveformChannelsQTabWidget = WaveformChannelsQTabWidget(self)
            self.addTab(self.WaveformChannelsQTabWidget, self.WaveformChannelsQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
            return
        try:
            self.WaveformTimingQWidget = WaveformTimingQWidget(self)
            self.addTab(self.WaveformTimingQWidget, self.WaveformTimingQWidget.settings_key)
        except Exception as ex:
            print(ex)
            return
        try:
            self.WaveformPhysicalValuesQWidget = WaveformPhysicalValuesQWidget(self)
            self.addTab(self.WaveformPhysicalValuesQWidget, self.WaveformPhysicalValuesQWidget.settings_key)
            self.WaveformPhysicalValuesQWidget.changed.connect(self.on_waveform_physical_values_changed)
        except Exception as ex:
            print(ex)

    def on_waveform_physical_values_changed(self):
        self.changed.emit()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.WaveformChannelsQTabWidget.save_report()
        except Exception as ex:
            print(ex)

        try:
            self.WaveformTimingQWidget.save_report()
        except Exception as ex:
            print(ex)

        try:
            self.WaveformPhysicalValuesQWidget.save_report()
        except Exception as ex:
            print(ex)

    def get_timing_dict(self):
        return self.SettingsDict['Waveform_timing']
