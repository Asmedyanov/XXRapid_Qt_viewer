from WaveformTimingQWidget import *
from WaveformChannelsTab import *
from WaveformPhysicalValuesQWidget import *
import os


class WaveformProcessingWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, channel_df_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.ChannelDFDict = channel_df_dict
        self.SettingsDict = settings_dict
        try:
            settings = settings_dict['Waveform_channels']
        except:
            settings = dict()
        self.WaveformChannelsTab = WaveformChannelsTab(self.ChannelDFDict, settings_dict=settings)
        self.SettingsDict['Waveform_channels'] = self.WaveformChannelsTab.SettingsDict
        self.WaveformChannelsTab.changed.connect(self.OnWaveformChannelsTabChanged)
        self.addTab(self.WaveformChannelsTab, 'Waveform_channels')
        try:
            settings = settings_dict['Waveform_timing']
        except:
            settings = dict()
        try:
            self.WaveformTimingQWidget = WaveformTimingQWidget(self.WaveformChannelsTab.PhysicalDFDict,
                                                               settings_dict=settings)

            self.SettingsDict['Waveform_timing'] = self.WaveformTimingQWidget.SettingsDict
            self.WaveformTimingQWidget.changed.connect(self.OnWaveformTimingQWidget)
            self.addTab(self.WaveformTimingQWidget, 'Waveform_timing')
        except Exception as ex:
            print(f'WaveformTimingQWidget {ex}')
        try:
            settings = settings_dict['Waveform_physical']
        except:
            settings = dict()
        try:
            self.WaveformPhysicalValuesQWidget = WaveformPhysicalValuesQWidget(
                self.WaveformChannelsTab.PhysicalDFDict, timeshift=self.WaveformTimingQWidget.t_start,
                settings_dict=settings)
            self.WaveformPhysicalValuesQWidget.changed.connect(self.OnWaveformPhysicalValuesQWidget)
            self.SettingsDict['Waveform_physical'] = self.WaveformPhysicalValuesQWidget.SettingsDict
            self.addTab(self.WaveformPhysicalValuesQWidget, 'Waveform_physical')
        except Exception as ex:
            print(f'WaveformPhysicalValuesQWidget {ex}')

    def OnWaveformPhysicalValuesQWidget(self):
        self.SettingsDict['Waveform_physical'] = self.WaveformPhysicalValuesQWidget.SettingsDict
        self.changed.emit()

    def OnWaveformTimingQWidget(self):
        self.SettingsDict['Waveform_timing'] = self.WaveformTimingQWidget.SettingsDict
        self.WaveformPhysicalValuesQWidget.set_data(self.WaveformChannelsTab.PhysicalDFDict,
                                                    self.WaveformTimingQWidget.t_start)
        self.changed.emit()

    def OnWaveformChannelsTabChanged(self):
        self.SettingsDict['Waveform_channels'] = self.WaveformChannelsTab.SettingsDict
        try:
            self.WaveformTimingQWidget.set_data(self.WaveformChannelsTab.PhysicalDFDict)
        except Exception as ex:
            print(f'WaveformTimingQWidget.set_data {ex}')
            try:
                settings = self.SettingsDict['Waveform_timing']
            except:
                settings = dict()
            try:
                self.WaveformTimingQWidget = WaveformTimingQWidget(self.WaveformChannelsTab.PhysicalDFDict,
                                                                   settings_dict=settings)

                self.SettingsDict['Waveform_timing'] = self.WaveformTimingQWidget.SettingsDict
                self.WaveformTimingQWidget.changed.connect(self.OnWaveformTimingQWidget)
                self.addTab(self.WaveformTimingQWidget, 'Waveform_timing')
            except Exception as ex:
                print(f'WaveformTimingQWidget {ex}')
            try:
                self.WaveformPhysicalValuesQWidget.set_data(self.WaveformChannelsTab.PhysicalDFDict,
                                                            timeshift=self.WaveformTimingQWidget.t_start)
            except Exception as ex:
                print(f'WaveformPhysicalValuesQWidget.set_data {ex}')
                try:
                    settings = self.SettingsDict['Waveform_physical']
                except:
                    settings = dict()
                try:
                    self.WaveformPhysicalValuesQWidget = WaveformPhysicalValuesQWidget(
                        self.WaveformChannelsTab.PhysicalDFDict, timeshift=self.WaveformTimingQWidget.t_start,
                        settings_dict=settings)
                    self.WaveformPhysicalValuesQWidget.changed.connect(self.OnWaveformPhysicalValuesQWidget)
                    self.SettingsDict['Waveform_physical'] = self.WaveformPhysicalValuesQWidget.SettingsDict
                    self.addTab(self.WaveformPhysicalValuesQWidget, 'Waveform_physical')
                except Exception as ex:
                    print(f'WaveformPhysicalValuesQWidget {ex}')
        self.changed.emit()

    def On_waveform_timing_changed(self):
        self.shutter_times = self.Waveform_timing_tab.peak_time
        # self.changed.emit()

    def set_data(self, ChannelDFDict, info_file_df):
        self.WaveformChannelsTab.set_data(ChannelDFDict)
        pass

    def Save_Raport(self, folder_name='Default_shot/QtTraceFolder'):
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

    def set_settings(self, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        self.SettingsDict = settings_dict
        try:
            settings = settings_dict['Waveform_channels']
        except:
            settings = dict()
        try:
            self.WaveformChannelsTab.set_settings(settings)
            self.SettingsDict['Waveform_channels'] = self.WaveformChannelsTab.SettingsDict
        except Exception as ex:
            print(f'WaveformChannelsTab.set_settings {ex}')

    def get_timing_dict(self):
        return self.SettingsDict['Waveform_timing']

