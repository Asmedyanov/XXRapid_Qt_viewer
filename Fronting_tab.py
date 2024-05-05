from PyQt5.QtWidgets import QTabWidget
from Quarting_tab import Quarting
from PyQt5.QtCore import pyqtSignal


class Fronting(QTabWidget):
    fronting_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Frame_tab_dict = dict()
        self.Frame_data_dict = dict()
        for i in range(4):
            self.Frame_tab_dict[f'Frame_{i + 1}'] = Quarting()
            self.Frame_tab_dict[f'Frame_{i + 1}'].quarting_changed.connect(self.On_quarting_changed)
            self.addTab(self.Frame_tab_dict[f'Frame_{i + 1}'], f'Frame {i + 1}')

    def On_quarting_changed(self):
        for my_key, my_frame in self.Frame_tab_dict.items():
            self.Frame_data_dict[my_key] = my_frame.Quart_data_dict
        self.fronting_changed.emit()

    def set_data(self, array_1, dx, base_dict=None):
        if base_dict is None:
            for i in range(4):
                self.Frame_tab_dict[f'Frame_{i + 1}'].set_data(array_1[i], dx)
        else:
            for i in range(4):
                self.Frame_tab_dict[f'Frame_{i + 1}'].set_data(array_1[i], dx, base_dict=base_dict[f'Frame_{i + 1}'])
