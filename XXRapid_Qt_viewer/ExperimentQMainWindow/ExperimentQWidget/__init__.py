import os

from .Waveform import *
from .Waveform.WaveformProcessingQTabWidget import *
from dict2xml import dict2xml
import xmltodict
from .XXRapidOriginalQWidget import *
from .XXRapidOverlappedQWidget import *
from .XXRapidFrontingQWidget import *
from .TOF import *
from PyQt5.QtWidgets import QMessageBox
from .ComsolSimulationQTabWidget import *
from .CAIQTabWidget import *
import shutil


class ExperimentQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.folder_path = self.parent.folder_path
        self.folder_list = os.listdir(self.folder_path)
        self.statusBar = self.parent.statusBar
        self.check_folder()
        self.SettingsDict = self.open_settings_xml()
        try:
            self.WaveformQTabWidget = WaveformQTabWidget(self)
            self.addTab(self.WaveformQTabWidget, self.WaveformQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
            return

        '''waveform_file_name = self.getWaveformFileName()
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

        before_name = self.get_before_name()
        shot_name = self.get_shot_name()
        try:
            self.XXRapidOriginalQWidget = XXRapidOriginalQWidget(
                before_name=before_name,
                shot_name=shot_name
            )
        except Exception as ex:
            print(f'XXRapidOriginalQWidget {ex}')
        self.addTab(self.XXRapidOriginalQWidget, 'XXRapid_Camera_original')

        key = 'Overlapped_images'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.XXRapidOverlappedQWidget = XXRapidOverlappedQWidget(self.XXRapidOriginalQWidget.CameraDataDict,
                                                                     settings)
            self.addTab(self.XXRapidOverlappedQWidget, key)
            self.XXRapidOverlappedQWidget.changed.connect(self.OnXXRapidOverlappedQWidget)
            self.SettingsDict[key] = self.XXRapidOverlappedQWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidOverlappedQWidget {ex}')

        key = 'Fronting'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.XXRapidFrontingQTabWidget = XXRapidFrontingQWidget(self.XXRapidOriginalQWidget.CameraDataDict,
                                                                    settings)
            self.addTab(self.XXRapidFrontingQTabWidget, key)
            self.XXRapidFrontingQTabWidget.changed.connect(self.OnXXRapidFrontingQTabWidget)
            self.tabBarDoubleClicked.connect(self.on_tab_bar_double_click)
            self.SettingsDict[key] = self.XXRapidFrontingQTabWidget.SettingsDict
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
            print(f'XXRapidTOFQTabWidget {ex}')
        key = 'Comsol'
        try:
            settings = settings_dict[key]
        except:
            settings = dict()
        try:
            comsol_simulation_filename = self.get_comsol_simulation_filename()
            self.ComsolSimulation = ComsolSimulationQTabWidget(self, comsol_simulation_filename, settings)
            self.SettingsDict[key] = self.ComsolSimulation.SettingsDict
            self.ComsolSimulation.changed.connect(self.on_comsol_simulation)
            self.addTab(self.ComsolSimulation, key)
        except Exception as ex:
            print(ex)
        try:
            self.CAIQTabWidget = CAIQTabWidget(self)
            self.addTab(self.CAIQTabWidget, 'CAI_experimental')
        except Exception as ex:
            print(ex)'''

    def on_waveform_changed(self):
        self.changed.emit()

    def test_settings_key(self, key_line):
        if key_line not in self.SettingsDict.keys():
            self.SettingsDict[key_line] = dict()

    def check_folder(self):
        if 'QtTraceFolder' not in self.folder_list:
            os.makedirs(f'{self.folder_path}/QtTraceFolder')
        if 'SettingsFile.xml' not in os.listdir(f'{self.folder_path}/QtTraceFolder'):
            shutil.copy('Default_shot/QtTraceFolder/SettingsFile.xml',
                        f'{self.folder_path}/QtTraceFolder')

    def on_comsol_simulation(self):
        self.SettingsDict['Comsol'] = self.ComsolSimulation.SettingsDict

    def get_comsol_simulation_filename(self):
        comsol_files_list = [name for name in self.folder_list if
                             name.startswith('Jmax') and name.endswith('csv')]
        # print(f'Folder contains waveform files\n{waveform_files_list}\nI took the last one')
        return f'{self.folder_path}/{comsol_files_list[-1]}'

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
        return f'{self.folder_path}/{before_files_list[-1]}'

    def get_shot_name(self):
        shot_files_list = [name for name in self.folder_list if
                           name.startswith('shot') and name.endswith('rtv')]
        # print(f'Folder contains shot files\n{shot_files_list}\nI took the last one')
        return f'{self.folder_path}/{shot_files_list[-1]}'

    def OnWaveformProcessingWidgetChanged(self):
        self.SettingsDict[
            'Waveform_processing_settings'] = self.WaveformProcessingWidget.SettingsDict
        self.changed.emit()

    def SaveSettings(self, filename='SettingsFile.xml'):
        SettingsFile = open(f'{self.folder_path}/QtTraceFolder/{filename}', 'w')
        SettingsFile.write(dict2xml({'Experiment_settings': self.SettingsDict}))
        SettingsFile.close()

    def SaveTrace(self, ):
        try:
            self.WaveformOriginalQWidget.save_report(f'{self.folder_path}/QtTraceFolder')
        except Exception as ex:
            print(f'WaveformOriginalQWidget.Save_Report {ex}')
        try:
            self.WaveformProcessingWidget.save_report(f'{self.folder_path}/QtTraceFolder')
        except Exception as ex:
            print(f'WaveformProcessingWidget.Save_Report {ex}')
        try:
            self.XXRapidOriginalQWidget.save_report(f'{self.folder_path}/QtTraceFolder')
        except Exception as ex:
            print(f'XXRapidOriginalQWidget.Save_Report {ex}')
        try:
            self.XXRapidOverlappedQWidget.save_report(f'{self.folder_path}/QtTraceFolder')
        except Exception as ex:
            print(f'XXRapidOverlappedQWidget.Save_Report {ex}')
        try:
            self.XXRapidTOFQTabWidget.save_report(f'{self.folder_path}/QtTraceFolder')
        except Exception as ex:
            print(f'XXRapidTOFQTabWidget.Save_Report {ex}')

    def open_settings_xml(self):
        settings = dict()
        try:
            SettingsFile = open(f'{self.folder_path}/QtTraceFolder/SettingsFile.xml', 'r')
        except Exception as ex:
            print(f'OpenSettings {ex}')
            SettingsFile = open('Default_shot/QtTraceFolder/SettingsFile.xml', 'r')
            print('Default settings')
        try:
            settings = xmltodict.parse(SettingsFile.read())['Experiment_settings']
        except Exception as ex:
            print(f'xmltodict {ex}')
        return settings

    def getWaveformFileName(self):
        waveform_files_list = [name for name in self.folder_list if
                               name.startswith('shot') and name.endswith('csv')]
        # print(f'Folder contains waveform files\n{waveform_files_list}\nI took the last one')
        return f'{self.folder_path}/{waveform_files_list[-1]}'

    def set_default_settings(self):
        settings_dict = self.open_settings_xml()
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
