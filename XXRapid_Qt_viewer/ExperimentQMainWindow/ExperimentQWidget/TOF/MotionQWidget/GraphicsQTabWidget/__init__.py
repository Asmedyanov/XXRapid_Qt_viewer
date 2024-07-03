import os

from PyQt5.QtWidgets import QTabWidget
from .Graphics import *
from SettingsQWidgets.ChildQTabWidget import *


class GraphicsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Graphics')
        self.report_path = self.parent.report_path
        self.motion_dict = self.parent.motion_dict
        self.motion_approximated_dict = self.parent.motion_approximated_dict
        self.index_to_plot_list = self.parent.index_to_plot_list

        self.GraphicsDict = dict()
        for my_key, my_list in self.motion_dict.items():
            self.current_key = my_key
            self.current_motion_list = my_list
            self.current_motion_approx_list = self.motion_approximated_dict[my_key]
            try:
                self.GraphicsDict[my_key] = Graphics(self)
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

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for graphics in self.GraphicsDict.values():
            try:
                graphics.save_report()
            except Exception as ex:
                print(ex)

    def save_origin_pro(self,op):
        for my_key, my_widget in self.GraphicsDict.items():
            my_widget.save_origin_pro(op)
