from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np


class Single_camera(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots(ncols=2)
        self.figure.set_layout_engine(layout='tight')

        self.ax[0].grid(linestyle='dotted')
        self.ax[1].grid(linestyle='dotted')
        self.ax[0].set(
            title='before',
        )
        self.ax[1].set(
            title='shot',
            yticklabels=[]
        )
        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def set_data(self, image_1, image_2):
        self.ax[0].imshow(image_1)
        self.ax[1].imshow(image_2)
        self.figure.canvas.draw()

