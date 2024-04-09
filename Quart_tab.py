from PyQt5.QtWidgets import QTabWidget
from MPL_tab import MPL_tab
from Tracer_tab import Tracer_tab
from Front_tab import Front_tab


class Quart_tab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.Front_tab_dict = dict()
        self.Tracer_tab = Tracer_tab()
        self.addTab(self.Tracer_tab, 'Tracer')
        self.Tracer_tab.tracer_changed.connect(self.On_Tracer_changed)
        for i in range(3):
            self.Front_tab_dict[f'Front {i + 1}'] = Front_tab()
            self.addTab(self.Front_tab_dict[f'Front {i + 1}'], f'Front {i + 1}')

    def On_Tracer_changed(self):
        self.x_min = int(min(self.Tracer_tab.x_1, self.Tracer_tab.x_2))
        self.x_max = int(max(self.Tracer_tab.x_1, self.Tracer_tab.x_2))
        self.y_min = int(min(self.Tracer_tab.y_1, self.Tracer_tab.y_2))
        self.y_max = int(max(self.Tracer_tab.y_1, self.Tracer_tab.y_2))
        self.cropped_image = self.Tracer_tab.image_array[self.y_min:self.y_max, self.x_min:self.x_max]
        for tab in self.Front_tab_dict.values():
            tab.set_data(self.cropped_image)

    def set_data(self, array_1):
        self.main_image = array_1
        self.Tracer_tab.set_data(array_1)
        self.On_Tracer_changed()
