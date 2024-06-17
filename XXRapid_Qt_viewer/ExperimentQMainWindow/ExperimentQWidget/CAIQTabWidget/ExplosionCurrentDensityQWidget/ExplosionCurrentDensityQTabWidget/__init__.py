from PyQt5.QtWidgets import QTabWidget
from .Graphics import *


class ExplosionCurrentDensityQTabWidget(QTabWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.current_density_dict = self.parent.current_density_dict
        self.current_density_plot_dict = dict()
        for my_key, my_df in self.current_density_dict.items():
            self.current_density_plot_dict[my_key] = Graphics(my_df)
            self.addTab(self.current_density_plot_dict[my_key],my_key)

    def update(self):
        for my_key, my_df in self.current_density_dict.items():
            self.current_density_plot_dict[my_key].set_data(my_df)
