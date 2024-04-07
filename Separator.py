from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class Separator(QWidget):
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

    def set_data(self, array_1, dx):
        self.ax.imshow(array_1, cmap='gray')
        try:
            self.Horizont.set_data([0, array_1.shape[1] - 1], [array_1.shape[0] // 2, array_1.shape[0] // 2])
            self.Vertical.set_data([array_1.shape[1] // 2, array_1.shape[1] // 2], [0, array_1.shape[0] - 1])
        except:
            self.Horizont, = self.ax.plot([0, array_1.shape[1] - 1], [array_1.shape[0] // 2, array_1.shape[0] // 2])
            self.Vertical, = self.ax.plot([array_1.shape[1] // 2, array_1.shape[1] // 2], [0, array_1.shape[0] - 1])
        self.figure.canvas.draw()
