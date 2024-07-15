from SettingsQWidgets.ChildQTabWidget import *
from .ChannelQWidget import *
import os


class WaveformChannelsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Waveform_channels')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
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
        physical_df_dict = dict()
        for my_key, my_channel in self.ChannelQWidgetDict.items():
            if my_channel.SettingsBox.Diagnostics == 'Rogowski_coil':
                physical_df_dict['Current'] = my_channel.df_smoothed
            elif my_channel.SettingsBox.Diagnostics == 'Tektronix_VD':
                physical_df_dict['Voltage'] = my_channel.df_smoothed
            elif my_channel.SettingsBox.Diagnostics == 'XXRapid_trig_out':
                physical_df_dict['Trigger'] = my_channel.df_smoothed
        return physical_df_dict

    def on_channel(self):
        self.PhysicalDFDict = self.get_physical_dict()
        self.changed.emit()

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for my_key, my_widget in self.ChannelQWidgetDict.items():
            my_widget.save_report()

    def save_origin_pro(self, op):
        work_book = op.new_book(lname=f'{self.settings_key}')
        for my_key, my_widget in self.ChannelQWidgetDict.items():
            my_widget.save_origin_pro(op, work_book)
