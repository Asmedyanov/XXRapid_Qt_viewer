from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from WaveformSmoothingWidget import WaveformSmoothingWidget
from ChannelQWidget import ChannelQWidget


class WaveformChannelsTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.ChannelQWidgetDict = dict()

    def set_data(self, channel_df_dict):
        for my_key, my_df in channel_df_dict.items():
            self.ChannelQWidgetDict[my_key] = ChannelQWidget()
            self.addTab(self.ChannelQWidgetDict[my_key], my_key)
            self.ChannelQWidgetDict[my_key].set_data(my_df)
