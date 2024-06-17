from PyQt5.QtWidgets import QTabWidget
from .CAIExplosionCurrentQWidget import *


class CAIExplosionCurrentQTabWidget(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.explosion_current_dict = self.parent.explosion_current_dict
        self.current_plot_dict = dict()
        for my_key, my_df in self.explosion_current_dict.items():
            self.current_plot_dict[my_key] = CAIExplosionCurrentQWidget(my_df)
            self.addTab(self.current_plot_dict[my_key], my_key)

    def update(self):
        self.explosion_current_dict = self.parent.explosion_current_dict
        for my_key, my_df in self.explosion_current_dict.items():
            self.current_plot_dict[my_key].set_data(my_df)
