from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve2d
from PyQt5.QtCore import pyqtSignal


class Tracer_tab(QWidget):
    tracer_changed = pyqtSignal()

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

        self.cid_1 = self.figure.canvas.mpl_connect('button_press_event', self.mouse_event_press)
        self.cid_2 = self.figure.canvas.mpl_connect('button_release_event', self.mouse_event_release)

    def mouse_event_press(self, event):
        self.x_1, self.y_1 = int(event.xdata), int(event.ydata)
        self.Front_line.set_data([self.x_1, self.x_2], [self.y_1, self.y_2])
        self.figure.canvas.draw()

    def mouse_event_release(self, event):
        self.x_2, self.y_2 = int(event.xdata), int(event.ydata)
        self.Front_line.set_data([self.x_1, self.x_2], [self.y_1, self.y_2])
        self.figure.canvas.draw()
        self.tracer_changed.emit()

    def set_data(self, array_1):
        N=2
        conv_array = np.ones((N, N)) / N**2
        self.image_array = convolve2d(array_1, conv_array, mode='same')
        #self.image_array=array_1
        try:
            self.image_plot.set_data(self.image_array)
        except:
            self.image_plot = self.ax.imshow(self.image_array, cmap='gray')
        self.image_width = array_1.shape[1]
        self.image_hight = array_1.shape[0]
        self.x_1 = 0
        self.y_1 = self.image_hight - 1
        self.x_2 = self.image_width - 1
        self.y_2 = 0
        try:
            self.Front_line.set_data([self.x_1, self.x_2], [self.y_1, self.y_2])
        except:
            self.Front_line, = self.ax.plot([self.x_1, self.x_2], [self.y_1, self.y_2],'o-r')
        self.figure.canvas.draw()
