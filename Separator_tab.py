from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSignal


class Separator(QWidget):
    center_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.figure.set_layout_engine(layout='tight')

        self.ax.grid(linestyle='dotted')
        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.cid_1 = self.figure.canvas.mpl_connect('button_press_event', self.On_mouse_click)

    def On_mouse_click(self, event):
        self.center_x, self.center_y = int(event.xdata), int(event.ydata)
        self.Horizont.set_data([0, self.image_width - 1], [self.center_y, self.center_y])
        self.Vertical.set_data([self.center_x, self.center_x], [0, self.image_hight - 1])
        self.figure.canvas.draw()
        self.center_signal.emit()

    def set_data(self, array_1, dx, base_dict=None):
        self.ax.imshow(array_1, cmap='gray')
        if base_dict is None:
            self.center_x = array_1.shape[1] // 2
            self.center_y = array_1.shape[0] // 2
        else:
            print('i took from file')
            self.center_x = int(base_dict['center_x'])
            self.center_y = int(base_dict['center_y'])
        self.image_width = array_1.shape[1]
        self.image_hight = array_1.shape[0]
        try:
            self.Horizont.set_data([0, self.image_width - 1], [self.center_y, self.center_y])
            self.Vertical.set_data([self.center_x, self.center_x], [0, self.image_hight - 1])
        except:
            self.Horizont, = self.ax.plot([0, self.image_width - 1], [self.center_y, self.center_y])
            self.Vertical, = self.ax.plot([self.center_x, self.center_x], [0, self.image_hight - 1])
        self.figure.canvas.draw()

    def get_data_dict(self):
        ret = {
            'center_x': self.center_x,
            'center_y': self.center_y,
        }
        return ret
