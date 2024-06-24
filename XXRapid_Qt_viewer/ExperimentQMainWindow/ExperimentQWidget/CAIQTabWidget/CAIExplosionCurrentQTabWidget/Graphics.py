from MPLQWidgets.MatplotlibSingeAxQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.ax.set(
            title='Explosion current',
            xlabel='foil width, mm',
            ylabel='I, kA'
        )
        self.df_current = self.parent.current_df
        self.current_plot, = self.ax.plot(self.df_current['width'], self.df_current['current'] * 1e-3)

    def refresh(self):
        self.df_current = self.parent.current_df
        self.current_plot.set_data(self.df_current['width'], self.df_current['current'] * 1e-3)
        self.changed.emit()
