from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class Four_overlapped_frames(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots(ncols=2, nrows=2)
        self.figure.set_layout_engine(layout='tight')
        for i in range(2):
            for j in range(2):
                self.ax[0, j].set(
                    xticklabels=[]
                )
                if j > 0:
                    self.ax[i, j].set(
                        yticklabels=[]
                    )
                self.ax[i, j].grid(linestyle='dotted')
        self.ax[0, 0].set_title('Image 1, mm')
        self.ax[0, 1].set_title('Image 2, mm')
        self.ax[1, 0].set_xlabel('Image 3, mm')
        self.ax[1, 1].set_xlabel('Image 4, mm')
        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def set_data(self, array_1, dx):
        extent = [-array_1.shape[2] * dx // 2,
                  array_1.shape[2] * dx // 2,
                  array_1.shape[1] * dx // 2,
                  -array_1.shape[1] * dx // 2]
        self.ax[0, 0].imshow(array_1[0], cmap='gray', extent=extent)
        self.ax[0, 1].imshow(array_1[1], cmap='gray', extent=extent)
        self.ax[1, 0].imshow(array_1[2], cmap='gray', extent=extent)
        self.ax[1, 1].imshow(array_1[3], cmap='gray', extent=extent)
        self.figure.canvas.draw()
