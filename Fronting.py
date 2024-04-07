from PyQt5.QtWidgets import QTabWidget
from Quarting import Quarting


class Fronting(QTabWidget):
    def __init__(self):
        super().__init__()
        self.Frame_tab_dict = dict()
        for i in range(4):
            self.Frame_tab_dict[f'Frame {i + 1}'] = Quarting()
            self.addTab(self.Frame_tab_dict[f'Frame {i + 1}'], f'Frame {i + 1}')

    def set_data(self, array_1, dx):
        for i in range(4):
            self.Frame_tab_dict[f'Frame {i + 1}'].set_data(array_1[i], dx)
