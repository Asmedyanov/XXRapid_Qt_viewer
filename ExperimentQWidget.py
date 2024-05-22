from WaveformOriginalQWidget import *
from WaveformProcessingWidget import *
import os
from dict2xml import dict2xml
import xmltodict
from PyQt5.QtCore import pyqtSignal


class ExperimentQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, folder_name='Default_shot'):
        super().__init__()
        self.folder_name = folder_name
        self.folder_list = os.listdir(folder_name)
        if 'QtTraceFolder' not in self.folder_list:
            os.makedirs(f'{folder_name}/QtTraceFolder')
            self.SettingsDict = {'Experiment_settings': dict()}
        else:
            try:
                self.SettingsDict = self.OpenSettings()
            except Exception as ex:
                print(ex)
                self.SettingsDict = {'Experiment_settings': dict()}

        self.WaveformOriginalQWidget = WaveformOriginalQWidget(self.getWaveformFileName())
        self.addTab(self.WaveformOriginalQWidget, 'Waveform Original')
        if 'Waveform_processing_settings' not in self.SettingsDict['Experiment_settings'].keys():
            self.WaveformProcessingWidget = WaveformProcessingWidget(self.WaveformOriginalQWidget.ChannelDFDict)
            self.SettingsDict['Experiment_settings'][
                'Waveform_processing_settings'] = self.WaveformProcessingWidget.SettingsDict
        else:
            self.WaveformProcessingWidget = WaveformProcessingWidget(self.WaveformOriginalQWidget.ChannelDFDict,
                                                                     self.SettingsDict['Experiment_settings'][
                                                                         'Waveform_processing_settings'])
        self.addTab(self.WaveformProcessingWidget, 'Waveform Processing')
        self.WaveformProcessingWidget.changed.connect(self.OnWaveformProcessingWidgetChanged)

    def OnWaveformProcessingWidgetChanged(self):
        self.SettingsDict['Experiment_settings'][
            'Waveform_processing_settings'] = self.WaveformProcessingWidget.SettingsDict
        self.changed.emit()

    def SaveSettings(self, filename='SettingsFile.xml'):
        SettingsFile = open(f'{self.folder_name}/QtTraceFolder/{filename}', 'w')
        SettingsFile.write(dict2xml(self.SettingsDict))
        SettingsFile.close()

    def OpenSettings(self, filename='SettingsFile.xml'):
        SettingsFile = open(f'{self.folder_name}/QtTraceFolder/{filename}', 'r')
        SettingsDict = {'Experiment_settings': xmltodict.parse(SettingsFile.read())['Experiment_settings']}
        return SettingsDict

    def getWaveformFileName(self):
        waveform_files_list = [name for name in self.folder_list if
                               name.startswith('shot') and name.endswith('csv')]
        # print(f'Folder contains waveform files\n{waveform_files_list}\nI took the last one')
        return f'{self.folder_name}/{waveform_files_list[-1]}'
