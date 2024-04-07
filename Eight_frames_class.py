from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class Eight_frames(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots(ncols=4, nrows=2)
        self.figure.set_layout_engine(layout='tight')
        for i in range(2):
            for j in range(4):
                self.ax[0, j].set(
                    xticklabels=[]
                )
                if j > 0:
                    self.ax[i, j].set(
                        yticklabels=[]
                    )
                self.ax[i, j].grid(linestyle='dotted')
        self.ax[0, 0].set_ylabel('Before')
        self.ax[1, 0].set_ylabel('Shot')
        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def set_data(self, array_1, array_2):
        for j in range(4):
            self.ax[0, j].imshow(array_1[j])
            self.ax[1, j].imshow(array_2[j])
        self.figure.canvas.draw()
