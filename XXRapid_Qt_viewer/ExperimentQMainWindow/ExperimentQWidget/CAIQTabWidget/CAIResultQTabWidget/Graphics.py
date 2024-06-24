from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.ax.set(
            title='CAI',
            xlabel='$J_{avg},\\times 10^7 A/cm^2$',
            ylabel='h$\\times 10^9 A^2*s/cm^4$'
        )
        self.df = self.parent.current_df
        self.df_cai = self.df.loc[
            ((self.df['width'] > 5) & (self.df['width'] < 15))]
        self.cai_plot, = self.ax.plot(self.df_cai['current_density'] * 1e-11,
                                      self.df_cai['cai'] * 1e-9, 'o')
        try:
            self.comsol_dict = self.parent.current_comsol
            self.j_exp = np.array(self.comsol_dict['j_exp'])*2
            self.h_exp = np.array(self.comsol_dict['h_exp'])
            self.dj_exp = 0.15 * self.j_exp
            self.dh_exp = 0.25 * self.h_exp
            self.comsol_cai_plot = self.ax.errorbar(1e-7 * self.j_exp,
                                                    1e-9 * self.h_exp,
                                                    xerr=1e-7 * self.dj_exp,
                                                    yerr=1e-9 * self.dh_exp,
                                                    fmt='o')
        except Exception as ex:
            print(ex)

    def set_data(self, df_current_density):
        self.df_current_density = df_current_density
        self.cai_plot.set_data(self.df_cai['current_density'] * 1e-11,
                               self.df_cai['cai'] * 1e-10)
        self.changed.emit()
