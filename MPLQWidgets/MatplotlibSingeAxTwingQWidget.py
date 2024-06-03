from .MatplotlibSingeAxQWidget import *


class MatplotlibSingeAxTwinxQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, png_name='SingleAxTwinxFigure'):
        super().__init__(png_name)
        self.ax_2 = self.ax.twinx()
        self.ax_2.tick_params(axis='y', colors='red')
        self.ax_2.yaxis.label.set_color('r')
        self.ax_2.spines["right"].set_edgecolor('r')

    def OnChanged(self):
        self.ax_2.relim()
        self.ax_2.autoscale_view()
        super().OnChanged()

    def save_report(self, folder_name=None):
        if folder_name is None:
            folder_name = 'No_name_reports'
            if folder_name not in os.listdir():
                os.makedirs(folder_name)
        self.figure.savefig(f'{folder_name}/{self.png_name}.png')
