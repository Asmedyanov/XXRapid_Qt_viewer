from .WaveformTimingQWidget import *
from .WaveformChannelsQTabWidget import *
from .WaveformPhysicalValuesQWidget import *
from SettingsQWidgets.ChildQTabWidget import *

import os


class WaveformProcessingQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Waveform_processing')
        self.folder_path = self.parent.folder_path
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

    def set_data(self, ChannelDFDict, info_file_df):
        self.WaveformChannelsTab.set_data(ChannelDFDict)
        pass

    def save_report(self, folder_name='Default_shot/QtTraceFolder'):
        if 'Waveform_processing' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Waveform_processing')
        self.WaveformChannelsTab.Save_Raport(f'{folder_name}/Waveform_processing')
        try:
            self.WaveformTimingQWidget.Save_Raport(f'{folder_name}/Waveform_processing')
        except Exception as ex:
            print(f'WaveformTimingQWidget.Save_Raport {ex}')
        try:
            self.WaveformPhysicalValuesQWidget.Save_Raport(f'{folder_name}/Waveform_processing')
        except Exception as ex:
            print(f'WaveformPhysicalValuesQWidget.Save_Raport {ex}')

    def get_timing_dict(self):
        return self.SettingsDict['Waveform_timing']
