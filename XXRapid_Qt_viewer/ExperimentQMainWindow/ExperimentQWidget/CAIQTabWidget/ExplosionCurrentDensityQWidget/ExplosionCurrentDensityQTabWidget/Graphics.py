from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.ax.set(
            title='explosion current density',
            xlabel='foil width, mm',
            ylabel='$J_{avg},\\times 10^7 A/cm^2$'
        )
        self.df = self.parent.current_df
        self.df_current_density = self.df.loc[
            ((self.df['width'] > 5) & (self.df['width'] < 15))]
        self.current_density_plot, = self.ax.plot(self.df_current_density['width'],
                                                  self.df_current_density['current_density'] * 1e-11)

    def refresh(self):
        self.df = self.parent.current_df
        self.df_current_density = self.df.loc[
            ((self.df['width'] > 5) & (self.df['width'] < 15))]
        self.current_density_plot.set_data(self.df_current_density['width'],
                                           self.df_current_density['current_density'] * 1e-11)
        self.changed.emit()
