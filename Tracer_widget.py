from Matplotlib_qtwidget import Matplotlib_qtwidget
import numpy as np
from scipy.signal import convolve2d
from PyQt5.QtCore import pyqtSignal


class Tracer_widget(Matplotlib_qtwidget):
    def __init__(self):
        super().__init__()
        self.ax = self.figure.add_subplot(111)
        self.ax.grid(linestyle='dotted')
        self.main_data_dict = {}
        self.cid_1 = self.figure.canvas.mpl_connect('button_press_event', self.mouse_event_press)
        self.cid_2 = self.figure.canvas.mpl_connect('button_release_event', self.mouse_event_release)

    def mouse_event_press(self, event):
        self.x_1, self.y_1 = int(event.xdata), int(event.ydata)
        self.Front_line.set_data([self.x_1, self.x_2], [self.y_1, self.y_2])
        self.figure.canvas.draw()

    def update_main_data_dict(self):
        self.main_data_dict = {
            'x_1': self.x_1,
            'y_1': self.y_1,
            'x_2': self.x_2,
            'y_2': self.y_2,
        }

    def mouse_event_release(self, event):
        self.x_2, self.y_2 = int(event.xdata), int(event.ydata)
        self.Front_line.set_data([self.x_1, self.x_2], [self.y_1, self.y_2])
        self.figure.canvas.draw()
        self.update_main_data_dict()
        self.changed.emit()

    def set_data(self, array_1, base_dict=None):
        N = 2
        conv_array = np.ones((N, N)) / N ** 2
        self.image_array = convolve2d(array_1, conv_array, mode='same')
        # self.image_array=array_1
        try:
            self.image_plot.set_data(self.image_array)
        except:
            self.image_plot = self.ax.imshow(self.image_array, cmap='gray')
        self.image_width = array_1.shape[1]
        self.image_hight = array_1.shape[0]
        if base_dict is None:
            self.x_1 = 0
            self.y_1 = self.image_hight - 1
            self.x_2 = self.image_width - 1
            self.y_2 = 0
        else:
            self.x_1 = int(base_dict['x_1'])
            self.y_1 = int(base_dict['y_1'])
            self.x_2 = int(base_dict['x_2'])
            self.y_2 = int(base_dict['y_2'])
        self.update_main_data_dict()
        try:
            self.Front_line.set_data([self.x_1, self.x_2], [self.y_1, self.y_2])
        except:
            self.Front_line, = self.ax.plot([self.x_1, self.x_2], [self.y_1, self.y_2], 'o-r')
        self.figure.canvas.draw()
