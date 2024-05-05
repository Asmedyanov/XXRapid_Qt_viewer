from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np
import Approx_functions


class Expansion_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots(ncols=4)
        self.figure.set_layout_engine(layout='tight')
        self.plot_by_quarts = dict()
        t = np.arange(0, 2 * np.pi, 0.1)
        for i in [1, 2, 3, 4]:
            self.plot_by_quarts[f'Quart_{i}'] = []
            for j in range(8):
                self.plot_by_quarts[f'Quart_{i}'].append(
                    self.ax[i - 1].plot((j + 1) * np.cos(t), (j + 1) * np.sin(t))[0]
                )

        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def set_data(self, base_dict, dx):
        self.base_dict = base_dict
        Expansion_by_quarts_dict = dict()
        for i in [1, 2, 3, 4]:
            Expansion_by_quart = []
            for j in [1, 2, 3, 4]:
                x_1 = int(self.base_dict[f'Frame_{j}'][f'Quart_{i}'][f'Tracer']['x_1'])
                x_2 = int(self.base_dict[f'Frame_{j}'][f'Quart_{i}'][f'Tracer']['x_2'])
                x_data = np.arange(max([x_1, x_2]))
                a = float(self.base_dict[f'Frame_{j}'][f'Quart_{i}']['fronts'][f'Front_1']['a'])
                b = float(self.base_dict[f'Frame_{j}'][f'Quart_{i}']['fronts'][f'Front_1']['b'])
                y_data_before = a * x_data + b
                for k in [2, 3]:
                    db_v = float(self.base_dict[f'Frame_{j}'][f'Quart_{i}']['fronts'][f'Front_{k}']['db_v'])
                    dxt = float(self.base_dict[f'Frame_{j}'][f'Quart_{i}']['fronts'][f'Front_{k}']['dxt'])
                    x0 = float(self.base_dict[f'Frame_{j}'][f'Quart_{i}']['fronts'][f'Front_{k}']['x0'])
                    x_p = float(self.base_dict[f'Frame_{j}'][f'Quart_{i}']['fronts'][f'Front_{k}']['x_p'])
                    y_data_shot = Approx_functions.f_free_style_full(x_data, a, b, db_v, x0, x_p, dxt)
                    expansion = np.abs(y_data_before - y_data_shot) * dx
                    Expansion_by_quart.append({
                        'x': x_data * dx,
                        'y': expansion})
            for j in range(len(Expansion_by_quart)):
                self.plot_by_quarts[f'Quart_{i}'][j].set_data(Expansion_by_quart[j]['x'], Expansion_by_quart[j]['y'])
            self.ax[i-1].relim()
            self.ax[i-1].autoscale_view()
        self.figure.canvas.draw()
