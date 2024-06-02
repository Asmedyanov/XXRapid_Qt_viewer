from PyQt5.QtWidgets import QVBoxLayout, QWidget
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import pyqtSignal


class MatplotlibQWidget(QWidget):
    changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        try:
            super().__init__()
        except:
            super().__init__()
        self.layout = QVBoxLayout()
        self.figure = plt.figure()
        self.figure.set_layout_engine(layout='tight')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.png_name = 'MatplotlibQWidget'

    def set_data(self, *args, **kwargs):
        pass

    def save_report(self, folder_name='./'):
        self.figure.savefig(f'{folder_name}/{self.png_name}.png')
