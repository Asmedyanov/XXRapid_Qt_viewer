from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal


class XXRapidTOFQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, timing_dict, expansion_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.Settings_dict = settings_dict

