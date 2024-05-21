from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from WaveformSmoothingWidget import WaveformSmoothingWidget
from ChannelQWidget import ChannelQWidget


class WaveformChannelsTab(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, channel_df_dict, settings_dict=None):
        super().__init__()
        self.ChannelQWidgetDict = dict()
        self.PhysicalDFDict = dict()
        if settings_dict is None:
            self.SettingsDict = dict()
            for my_key, my_df in channel_df_dict.items():
                self.ChannelQWidgetDict[my_key] = ChannelQWidget(my_key, my_df)
                self.SettingsDict[my_key] = self.ChannelQWidgetDict[my_key].SettingsDict
        else:
            self.SettingsDict = settings_dict
            for my_key, my_df in channel_df_dict.items():
                self.ChannelQWidgetDict[my_key] = ChannelQWidget(my_key, my_df, self.SettingsDict[my_key])
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
