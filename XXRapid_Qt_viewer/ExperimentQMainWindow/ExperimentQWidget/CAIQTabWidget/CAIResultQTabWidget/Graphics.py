from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent, df_cai):
        self.parent = parent
        super().__init__()
        self.ax.set(
            title='CAI',
            xlabel='$J_{avg},\\times 10^7 A/cm^2$',
            ylabel='h$\\times 10^9 A^2*s/cm^4$'
        )
        self.df_cai = df_cai.loc[
            ((df_cai['width'] > 5) & (df_cai['width'] < 15))]
        self.cai_plot, = self.ax.plot(self.df_cai['current_density'] * 1e-11,
                                      self.df_cai['cai'] * 1e-10,'o')
        self.comsol_cai_plot = self.ax.errorbar(1e-7 * self.parent.comsol_df['current_density'],
                                                 1e-9 * self.parent.comsol_df['cai'],
                                                 xerr=1e-7 * self.parent.comsol_df['current_density'] * 0.1,
                                                 yerr=1e-9 * self.parent.comsol_df['cai'] * 0.2,
                                                 fmt='o')

    def set_data(self, df_current_density):
        self.df_current_density = df_current_density
        self.cai_plot.set_data(self.df_cai['current_density'] * 1e-11,
                               self.df_cai['cai'] * 1e-10)
        self.changed.emit()
