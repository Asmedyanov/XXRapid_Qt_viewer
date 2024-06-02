from WaveformOriginalQWidget import *
from WaveformProcessingWidget import *
from dict2xml import dict2xml
import xmltodict
from XXRapidOriginalQWidget import *
from XXRapidOverlappedQWidget import *
from XXRapidFrontingQWidget import *


class ExperimentQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, folder_name='Default_shot'):
        super().__init__()
        self.folder_name = folder_name
        self.folder_list = os.listdir(folder_name)
        if 'QtTraceFolder' not in self.folder_list:
            os.makedirs(f'{folder_name}/QtTraceFolder')
        settings_dict = self.OpenSettings('SettingsFile.xml')
        self.SettingsDict = settings_dict
        WaveformFileName = self.getWaveformFileName()
        self.WaveformOriginalQWidget = WaveformOriginalQWidget(WaveformFileName)
        self.addTab(self.WaveformOriginalQWidget, 'Waveform Original')
        try:
            settings = settings_dict['Waveform_processing_settings']
        except:
            settings = dict()
        try:
            self.WaveformProcessingWidget = WaveformProcessingWidget(self.WaveformOriginalQWidget.ChannelDFDict,
                                                                     settings_dict=settings)
            self.addTab(self.WaveformProcessingWidget, 'Waveform WaveformProcessingQTabWidget')
            self.WaveformProcessingWidget.changed.connect(self.OnWaveformProcessingWidgetChanged)
            self.SettingsDict['Waveform_processing_settings'] = self.WaveformProcessingWidget.SettingsDict
        except Exception as ex:
            print(f'WaveformProcessingWidget {ex}')
        before_name = self.get_before_name()
        shot_name = self.get_shot_name()
        self.XXRapidOriginalQWidget = XXRapidOriginalQWidget(
            before_name=before_name,
            shot_name=shot_name
        )
        self.addTab(self.XXRapidOriginalQWidget, 'XXRapid_Camera_original')
        try:
            settings = settings_dict['Overlapped_images']
        except:
            settings = dict()
        try:
            self.XXRapidOverlappedQWidget = XXRapidOverlappedQWidget(self.XXRapidOriginalQWidget.CameraDataDict,
                                                                     settings)
            self.addTab(self.XXRapidOverlappedQWidget, 'Overlapped_images')
            self.XXRapidOverlappedQWidget.changed.connect(self.OnXXRapidOverlappedQWidget)
            self.SettingsDict['Overlapped_images'] = self.XXRapidOverlappedQWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidOverlappedQWidget {ex}')
        try:
            settings = settings_dict['Fronting']
        except:
            settings = dict()
        try:
            self.XXRapidFrontingQTabWidget = XXRapidFrontingQWidget(self.XXRapidOriginalQWidget.CameraDataDict,
                                                                    settings)
            self.addTab(self.XXRapidFrontingQTabWidget, 'Fronting')
            self.XXRapidFrontingQTabWidget.changed.connect(self.OnXXRapidFrontingQTabWidget)
            self.SettingsDict['Fronting'] = self.XXRapidFrontingQTabWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidFrontingQTabWidget {ex}')

    def OnXXRapidFrontingQTabWidget(self):
        self.SettingsDict['Fronting'] = self.XXRapidFrontingQTabWidget.SettingsDict
        self.changed.emit()

    def OnXXRapidOverlappedQWidget(self):
        self.SettingsDict['Overlapped_images'] = self.XXRapidOverlappedQWidget.SettingsDict
        self.changed.emit()

    def get_before_name(self):
        before_files_list = [name for name in self.folder_list if
                             name.startswith('before') and name.endswith('rtv')]
        return f'{self.folder_name}/{before_files_list[-1]}'

    def get_shot_name(self):
        shot_files_list = [name for name in self.folder_list if
                           name.startswith('shot') and name.endswith('rtv')]
        # print(f'Folder contains shot files\n{shot_files_list}\nI took the last one')
        return f'{self.folder_name}/{shot_files_list[-1]}'

    def OnWaveformProcessingWidgetChanged(self):
        self.SettingsDict[
            'Waveform_processing_settings'] = self.WaveformProcessingWidget.SettingsDict
        self.changed.emit()

    def SaveSettings(self, filename='SettingsFile.xml'):
        SettingsFile = open(f'{self.folder_name}/QtTraceFolder/{filename}', 'w')
        SettingsFile.write(dict2xml({'Experiment_settings': self.SettingsDict}))
        SettingsFile.close()

    def SaveTrace(self, ):
        try:
            self.WaveformOriginalQWidget.save_report(f'{self.folder_name}/QtTraceFolder')
        except Exception as ex:
            print(f'WaveformOriginalQWidget.Save_Report {ex}')
        try:
            self.WaveformProcessingWidget.save_report(f'{self.folder_name}/QtTraceFolder')
        except Exception as ex:
            print(f'WaveformProcessingWidget.Save_Report {ex}')
        try:
            self.XXRapidOriginalQWidget.save_report(f'{self.folder_name}/QtTraceFolder')
        except Exception as ex:
            print(f'XXRapidOriginalQWidget.Save_Report {ex}')
        try:
            self.XXRapidOverlappedQWidget.save_report(f'{self.folder_name}/QtTraceFolder')
        except Exception as ex:
            print(f'XXRapidOverlappedQWidget.Save_Report {ex}')

    def OpenSettings(self, filename='Default_shot/QtTraceFolder/SettingsFile.xml'):
        try:
            SettingsFile = open(f'{self.folder_name}/QtTraceFolder/{filename}', 'r')
        except Exception as ex:
            print(f'OpenSettings {ex}')
            SettingsFile = open('Default_shot/QtTraceFolder/SettingsFile.xml', 'r')
            print('Default settings')
        try:
            SettingsDict = xmltodict.parse(SettingsFile.read())['Experiment_settings']
            return SettingsDict
        except Exception as ex:
            print(f'xmltodict {ex}')
            return dict()

    def getWaveformFileName(self):
        waveform_files_list = [name for name in self.folder_list if
                               name.startswith('shot') and name.endswith('csv')]
        # print(f'Folder contains waveform files\n{waveform_files_list}\nI took the last one')
        return f'{self.folder_name}/{waveform_files_list[-1]}'
