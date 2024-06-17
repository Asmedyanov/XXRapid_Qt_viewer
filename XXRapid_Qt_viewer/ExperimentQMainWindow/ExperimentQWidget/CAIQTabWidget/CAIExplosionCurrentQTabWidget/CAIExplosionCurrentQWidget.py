from MPLQWidgets.MatplotlibSingeAxQWidget import *


class CAIExplosionCurrentQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, df_current):
        super().__init__()
        self.ax.set(
            title='Explosion current',
            xlabel='foil width, mm',
            ylabel='I, kA'
        )
        self.df_current = df_current
        self.current_plot, = self.ax.plot(self.df_current['width'], self.df_current['current'] * 1e-3)

    def set_data(self, df_current):
        self.df_current = df_current
        self.current_plot.set_data(self.df_current['width'], self.df_current['current'] * 1e-3)
        self.changed.emit()
