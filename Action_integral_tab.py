from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import pyqtSignal
from Explosion_current_widget import Explosion_current_widget
from Explosion_current_density_widget import Explosion_current_density_widget
from Action_integral_widget import Action_integral_widget


class Action_integral_tab(QTabWidget):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.Explosion_current_widget = Explosion_current_widget()
        self.Explosion_current_widget.changed.connect(self.On_Explosion_current_widget_changed)
        self.addTab(self.Explosion_current_widget, 'Explosion current')

        self.Explosion_current_density_widget = Explosion_current_density_widget()
        self.Explosion_current_density_widget.changed.connect(self.On_Explosion_current_density_widget_changed)
        self.addTab(self.Explosion_current_density_widget, 'Explosion current density')

        self.Action_integral_widget = Action_integral_widget()
        self.Action_integral_widget.changed.connect(self.On_Action_integral_widget_changed)
        self.addTab(self.Action_integral_widget, 'Action integral')

    def On_Explosion_current_widget_changed(self):
        self.Explosion_current_density_widget.set_data(self.Explosion_current_widget.explosion_current_dict,
                                                       self.geometry_dict)

    def On_Explosion_current_density_widget_changed(self):
        pass

    def On_Action_integral_widget_changed(self):
        pass

    def set_data(self, explosion_time_dict, df_current, geometry_dict):
        self.geometry_dict = geometry_dict
        self.Explosion_current_widget.set_data(explosion_time_dict, df_current)
        self.Action_integral_widget.set_data(explosion_time_dict, df_current, geometry_dict)
        self.changed.emit()
