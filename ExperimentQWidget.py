from PyQt5.QtWidgets import QTabWidget
from WaveformOriginalQWidget import *
from WaveformProcessingWidget import *
import os


class ExperimentQWidget(QTabWidget):
    def __init__(self, folder_name='Default_shot'):
        super().__init__()
        self.folder_name = folder_name
        self.folder_list = os.listdir(folder_name)
        self.WaveformOriginalQWidget = WaveformOriginalQWidget(self.getWaveformFileName())
        self.addTab(self.WaveformOriginalQWidget, 'Waveform Original')
        self.WaveformProcessingWidget = WaveformProcessingWidget(self.WaveformOriginalQWidget.ChannelDFDict)
        self.addTab(self.WaveformProcessingWidget, 'Waveform Processing')

    def getWaveformFileName(self):
        waveform_files_list = [name for name in self.folder_list if
                               name.startswith('shot') and name.endswith('csv')]
        # print(f'Folder contains waveform files\n{waveform_files_list}\nI took the last one')
        return f'{self.folder_name}/{waveform_files_list[-1]}'
