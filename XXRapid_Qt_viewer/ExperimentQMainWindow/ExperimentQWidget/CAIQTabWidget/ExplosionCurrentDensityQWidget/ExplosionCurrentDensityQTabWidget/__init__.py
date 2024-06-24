from PyQt5.QtWidgets import QTabWidget
from .Graphics import *


class ExplosionCurrentDensityQTabWidget(QTabWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.current_density_dict = self.parent.current_density_dict
        self.current_density_plot_dict = dict()
        for my_key, my_df in self.current_density_dict.items():
            self.current_df = my_df
            try:
                self.current_density_plot_dict[my_key] = Graphics(self)
                self.addTab(self.current_density_plot_dict[my_key], my_key)
            except Exception as ex:
                print(ex)

    def refresh(self):
        self.current_density_dict = self.parent.current_density_dict
        for my_key, my_df in self.current_density_dict.items():
            self.current_df = my_df
            try:
                self.current_density_plot_dict[my_key].refresh()
            except Exception as ex:
                print(ex)
