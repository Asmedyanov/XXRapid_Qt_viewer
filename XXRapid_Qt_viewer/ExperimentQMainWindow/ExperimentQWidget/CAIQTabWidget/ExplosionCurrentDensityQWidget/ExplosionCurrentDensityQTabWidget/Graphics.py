from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, df_current_density):
        super().__init__()
        self.ax.set(
            title='explosion current density',
            xlabel='foil width, mm',
            ylabel='$J_{avg},\\times 10^7 A/cm^2$'
        )
        self.df_current_density = df_current_density.loc[
            ((df_current_density['width'] > 5) & (df_current_density['width'] < 15))]
        self.current_density_plot, = self.ax.plot(self.df_current_density['width'],
                                                  self.df_current_density['current_density'] * 1e-11)

    def set_data(self, df_current_density):
        self.df_current_density = df_current_density
        self.current_density_plot.set_data(self.df_current_density['width'],
                                           self.df_current_density['current_density'] * 1e-11)
        self.changed.emit()
