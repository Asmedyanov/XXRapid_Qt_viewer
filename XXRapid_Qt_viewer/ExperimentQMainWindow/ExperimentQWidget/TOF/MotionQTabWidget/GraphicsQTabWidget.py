from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal


class GraphicsQTabWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, motion_dict, motion_approximated_dict, index_to_plot_list=[1, 2], settings_dict=None):
        if settings_dict is None:
            settings_dict = dict()
        super().__init__()
        self.SettingsDict = settings_dict
        self.GraphicsDict = dict()
        for my_key, my_list in motion_dict.items():
            self.GraphicsDict[my_key] = GraphicsQWidget(my_list, motion_approximated_dict[my_key], index_to_plot_list)
            self.addTab(self.GraphicsDict[my_key], my_key)

    def set_data(self, motion_dict, motion_approximated_dict, index_to_plot_list):
        for my_key, my_list in motion_dict.items():
            self.GraphicsDict[my_key].set_data(my_list, motion_approximated_dict[my_key], index_to_plot_list)
        self.changed.emit()
