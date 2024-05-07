from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from Movement_widget import Movement_widget
from Velocity_widget import Velocity_widget
from Onset_time_widget import Onset_time_widget


class TOF_tab(QTabWidget):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Movement_widget = Movement_widget()
        self.addTab(self.Movement_widget, 'Movement')
        self.Movement_widget.changed.connect(self.On_Movement_widget_changed)

        self.Velocity_widget = Velocity_widget()
        self.addTab(self.Velocity_widget, 'Velocity')
        self.Onset_time_widget = Onset_time_widget()
        self.addTab(self.Onset_time_widget, 'Onset time')

    def On_Movement_widget_changed(self):
        self.Velocity_widget.set_data(self.Movement_widget.approximation_dict)
        self.Onset_time_widget.set_data(self.Movement_widget.approximation_dict)
        self.changed.emit()

    def set_data(self, expansion_by_cross_section_dict, shutter_times, dx):
        self.dx = dx
        self.Movement_widget.set_data(expansion_by_cross_section_dict, shutter_times, dx)
        self.changed.emit()
