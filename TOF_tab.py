from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from Movement_widget import Movement_widget


class TOF_tab(QTabWidget):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Movement_widget = Movement_widget()
        self.addTab(self.Movement_widget, 'Movement')

    def set_data(self, expansion_by_cross_section_dict, shutter_times, dx):
        self.dx = dx
        self.Movement_widget.set_data(expansion_by_cross_section_dict, shutter_times)
