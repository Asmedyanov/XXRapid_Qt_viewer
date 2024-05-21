from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from WaveformSmoothingWidget import WaveformSmoothingWidget
from WaveformTimingWidget import WaveformTimingWidget
from WaveformChannelsTab import WaveformChannelsTab


class WaveformProcessingWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, channel_df_dict):
        super().__init__()
        self.ChannelDFDict = channel_df_dict
        self.WaveformChannelsTab = WaveformChannelsTab(self.ChannelDFDict)
        self.addTab(self.WaveformChannelsTab, 'Waveform channels')

    def On_waveform_timing_changed(self):
        self.shutter_times = self.Waveform_timing_tab.peak_time
        # self.changed.emit()

    def set_data(self, ChannelDFDict, info_file_df):
        self.WaveformChannelsTab.set_data(ChannelDFDict)
        pass
        '''self.Waveform_smoothing_tab.set_data(waveform_dict, info_file_df['Value']['Rogovski_conv'])
        self.Waveform_timing_tab.set_data(self.Waveform_smoothing_tab.df_smoothed,
                                          self.Waveform_smoothing_tab.df_4quick, info_file_df)'''
