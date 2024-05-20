from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from WaveformSmoothingWidget import WaveformSmoothingWidget
from WaveformTimingWidget import WaveformTimingWidget
from WaveformChannelsTab import WaveformChannelsTab


class WaveformProcessingWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        '''self.Waveform_smoothing_tab = WaveformSmoothingWidget()
        self.addTab(self.Waveform_smoothing_tab, 'Waveform smoothing')
        self.Waveform_timing_tab = WaveformTimingWidget()
        self.addTab(self.Waveform_timing_tab, 'Waveform timing')
        self.Waveform_timing_tab.changed.connect(self.On_waveform_timing_changed)'''
        self.WaveformChannelsTab = WaveformChannelsTab()
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
