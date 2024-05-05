from PyQt5.QtWidgets import QTabWidget
from MPL_tab import MPL_tab
from Tracer_tab import Tracer_tab
from Front_tab import Front_tab
from PyQt5.QtCore import pyqtSignal


class Quart_tab(QTabWidget):
    quart_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Front_tab_dict = dict()
        self.Tracer_tab = Tracer_tab()
        self.addTab(self.Tracer_tab, 'Tracer')
        self.Tracer_tab.tracer_changed.connect(self.On_Tracer_changed)
        approx_list = ['line', 'my', 'my']
        self.front_data_dict = dict()
        for i in range(3):
            self.Front_tab_dict[f'Front_{i + 1}'] = Front_tab(self, approx_list[i])
            self.Front_tab_dict[f'Front_{i + 1}'].front_tab_changed.connect(self.On_Front_tab_changed)
            self.addTab(self.Front_tab_dict[f'Front_{i + 1}'], f'Front_{i + 1}')

    def On_Front_tab_changed(self):
        for my_key, my_Front_tab in self.Front_tab_dict.items():
            self.front_data_dict[my_key] = my_Front_tab.get_data_dict()
        self.quart_changed.emit()

    def On_Tracer_changed(self):
        self.x_min = 0  # int(min(self.Tracer_tab.x_1, self.Tracer_tab.x_2))
        self.x_max = int(max(self.Tracer_tab.x_1, self.Tracer_tab.x_2))
        self.y_min = int(min(self.Tracer_tab.y_1, self.Tracer_tab.y_2))
        self.y_max = int(max(self.Tracer_tab.y_1, self.Tracer_tab.y_2))
        self.cropped_image = self.Tracer_tab.image_array[self.y_min:self.y_max, self.x_min:self.x_max]
        if self.base_dict is None:
            for tab in self.Front_tab_dict.values():
                tab.set_data(self.cropped_image)
        else:
            for my_key, tab in self.Front_tab_dict.items():
                tab.set_data(self.cropped_image, base_dict=self.base_dict['fronts'][my_key])
                self.front_data_dict[my_key] = tab.get_data_dict()
        self.quart_changed.emit()

    def set_data(self, array_1, base_dict=None):
        self.base_dict = base_dict
        self.main_image = array_1
        if base_dict is None:
            self.Tracer_tab.set_data(array_1)
        else:
            self.Tracer_tab.set_data(array_1, base_dict=base_dict['Tracer'])
        #for my_key, my_Front_tab in self.Front_tab_dict.items():
            #self.front_data_dict[my_key] = my_Front_tab.get_data_dict()
        self.On_Tracer_changed()

    def get_data_dict(self):
        ret = {
            'Tracer': self.Tracer_tab.main_data_dict,
            'fronts': self.front_data_dict
        }
        return ret
