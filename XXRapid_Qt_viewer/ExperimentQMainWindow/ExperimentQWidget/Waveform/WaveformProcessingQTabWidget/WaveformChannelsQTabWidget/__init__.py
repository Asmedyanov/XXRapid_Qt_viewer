from SettingsQWidgets.ChildQTabWidget import *
from .ChannelQWidget import *
import os


class WaveformChannelsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Waveform_channels')
        self.WaveformOriginalQWidget = self.parent.WaveformOriginalQWidget
        self.ChannelDFDict = self.WaveformOriginalQWidget.ChannelDFDict
        self.ChannelQWidgetDict = dict()
        for my_key, my_df in self.ChannelDFDict.items():
            try:
                self.focused_key = my_key
                self.focused_df = my_df
                self.ChannelQWidgetDict[my_key] = ChannelQWidget(self)
                self.ChannelQWidgetDict[my_key].changed.connect(self.on_channel)
                self.addTab(self.ChannelQWidgetDict[my_key], self.ChannelQWidgetDict[my_key].settings_key)
            except Exception as ex:
                print(ex)
        self.PhysicalDFDict = self.get_physical_dict()

    def get_physical_dict(self):
        PhysicalDFDict = dict()
        for my_key, my_channel in self.ChannelQWidgetDict.items():
            if my_channel.SettingsBox.Diagnostics == 'Rogowski_coil':
                PhysicalDFDict['Current'] = my_channel.df_smoothed
            elif my_channel.SettingsBox.Diagnostics == 'Tektronix_VD':
                PhysicalDFDict['Voltage'] = my_channel.df_smoothed
            elif my_channel.SettingsBox.Diagnostics == 'XXRapid_trig_out':
                PhysicalDFDict['Trigger'] = my_channel.df_smoothed
        return PhysicalDFDict

    def on_channel(self):
        self.PhysicalDFDict = self.get_physical_dict()
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

    def set_settings(self, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        self.SettingsDict = settings_dict
        for my_key, my_channel_widget in self.ChannelQWidgetDict.items():
            try:
                settings = settings_dict[my_key]
            except:
                settings = dict()
            try:
                my_channel_widget.set_settings(settings)
                self.SettingsDict[my_key] = my_channel_widget.SettingsDict
            except Exception as ex:
                print(f'ChannelQWidgetDict[{my_key}].set_settings {ex}')
