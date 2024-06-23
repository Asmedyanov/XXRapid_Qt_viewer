from PyQt5.QtWidgets import QTabWidget
from .GraphicsQWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class GraphicsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Graphics')
        self.expansion_dict = self.parent.expansion_dict
        self.timing_dict = self.parent.timing_dict

        self.GraphicsDict = dict()
        for my_key, my_list in self.expansion_dict.items():
            self.current_key = my_key
            self.current_expansion_data = my_list
            try:
                self.GraphicsDict[my_key] = GraphicsQWidget(self)
                self.addTab(self.GraphicsDict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.expansion_dict = self.parent.expansion_dict
        self.timing_dict = self.parent.timing_dict
        for my_key, my_list in self.expansion_dict.items():
            self.current_key = my_key
            self.current_expansion_data = my_list
            try:
                self.GraphicsDict[my_key].refresh()
            except Exception as ex:
                print(ex)

    def set_data(self, timing_dict, expansion_dict):
        for my_key, my_list in expansion_dict.items():
            self.GraphicsDict[my_key].set_data(expansion_list=my_list, time_list=timing_dict)
        self.changed.emit()
