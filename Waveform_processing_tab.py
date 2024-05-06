from PyQt5.QtWidgets import QTabWidget
from Separator_tab import Separator
from Quart_tab import Quart_tab
import numpy as np
from PyQt5.QtCore import pyqtSignal
from Waveform_smoothing_tab import Waveform_smoothing_tab
from Waveform_timing_tab import Waveform_timing_tab


class Waveform_processing_tab(QTabWidget):
    Waveform_processing_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Waveform_smoothing_tab = Waveform_smoothing_tab()
        self.addTab(self.Waveform_smoothing_tab, 'Waveform smoothing')
        self.Waveform_timing_tab = Waveform_timing_tab()
        self.addTab(self.Waveform_timing_tab, 'Waveform timing')
        '''self.Quart_tab_dict = dict()
        self.Quart_data_dict = dict()
        for i in range(4):
            self.Quart_tab_dict[f'Quart_{i + 1}'] = Quart_tab()
            self.Quart_tab_dict[f'Quart_{i + 1}'].quart_changed.connect(self.On_quart_changed)
            self.addTab(self.Quart_tab_dict[f'Quart_{i + 1}'], f'Quart {i + 1}')
        self.Separator_tab.center_signal.connect(self.On_Separator_changed)'''

    def set_data(self, waveform_dict, info_file_df):
        self.Waveform_smoothing_tab.set_data(waveform_dict, info_file_df['Value']['Rogovski_conv'])
        self.Waveform_timing_tab.set_data(self.Waveform_smoothing_tab.df_smoothed, info_file_df)
