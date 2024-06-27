import os

from PyQt5.QtWidgets import QTabWidget
from .Graphics import *


class ExplosionCurrentDensityQTabWidget(QTabWidget):
    def __init__(self, parent):
        self.parent = parent
        self.report_path = self.parent.report_path
        super().__init__()
        self.current_density_dict = self.parent.current_density_dict
        self.GraphicsDict = dict()
        for my_key, my_df in self.current_density_dict.items():
            self.current_df = my_df
            self.current_key = my_key
            try:
                self.GraphicsDict[my_key] = Graphics(self)
                self.addTab(self.GraphicsDict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.current_density_dict = self.parent.current_density_dict
        for my_key, my_df in self.current_density_dict.items():
            self.current_df = my_df
            try:
                self.GraphicsDict[my_key].refresh()
            except Exception as ex:
                print(ex)

    def save_report(self):
        for graphics in self.GraphicsDict.values():
            try:
                graphics.save_report()
            except Exception as ex:
                print(ex)
