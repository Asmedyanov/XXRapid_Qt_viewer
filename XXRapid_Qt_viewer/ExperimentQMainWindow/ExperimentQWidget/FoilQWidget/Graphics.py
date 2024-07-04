from MPLQWidgets.MatplotlibSingeAxQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.ax.set(
            title=f'Foil shape {self.parent.mass:3.3f} g',
            xlabel='y, mm',
            ylabel='x, mm',
        )
        self.plot, = self.ax.plot(self.parent.points_x, self.parent.points_y, '-o')

    def refresh(self):
        self.ax.set(
            title=f'Foil shape {self.parent.mass:3.3f} g')
        self.plot.set_data(self.parent.points_x, self.parent.points_y)
        self.changed.emit()

    def save_report(self):
        self.figure.savefig(f'{self.report_path}/{self.current_key}')
