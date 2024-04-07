import numpy as np
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
        self.figure.set_layout_engine(layout='tight')
        self.ax.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])
        self.ax.set_title(self.title)
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")

        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def compare_2_image(self, image_1, image_2):
        self.figure.clear()

        self.grid = self.figure.add_gridspec(ncols=2, nrows=1).subplots()
        self.grid[0].grid(linestyle='dotted')
        self.grid[1].grid(linestyle='dotted')
        self.grid[0].set(
            title='before',
        )
        self.grid[0].imshow(image_1)
        self.grid[1].set(
            title='shot',
            yticklabels=[]
        )
        self.grid[1].imshow(image_2)
        self.figure.canvas.draw()

    def compare_2_image_arrays(self, array_1, array_2):
        self.figure.clear()

        self.grid = self.figure.add_gridspec(ncols=array_1.shape[0], nrows=2).subplots()
        self.grid[0, 0].set(
            ylabel='before'
        )

        self.grid[1, 0].set(
            ylabel='shot'
        )
        for i in range(array_1.shape[0]):
            self.grid[0, i].imshow(array_1[i])
            self.grid[0, i].grid(linestyle='dotted')

            self.grid[1, i].imshow(array_2[i])
            self.grid[1, i].grid(linestyle='dotted')
            if i != 0:
                self.grid[0, i].set_yticklabels([])
                self.grid[1, i].set_yticklabels([])
            self.grid[0, i].set_xticklabels([])
            self.figure.canvas.draw()

    def overlap_2_image_arrays(self, array_1, array_2, dx):
        self.figure.clear()

        self.grid = self.figure.add_gridspec(ncols=2, nrows=2).subplots()
        self.grid[0, 0].set(
            title='Image 1, mm',
            xticklabels=[]
        )
        self.grid[0, 1].set(
            title='Image 2, mm',
            xticklabels=[], yticklabels=[]
        )
        self.grid[1, 0].set(
            xlabel='Image 3, mm'
        )
        self.grid[1, 1].set(
            xlabel='Image 4, mm',
            yticklabels=[]
        )

        '''self.grid[0, 0].grid(linestyle='dotted')
        self.grid[0, 1].grid(linestyle='dotted')
        self.grid[1, 0].grid(linestyle='dotted')
        self.grid[1, 1].grid(linestyle='dotted')'''

        array_2_clean = np.where(array_2 > 1.0 * array_1, 1.0 * array_1, array_2)
        overlapped_array = np.where(array_1 == 0, 0, array_2_clean / array_1)

        extent = [-array_1.shape[2] * dx // 2,
                  array_1.shape[2] * dx // 2,
                  array_1.shape[1] * dx // 2,
                  -array_1.shape[1] * dx // 2]

        self.grid[0, 0].imshow(overlapped_array[0], cmap='gray', extent=extent)
        self.grid[0, 1].imshow(overlapped_array[1], cmap='gray', extent=extent)
        self.grid[1, 0].imshow(overlapped_array[2], cmap='gray', extent=extent)
        self.grid[1, 1].imshow(overlapped_array[3], cmap='gray', extent=extent)
        self.grid[0, 0].grid()
        self.grid[0, 1].grid()
        self.grid[1, 0].grid()
        self.grid[1, 1].grid()
        self.figure.canvas.draw()

    def overlap_3_camera(self, array_1, array_2, dx):
        self.figure.clear()

        self.grid = self.figure.add_gridspec(ncols=3, nrows=1).subplots()
        self.grid[0].set(
            title='Image 1, mm',
        )
        self.grid[1].set(
            title='Image 2, mm',
            yticklabels=[]
        )
        self.grid[2].set(
            title ='Image 3, mm',
            yticklabels=[]
        )
        array_2_clean = np.where(array_2 > 1.0 * array_1, 1.0 * array_1, array_2)
        overlapped_array = np.where(array_1 == 0, 0, array_2_clean / array_1)

        extent = [-array_1.shape[2] * dx // 2,
                  array_1.shape[2] * dx // 2,
                  array_1.shape[1] * dx // 2,
                  -array_1.shape[1] * dx // 2]

        for i in range(3):
            self.grid[i].grid()
            self.grid[i].imshow(overlapped_array[i], cmap='gray', extent=extent)
        self.figure.canvas.draw()
