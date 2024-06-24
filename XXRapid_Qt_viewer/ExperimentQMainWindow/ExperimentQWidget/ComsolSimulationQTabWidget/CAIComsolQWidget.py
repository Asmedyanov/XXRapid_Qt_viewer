from MPLQWidgets.MatplotlibSingeAxQWidget import *


class CAIComsolQWidget(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        super().__init__()
        self.ax.set(
            title='CAI',
            ylabel='h $\\times 10^9 A^2 s/cm^4$',
            xlabel='J $\\times 10^7 A/cm^2$'
        )
        self.parent = parent
        self.w_list = self.parent.ComsolCurrentQTabWidget.width_list_number
        self.j_list = self.parent.ComsolCurrentQTabWidget.j_exp_array
        self.h_list = self.parent.ComsolCurrentQTabWidget.h_exp_array
        self.cai_plot = self.ax.errorbar(1e-7 * np.array(self.j_list), 1e-9 * np.array(self.h_list),
                                         xerr=1e-7 * np.array(self.j_list) * 0.1,
                                         yerr=1e-9 * np.array(self.h_list) * 0.2,
                                         fmt='o')

    def update(self):
        self.w_list = self.parent.ComsolCurrentQTabWidget.width_list_number
        self.j_list = self.parent.ComsolCurrentQTabWidget.j_exp_array
        self.h_list = self.parent.ComsolCurrentQTabWidget.h_exp_array
        self.cai_plot.set_data(1e-7 * np.array(self.j_list), 1e-9 * np.array(self.h_list),
                               xerr=1e-7 * np.array(self.j_list) * 0.1,
                               yerr=1e-9 * np.array(self.h_list) * 0.2
                               )
        self.changed.emit()

    def get_cai_df(self):
        df = pd.DataFrame({
            'width': np.array(self.w_list),
            'current_density': np.array(self.j_list),
            'cai': np.array(self.h_list)
        })
        return df
