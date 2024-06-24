from MPLQWidgets.MatplotlibSingeAxQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.comsol_current_df = self.parent.comsol_current_df
        self.tof_df = self.parent.tof_dict[self.parent.current_key]
        self.CAI_dict = self.parent.CAI_dict[self.parent.current_key]
        super().__init__()
        self.ax.set(
            xlabel='time, ns',
            ylabel='$J_{edge} \\times 10^{8} A/cm^2$'
        )
        self.current_density_plot_dict = dict()
        self.t_exp_plot_dict = dict()
        self.CAI_dict['width'] = []  # mm
        self.CAI_dict['t_exp'] = []  # ns
        self.CAI_dict['j_exp'] = []  # A/cm^2
        self.CAI_dict['h_exp'] = []  # A^2*s/cm^4

        for my_key in self.comsol_current_df.columns:
            if my_key.startswith('time'):
                time = self.comsol_current_df[my_key].values
            else:
                width = float(my_key.split(' ')[0])
                t_exp = self.tof_df['onset_time'].loc[self.tof_df['width'] < width].max()
                j_exp_index = np.argwhere(time < t_exp * 1e-9).max()

                current_density = self.comsol_current_df[my_key].values
                j_exp = current_density[j_exp_index]
                h_exp = np.sum(current_density[:j_exp_index] ** 2 * np.gradient(time[:j_exp_index]))
                self.CAI_dict['width'].append(width)
                self.CAI_dict['t_exp'].append(t_exp)
                self.CAI_dict['j_exp'].append(j_exp)
                self.CAI_dict['h_exp'].append(h_exp)

                self.current_density_plot_dict[my_key], = self.ax.plot(time * 1e9,
                                                                       current_density * 1e-8,
                                                                       label=my_key)
                self.t_exp_plot_dict[my_key] = self.ax.axvline(t_exp, linestyle=':',
                                                               c='r')

        self.ax.legend()

    def refresh(self):
        self.tof_dict = self.parent.tof_dict
