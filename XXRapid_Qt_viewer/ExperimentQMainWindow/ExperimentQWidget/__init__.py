from .Waveform import *
from .Waveform.WaveformProcessingQTabWidget import *
from dict2xml import dict2xml
import xmltodict
from XXRapidOriginalQWidget import *
from XXRapidOverlappedQWidget import *
from XXRapidFrontingQWidget import *
from PyQt5.QtWidgets import QMessageBox


class ExperimentQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, parent, folder_name='Default_shot', default=False, ):
        super().__init__()
        self.folder_name = folder_name
        self.folder_list = os.listdir(folder_name)
        self.parent = parent
        self.statusBar = self.parent.statusBar
        if 'QtTraceFolder' not in self.folder_list:
            os.makedirs(f'{folder_name}/QtTraceFolder')
        if default:
            settings_dict = self.OpenSettings()
        else:
            button_reply = QMessageBox.question(self, 'Settings message', "Do you want to use default settings?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if button_reply == QMessageBox.Yes:
                settings_dict = self.OpenSettings()
            else:
                settings_dict = self.OpenSettings('SettingsFile.xml')
        self.SettingsDict = settings_dict
        waveform_file_name = self.getWaveformFileName()
        self.WaveformOriginalQWidget = WaveformOriginalQWidget(waveform_file_name)
        self.addTab(self.WaveformOriginalQWidget, 'Waveform Original')

        key = 'Waveform_processing_settings'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.WaveformProcessingWidget = WaveformProcessingQTabWidget(self.WaveformOriginalQWidget.ChannelDFDict,
                                                                         settings_dict=settings)
            self.addTab(self.WaveformProcessingWidget, key)
            self.WaveformProcessingWidget.changed.connect(self.OnWaveformProcessingWidgetChanged)
            self.SettingsDict[key] = self.WaveformProcessingWidget.SettingsDict
        except Exception as ex:
            print(f'WaveformProcessingWidget {ex}')

        '''before_name = self.get_before_name()
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
            self.tabBarDoubleClicked.connect(self.on_tab_bar_double_click)
            self.SettingsDict['Fronting'] = self.XXRapidFrontingQTabWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidFrontingQTabWidget {ex}')
        try:
            settings = settings_dict['TOF']
        except:
            settings = dict()
        try:
            self.XXRapidTOFQTabWidget = XXRapidTOFQTabWidget(
                timing_dict=self.WaveformProcessingWidget.get_timing_dict(),
                expansion_dict=self.XXRapidFrontingQTabWidget.get_expansion_dict(),
                settings_dict=settings)
            self.addTab(self.XXRapidTOFQTabWidget, 'TOF')
            self.XXRapidTOFQTabWidget.changed.connect(self.OnXXRapidTOFQTabWidget)
            self.SettingsDict['TOF'] = self.XXRapidTOFQTabWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidTOFQTabWidget {ex}')'''

    def OnXXRapidTOFQTabWidget(self):
        self.SettingsDict['TOF'] = self.XXRapidTOFQTabWidget.SettingsDict
        pass

    def OnXXRapidFrontingQTabWidget(self):
        self.SettingsDict['Fronting'] = self.XXRapidFrontingQTabWidget.SettingsDict
        self.statusBar.showMessage(f'Press "t" to update TOF')

        self.changed.emit()

    def keyPressEvent(self, a0):

        if a0.key() == 84:

            try:
                self.XXRapidTOFQTabWidget.set_data(timing_dict=self.WaveformProcessingWidget.get_timing_dict(),
                                                   expansion_dict=self.XXRapidFrontingQTabWidget.get_expansion_dict())
                self.statusBar.showMessage(f'TOF is updated')
            except Exception as ex:
                print(f'XXRapidTOFQTabWidget.set_data {ex}')

    def on_tab_bar_double_click(self):
        try:
            self.XXRapidTOFQTabWidget.set_data(timing_dict=self.WaveformProcessingWidget.get_timing_dict(),
                                               expansion_dict=self.XXRapidFrontingQTabWidget.get_expansion_dict())
        except Exception as ex:
            print(f'XXRapidTOFQTabWidget.set_data {ex}')

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
        try:
            self.XXRapidTOFQTabWidget.save_report(f'{self.folder_name}/QtTraceFolder')
        except Exception as ex:
            print(f'XXRapidTOFQTabWidget.Save_Report {ex}')

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

    def set_default_settings(self):
        settings_dict = self.OpenSettings()
        self.SettingsDict = settings_dict

        try:
            settings = settings_dict['Waveform_processing_settings']
        except:
            settings = dict()
        try:
            self.WaveformProcessingWidget.set_settings(settings)
            self.SettingsDict['Waveform_processing_settings'] = self.WaveformProcessingWidget.SettingsDict
        except Exception as ex:
            print(f'WaveformProcessingWidget.set_settings {ex}')
