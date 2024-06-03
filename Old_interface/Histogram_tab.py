from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class Histogram_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots(ncols=4, nrows=2)
        self.figure.set_layout_engine(layout='tight')
        for i in range(2):
            for j in range(4):

                self.ax[i, j].grid(linestyle='dotted')
        self.ax[0, 0].set_ylabel('Before')
        self.ax[1, 0].set_ylabel('Shot')
        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.hist_line_1 = []
        self.hist_line_2 = []

    def set_data(self, array_1, array_2):
        histogram_list_1 = []
        for image in array_1:
            histogram, bins = np.histogram(image.ravel(), bins=100,range=(1,5.0e3))
            histogram_list_1.append([histogram, bins])
        histogram_list_2 = []
        for image in array_2:
            histogram, bins = np.histogram(image.ravel(), bins=100,range=(1,5.0e3))
            histogram_list_2.append([histogram, bins])
        pass
        for j in range(4):
            self.ax[0, j].clear()
            self.ax[0, j].hist(
                        histogram_list_1[j][0],
                        histogram_list_1[j][1],
                        histtype='bar'
                    )
            self.ax[1, j].clear()
            self.ax[1, j].hist(
                        histogram_list_2[j][0],
                        histogram_list_2[j][1],
                        histtype='bar'
                    )
        self.figure.canvas.draw()
