from PyQt5.QtWidgets import QTabWidget
from MPL_tab import MPL_tab
from Tracer_tab import Tracer_tab


class Quart_tab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.Quart_tab_dict = dict()
        self.Tracer_tab = Tracer_tab()
        self.addTab(self.Tracer_tab, 'Tracer')
        for i in range(3):
            self.Quart_tab_dict[f'Front {i + 1}'] = MPL_tab(f'Front {i + 1}')
            self.addTab(self.Quart_tab_dict[f'Front {i + 1}'], f'Front {i + 1}')

    def set_data(self, array_1):
        self.Tracer_tab.set_data(array_1)
        '''for i in range(4):
            self.Quart_tab_dict[f'Frame {i + 1}'].set_data(array_1[i], dx)'''
