from PyQt5.QtWidgets import QTabWidget
from Separator_tab import Separator
from Quart_tab import Quart_tab
import numpy as np


class Quarting(QTabWidget):
    def __init__(self):
        super().__init__()
        self.Separator_tab = Separator()
        self.addTab(self.Separator_tab, 'Separator')
        self.Quart_tab_dict = dict()
        for i in range(4):
            self.Quart_tab_dict[f'Quart {i + 1}'] = Quart_tab()
            self.addTab(self.Quart_tab_dict[f'Quart {i + 1}'], f'Quart {i + 1}')
        self.Separator_tab.center_signal.connect(self.On_Separator_changed)

    def On_Separator_changed(self):
        self.Quarts_list = [
            self.image_array[:self.Separator_tab.center_y, self.Separator_tab.center_x:],
            np.flip(self.image_array[:self.Separator_tab.center_y, :self.Separator_tab.center_x], axis=1),
            np.flip(np.flip(self.image_array[self.Separator_tab.center_y:, :self.Separator_tab.center_x], axis=0),
                    axis=1),
            np.flip(self.image_array[:self.Separator_tab.center_y, :self.Separator_tab.center_x],axis=1)
        ]
        for i in range(4):
            self.Quart_tab_dict[f'Quart {i + 1}'].set_data(self.Quarts_list[i])

    def set_data(self, array_1, dx):
        self.Separator_tab.set_data(array_1, dx)
        self.image_array = array_1
        self.On_Separator_changed()
