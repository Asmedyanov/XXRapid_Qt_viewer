from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
class MPL_tab(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.layout = QVBoxLayout()

        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.ax.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])
        self.ax.set_title(self.title)
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")

        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)