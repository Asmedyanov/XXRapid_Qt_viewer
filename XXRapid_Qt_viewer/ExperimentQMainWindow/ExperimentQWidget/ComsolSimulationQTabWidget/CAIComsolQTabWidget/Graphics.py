from MPLQWidgets.MatplotlibSingeAxQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.CAI_dict = self.parent.current_dict
        super().__init__()
        self.ax.set(
            ylabel='$h_{edge} \\times 10^{9} A^2s/cm^4$',
            xlabel='$J_{edge} \\times 10^{7} A/cm^2$'
        )
        self.error_bar = self.ax.errorbar(
            np.array(self.CAI_dict['j_exp'])*1e-7,
            np.array(self.CAI_dict['h_exp'])*1e-9,
            xerr=np.array(self.CAI_dict['j_exp'])*1e-7 * 0.15,
            yerr=np.array(self.CAI_dict['h_exp'])*1e-9 * 0.25,
            fmt='o'

        )

    def refresh(self):
        self.tof_dict = self.parent.tof_dict
