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
            self.WaveformChannelsQTabWidget.changed.connect(self.on_waveform_channels_changed)
        except Exception as ex:
            print(ex)
            return
        try:
            self.WaveformTimingQWidget = WaveformTimingQWidget(self)
            self.addTab(self.WaveformTimingQWidget, self.WaveformTimingQWidget.settings_key)
            self.WaveformTimingQWidget.changed.connect(self.on_waveform_timing_changed)
        except Exception as ex:
            print(ex)
            return
        try:
            self.WaveformPhysicalValuesQWidget = WaveformPhysicalValuesQWidget(self)
            self.addTab(self.WaveformPhysicalValuesQWidget, self.WaveformPhysicalValuesQWidget.settings_key)
        except Exception as ex:
            print(ex)

        '''key = 'Waveform_channels'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        self.WaveformChannelsTab = WaveformChannelsQTabWidget(self.ChannelDFDict, settings_dict=settings)
        self.SettingsDict['Waveform_channels'] = self.WaveformChannelsTab.SettingsDict
        self.WaveformChannelsTab.changed.connect(self.OnWaveformChannelsTabChanged)
        self.addTab(self.WaveformChannelsTab, 'Waveform_channels')

        key = 'Waveform_timing'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.WaveformTimingQWidget = WaveformTimingQWidget(self.WaveformChannelsTab.PhysicalDFDict,
                                                               settings_dict=settings)

            self.SettingsDict[key] = self.WaveformTimingQWidget.SettingsDict
            self.WaveformTimingQWidget.changed.connect(self.OnWaveformTimingQWidget)
            self.addTab(self.WaveformTimingQWidget, key)
        except Exception as ex:
            print(f'WaveformTimingQWidget {ex}')

        key = 'Waveform_physical'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.WaveformPhysicalValuesQWidget = WaveformPhysicalValuesQWidget(
                self.WaveformChannelsTab.PhysicalDFDict, timeshift=self.WaveformTimingQWidget.t_start,
                settings_dict=settings)
            self.WaveformPhysicalValuesQWidget.changed.connect(self.OnWaveformPhysicalValuesQWidget)
            self.SettingsDict[key] = self.WaveformPhysicalValuesQWidget.SettingsDict
            self.addTab(self.WaveformPhysicalValuesQWidget, key)
        except Exception as ex:
            print(f'WaveformPhysicalValuesQWidget {ex}')'''

    def on_waveform_timing_changed(self):
        try:
            self.WaveformPhysicalValuesQWidget.update()
        except Exception as ex:
            print(ex)

    def OnWaveformPhysicalValuesQWidget(self):
        self.SettingsDict['Waveform_physical'] = self.WaveformPhysicalValuesQWidget.SettingsDict
        self.changed.emit()

    def OnWaveformTimingQWidget(self):
        self.SettingsDict['Waveform_timing'] = self.WaveformTimingQWidget.SettingsDict
        try:
            self.WaveformPhysicalValuesQWidget.set_data(self.WaveformChannelsTab.PhysicalDFDict,
                                                        self.WaveformTimingQWidget.t_start)
        except Exception as ex:
            print(f'self.WaveformPhysicalValuesQWidget.set_data {ex}')
        self.changed.emit()

    def on_waveform_channels_changed(self):
        try:
            self.WaveformTimingQWidget.update()
        except Exception as ex:
            print(ex)

    def OnWaveformChannelsTabChanged(self):
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
