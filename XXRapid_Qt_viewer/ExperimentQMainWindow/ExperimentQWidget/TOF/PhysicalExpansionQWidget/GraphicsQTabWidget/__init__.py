from PyQt5.QtWidgets import QTabWidget
from .Graphics import *
from SettingsQWidgets.ChildQTabWidget import *


class GraphicsQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Graphics')
        self.expansion_dict = self.parent.expansion_dict
        self.timing_dict = self.parent.timing_dict
        self.report_path = self.parent.report_path

        self.GraphicsDict = dict()
        for my_key, my_list in self.expansion_dict.items():
            self.current_key = my_key
            self.current_expansion_data = my_list
            try:
                self.GraphicsDict[my_key] = Graphics(self)
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

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        for graphics in self.GraphicsDict.values():
            try:
                graphics.save_report()
            except Exception as ex:
                print(ex)
