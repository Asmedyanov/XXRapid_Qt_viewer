from .MatplotlibQWidget import *
import os
import numpy as np
import pandas as pd


class MatplotlibSingeAxQWidget(MatplotlibQWidget):
    def __init__(self, png_name='SingleAxFigure'):
        super().__init__()
        self.png_name = png_name
        self.ax = self.figure.add_subplot(111)
        self.changed.connect(self.on_changed)
        self.ax.grid(ls=':')

    def on_changed(self):
        self.ax.relim()
        self.ax.autoscale_view()
        super().on_changed()

    def save_report(self, folder_name=None):
        if folder_name is None:
            folder_name = 'No_name_reports'
            if folder_name not in os.listdir():
                os.makedirs(folder_name)
        self.figure.savefig(f'{folder_name}/{self.png_name}.png')
