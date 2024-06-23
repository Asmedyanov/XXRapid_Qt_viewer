from PyQt5.QtWidgets import QTabWidget
from .GraphicsQWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class GraphicsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Graphics')
        self.motion_dict = self.parent.motion_dict
        self.motion_approximated_dict = self.parent.motion_approximated_dict
        self.index_to_plot_list = self.parent.index_to_plot_list

        self.GraphicsDict = dict()
        for my_key, my_list in self.motion_dict.items():
            self.current_key = my_key
            self.current_motion_list = my_list
            self.current_motion_approx_list = self.motion_approximated_dict[my_key]
            try:
                self.GraphicsDict[my_key] = GraphicsQWidget(self)
                self.addTab(self.GraphicsDict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.motion_dict = self.parent.motion_dict
        self.motion_approximated_dict = self.parent.motion_approximated_dict
        self.index_to_plot_list = self.parent.index_to_plot_list
        for my_key, my_list in self.motion_dict.items():
            self.current_key = my_key
            self.current_motion_list = my_list
            self.current_motion_approx_list = self.motion_approximated_dict[my_key]
            try:
                self.GraphicsDict[my_key].refresh()
            except Exception as ex:
                print(ex)

    def set_data(self, motion_dict, motion_approximated_dict, index_to_plot_list):
        for my_key, my_list in motion_dict.items():
            self.GraphicsDict[my_key].set_data(my_list, motion_approximated_dict[my_key], index_to_plot_list)
        self.changed.emit()
