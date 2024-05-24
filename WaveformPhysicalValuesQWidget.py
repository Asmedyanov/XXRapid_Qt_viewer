from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from WaveformCurrentQWidget import *
from WaveformFullVoltageQWidget import *


class WaveformPhysicalValuesQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, physical_df_dict=None, settings_dict=None, timeshift=0):
        super().__init__()
        self.WaveformCurrentQWidget = WaveformCurrentQWidget(physical_df_dict['Current'], timeshift)
        self.addTab(self.WaveformCurrentQWidget, 'Waveform_current')
        self.WaveformFullVoltageQWidget = WaveformFullVoltageQWidget(physical_df_dict['Voltage'], timeshift)
        self.addTab(self.WaveformFullVoltageQWidget,'Full voltage')

    def set_data(self, physical_df_dict=None, timeshift=0):
        self.WaveformCurrentQWidget.set_data(physical_df_dict['Current'], timeshift)
        self.WaveformFullVoltageQWidget.set_data(physical_df_dict['Voltage'], timeshift)
        self.changed.emit()
