from PyQt5.QtWidgets import QTabWidget
from Separator_tab import Separator_widget
from Quart_tab import Quart_tab
import numpy as np
from PyQt5.QtCore import pyqtSignal


class Quarting_tab(QTabWidget):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Separator_tab = Separator_widget()
        self.addTab(self.Separator_tab, 'Separator')
        self.Quart_tab_dict = dict()
        self.Quart_data_dict = dict()
        for i in range(4):
            key = f'Quart_{i + 1}'
            self.Quart_tab_dict[key] = Quart_tab()
            self.Quart_tab_dict[key].changed.connect(self.On_quart_changed)
            self.addTab(self.Quart_tab_dict[key], key)
        self.Separator_tab.changed.connect(self.On_Separator_changed)

    def On_quart_changed(self):
        for my_key, my_Quart_tab in self.Quart_tab_dict.items():
            self.Quart_data_dict[my_key] = my_Quart_tab.get_data_dict()
        self.changed.emit()

    def On_Separator_changed(self):
        self.Quart_data_dict['center'] = self.Separator_tab.get_data_dict()
        self.Quarts_list = [
            self.image_array[:self.Separator_tab.center_y, self.Separator_tab.center_x:],
            np.flip(self.image_array[:self.Separator_tab.center_y, :self.Separator_tab.center_x], axis=1),
            np.flip(np.flip(self.image_array[self.Separator_tab.center_y:, :self.Separator_tab.center_x], axis=0),
                    axis=1),
            np.flip(self.image_array[:self.Separator_tab.center_y, :self.Separator_tab.center_x], axis=1)
        ]
        for i in range(4):
            key = f'Quart_{i + 1}'
            if self.base_dict is None:
                self.Quart_tab_dict[key].set_data(self.Quarts_list[i])
            else:
                self.Quart_tab_dict[key].set_data(self.Quarts_list[i], base_dict=self.base_dict[key])
        self.changed.emit()

    def set_data(self, array_1, dx, base_dict=None):
        if base_dict is None:
            self.Separator_tab.set_data(array_1, dx)
        else:
            self.Separator_tab.set_data(array_1, dx, base_dict=base_dict['center'])
        self.base_dict = base_dict
        self.image_array = array_1
        self.On_Separator_changed()
