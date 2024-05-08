from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from Explosion_current_widget import Explosion_current_widget


class Action_integral_tab(QTabWidget):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Explosion_current_widget = Explosion_current_widget()
        self.addTab(self.Explosion_current_widget, 'Explosion current')

    def set_data(self, explosion_time_dict, df_current):
        self.Explosion_current_widget.set_data(explosion_time_dict, df_current)
        self.changed.emit()
