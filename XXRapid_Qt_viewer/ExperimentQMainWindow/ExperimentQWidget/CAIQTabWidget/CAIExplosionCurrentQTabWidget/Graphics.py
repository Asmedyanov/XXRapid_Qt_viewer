from MPLQWidgets.MatplotlibSingeAxQWidget import *


class Graphics(MatplotlibSingeAxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.report_path = self.parent.report_path
        self.settings_key = self.parent.current_key
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

    def save_report(self):
        self.figure.savefig(f'{self.report_path}/{self.settings_key}.png')
        self.df_current.to_csv(f'{self.report_path}/{self.settings_key}.csv')
