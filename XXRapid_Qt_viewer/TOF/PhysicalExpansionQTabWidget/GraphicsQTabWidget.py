from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from XXRapid_Qt_viewer.TOF.PhysicalExpansionQTabWidget.GraphicsQWidget import *


class GraphicsQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, timing_dict, expansion_dict, settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.SettingsDict = settings_dict
        self.GraphicsDict = dict()
        for my_key, my_list in expansion_dict.items():
            self.GraphicsDict[my_key] = GraphicsQWidget(expansion_list=my_list, time_list=timing_dict)
            self.addTab(self.GraphicsDict[my_key], my_key)

    def set_data(self,timing_dict, expansion_dict):
        for my_key, my_list in expansion_dict.items():
            self.GraphicsDict[my_key].set_data(expansion_list=my_list, time_list=timing_dict)
        self.changed.emit()
