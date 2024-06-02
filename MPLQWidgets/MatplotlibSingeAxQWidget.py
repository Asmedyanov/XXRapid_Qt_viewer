from MatplotlibQWidget import *
import os


class MatplotlibSingeAxQWidget(MatplotlibQWidget):
    def __init__(self, png_name='SingleAxFigure'):
        super().__init__()
        self.png_name = png_name
        self.ax = self.figure.add_subplot(111)
        self.changed.connect(self.OnChanged)
        self.ax.grid(ls=':')

    def OnChanged(self):
        self.ax.relim()
        self.ax.autoscale_view()
        self.figure.canvas.draw()

    def save_report(self, folder_name=None):
        if folder_name is None:
            folder_name = 'No_name_reports'
            if folder_name not in os.listdir():
                os.makedirs(folder_name)
        self.figure.savefig(f'{folder_name}/{self.png_name}.png')
