from PyQt5.QtWidgets import QTabWidget
from .ComsolSimulationQWidget import *


class ComsolSimulationQTabWidget(QTabWidget):
    def __init__(self, parent, filename='Default_shot/Jmax.csv'):
        super().__init__()
        self.parent = parent
        self.filename = filename
        self.ComsolSimulationQWidget = ComsolSimulationQWidget(self.parent, self.filename)
        self.addTab(self.ComsolSimulationQWidget,'ComsolSimulation')
