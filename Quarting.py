from PyQt5.QtWidgets import QTabWidget
from MPL_tab import MPL_tab
from Separator import Separator
from Quart_tab import Quart_tab


class Quarting(QTabWidget):
    def __init__(self):
        super().__init__()
        self.Separator_tab = Separator()
        self.addTab(self.Separator_tab, 'Separator')
        self.Quart_tab_dict = dict()
        for i in range(4):
            self.Quart_tab_dict[f'Quart {i + 1}'] = Quart_tab()
            self.addTab(self.Quart_tab_dict[f'Quart {i + 1}'], f'Quart {i + 1}')

    def set_data(self, array_1, dx):
        self.Separator_tab.set_data(array_1, dx)
        center_x = array_1.shape[0] // 2
        center_y = array_1.shape[1] // 2
        self.Quarts_list = [
            array_1[:center_x, center_y:],
            array_1[:center_x, :center_y],
            array_1[center_x:, :center_y],
            array_1[center_x:, center_y:],
        ]
        for i in range(4):
            self.Quart_tab_dict[f'Quart {i + 1}'].set_data(self.Quarts_list[i])
