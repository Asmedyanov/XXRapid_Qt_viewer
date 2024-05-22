from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal

class WaveformPhysicalValuesQWidget(QTabWidget):
    changed = pyqtSignal()
    def __init__(self,physical_df_dict=None, settings_dict=None):
        super().__init__()