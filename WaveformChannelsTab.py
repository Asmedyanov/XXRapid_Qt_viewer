from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from ChannelQWidget import ChannelQWidget
import os


class WaveformChannelsTab(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, channel_df_dict, settings_dict=None):
        super().__init__()
        self.setTabPosition(QTabWidget.TabPosition.West)
        self.ChannelQWidgetDict = dict()
        self.PhysicalDFDict = dict()
        self.SettingsDict = dict()
        for my_key, my_df in channel_df_dict.items():
            try:
                settings = settings_dict[my_key]
            except:
                settings = None
            self.ChannelQWidgetDict[my_key] = ChannelQWidget(my_key, my_df, settings)
        for my_key, my_channel in self.ChannelQWidgetDict.items():
            self.addTab(my_channel, my_key)
            if my_channel.ChannelSettingsQWidget.Diagnostics == 'Rogowski_coil':
                self.PhysicalDFDict['Current'] = my_channel.df_smoothed
            elif my_channel.ChannelSettingsQWidget.Diagnostics == 'Tektronix_VD':
                self.PhysicalDFDict['Voltage'] = my_channel.df_smoothed
            elif my_channel.ChannelSettingsQWidget.Diagnostics == 'XXRapid_trig_out':
                self.PhysicalDFDict['Trigger'] = my_channel.df_smoothed
            my_channel.changed.connect(self.OnChannelChanged)

    def OnChannelChanged(self):
        for my_key, my_channel in self.ChannelQWidgetDict.items():
            self.SettingsDict[my_key] = my_channel.SettingsDict
            if my_channel.ChannelSettingsQWidget.Diagnostics == 'Rogowski_coil':
                self.PhysicalDFDict['Current'] = my_channel.df_smoothed
            elif my_channel.ChannelSettingsQWidget.Diagnostics == 'Tektronix_VD':
                self.PhysicalDFDict['Voltage'] = my_channel.df_smoothed
            elif my_channel.ChannelSettingsQWidget.Diagnostics == 'XXRapid_trig_out':
                self.PhysicalDFDict['Trigger'] = my_channel.df_smoothed
        self.changed.emit()

    def set_data(self, channel_df_dict):
        for my_key, my_df in channel_df_dict.items():
            self.ChannelQWidgetDict[my_key] = ChannelQWidget()
            self.addTab(self.ChannelQWidgetDict[my_key], my_key)
            self.ChannelQWidgetDict[my_key].set_data(my_df)

    def Save_Raport(self, folder_name):
        if 'Waveform_channels' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/Waveform_channels')
        for mykey, mychannel in self.ChannelQWidgetDict.items():
            if mykey not in os.listdir(f'{folder_name}/Waveform_channels'):
                os.makedirs(f'{folder_name}/Waveform_channels/{mykey}')
            mychannel.Save_Raport(f'{folder_name}/Waveform_channels/{mykey}')
