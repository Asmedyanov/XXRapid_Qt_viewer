import os

from .Waveform import *
from .Waveform.WaveformProcessingQTabWidget import *
from dict2xml import dict2xml
import xmltodict
from .XXRapidOriginalQWidget import *
from .XXRapidOverlappedQWidget import *
from .XXRapidFrontingQWidget import *
from .TOF import *
from .ComsolSimulationQTabWidget import *
from .CAIQTabWidget import *
import shutil


class ExperimentQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.folder_path = self.parent.folder_path
        self.report_path = f'{self.folder_path}/QtTraceFolder'
        self.folder_list = os.listdir(self.folder_path)
        self.statusBar = self.parent.statusBar
        self.check_folder()
        self.SettingsDict = self.open_settings_xml()
        self.auto_refresh = self.parent.auto_refresh
        try:
            self.WaveformQTabWidget = WaveformQTabWidget(self)
            self.addTab(self.WaveformQTabWidget, self.WaveformQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.XXRapidOriginalQWidget = XXRapidOriginalQTabWidget(self)
            self.addTab(self.XXRapidOriginalQWidget, self.XXRapidOriginalQWidget.settings_key)
        except Exception as ex:
            print(ex)

        try:
            self.XXRapidOverlappedQWidget = XXRapidOverlappedQWidget(self)
            self.addTab(self.XXRapidOverlappedQWidget, self.XXRapidOverlappedQWidget.settings_key)
        except Exception as ex:
            print(ex)

        try:
            self.XXRapidFrontingQWidget = XXRapidFrontingQWidget(self)
            self.addTab(self.XXRapidFrontingQWidget, self.XXRapidFrontingQWidget.settings_key)
        except Exception as ex:
            print(ex)

        try:
            self.XXRapidTOFQTabWidget = XXRapidTOFQTabWidget(self)
            self.addTab(self.XXRapidTOFQTabWidget, self.XXRapidTOFQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.ComsolSimulationQTabWidget = ComsolSimulationQTabWidget(self)
            self.addTab(self.ComsolSimulationQTabWidget, self.ComsolSimulationQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.CAIQTabWidget = CAIQTabWidget(self)
            self.addTab(self.CAIQTabWidget, self.CAIQTabWidget.settings_key)
        except Exception as ex:
            print(ex)

    def save_origin_pro(self):
        import originpro as op
        op.new()
        path = os.getcwd()
        save_name = path + '\\Experiment_OriginLab.opju'
        op.save(save_name)
        try:
            self.WaveformQTabWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        op.save()
        op.exit()

        shutil.copy('Experiment_OriginLab.opju',
                    f'{self.folder_path}/QtTraceFolder')

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

    def get_before_name(self):
        before_files_list = [name for name in self.folder_list if
                             name.startswith('before') and name.endswith('rtv')]
        return f'{self.folder_path}/{before_files_list[-1]}'

    def get_shot_name(self):
        shot_files_list = [name for name in self.folder_list if
                           name.startswith('shot') and name.endswith('rtv')]
        # print(f'Folder contains shot files\n{shot_files_list}\nI took the last one')
        return f'{self.folder_path}/{shot_files_list[-1]}'

    def save_settings(self, filename='SettingsFile.xml'):
        settings_file = open(f'{self.folder_path}/QtTraceFolder/{filename}', 'w')
        settings_file.write(dict2xml({'Experiment_settings': self.SettingsDict}))
        settings_file.close()

    def save_report(self):

        try:
            self.WaveformQTabWidget.save_report()
        except Exception as ex:
            print(f'WaveformOriginalQWidget.save_report {ex}')
        try:
            self.XXRapidOriginalQWidget.save_report()
        except Exception as ex:
            print(f'XXRapidOriginalQWidget.save_report {ex}')
        try:
            self.XXRapidOverlappedQWidget.save_report()
        except Exception as ex:
            print(f'XXRapidOverlappedQWidget.save_report {ex}')
        try:
            self.XXRapidFrontingQWidget.save_report()
        except Exception as ex:
            print(f'XXRapidOverlappedQWidget.save_report {ex}')
        try:
            self.XXRapidTOFQTabWidget.save_report()
        except Exception as ex:
            print(f'XXRapidTOFQTabWidget.save_report {ex}')
        try:
            self.ComsolSimulationQTabWidget.save_report()
        except Exception as ex:
            print(f'ComsolSimulationQTabWidget.save_report {ex}')
        try:
            self.CAIQTabWidget.save_report()
        except Exception as ex:
            print(f'CAIQTabWidget.save_report {ex}')

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
