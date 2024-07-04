from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = self.parent.current_key
        self.report_path = self.parent.report_path
        super().__init__()
        self.ax.set(
            title='explosion current density',
            xlabel='foil width, mm',
            ylabel='$J_{avg},\\times 10^7 A/cm^2$'
        )
        self.df = self.parent.current_df
        self.df_current_density = self.df
        self.current_density_plot, = self.ax.plot(self.df_current_density['width'],
                                                  self.df_current_density['current_density']*1e-5)

    def refresh(self):
        self.df = self.parent.current_df
        self.df_current_density = self.df
        self.current_density_plot.set_data(self.df_current_density['width'],
                                           self.df_current_density['current_density']*1e-5)
        self.changed.emit()

    def save_report(self):
        self.figure.savefig(f'{self.report_path}/{self.settings_key}.png')
        self.df_current_density.to_csv(f'{self.report_path}/{self.settings_key}.csv')
