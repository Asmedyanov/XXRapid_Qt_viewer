from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from Waveform_smoothing_tab import Waveform_smoothing_tab
from Waveform_timing_tab import Waveform_timing_tab


class Waveform_processing_tab(QTabWidget):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Waveform_smoothing_tab = Waveform_smoothing_tab()
        self.addTab(self.Waveform_smoothing_tab, 'Waveform smoothing')
        self.Waveform_timing_tab = Waveform_timing_tab()
        self.addTab(self.Waveform_timing_tab, 'Waveform timing')
        self.Waveform_timing_tab.changed.connect(self.On_waveform_timing_changed)

    def On_waveform_timing_changed(self):
        self.shutter_times = self.Waveform_timing_tab.peak_time
        self.changed.emit()

    def set_data(self, waveform_dict, info_file_df):
        self.Waveform_smoothing_tab.set_data(waveform_dict, info_file_df['Value']['Rogovski_conv'])
        self.Waveform_timing_tab.set_data(self.Waveform_smoothing_tab.df_smoothed, info_file_df)
