from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *
from .Settings import *


class IdotQWidget(SettingsMPLQWidget):

    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'I_dot'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.CurrentQWidget = self.parent.CurrentQWidget
        self.CurrentQWidget.changed.connect(self.refresh)
        self.t_end = self.parent.t_end
        self.df_current = self.CurrentQWidget.current_df_to_plot
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.MPLQWidget.png_name = 'Idot'
        self.MPLQWidget.ax.set(
            xlabel='$t, \\mu s$',
            ylabel='$\\dot I, kA/ns$',
            title='dI/dt'
        )
        self.df_idot = self.get_df_idot()
        self.df_idot_to_plot = self.get_idot_to_plot()
        self.dt = self.get_dt()
        self.N_smoothing = self.get_n_smooth()
        self.df_idot_smoothed = self.get_df_idot_smoothed()
        self.df_idot_smoothed_to_plot = self.get_idot_smoothed_to_plot()
        self.IdotPlot, = self.MPLQWidget.ax.plot(
            self.df_idot_to_plot['time'] * 1e6,
            self.df_idot_to_plot['Units'] * 1e-12,
            label='original')
        self.IdotPlot_smoothed, = self.MPLQWidget.ax.plot(
            self.df_idot_smoothed_to_plot['time'] * 1e6,
            self.df_idot_smoothed_to_plot['Units'] * 1e-12,
            label='smoothed')
        self.MPLQWidget.ax.legend()

    def get_idot_smoothed_to_plot(self):
        return self.df_idot_smoothed.loc[
            ((self.df_idot_smoothed['time'] > 0) & (self.df_idot_smoothed['time'] < self.t_end))]

    def get_idot_to_plot(self):
        return self.df_idot.loc[((self.df_idot['time'] > 0) & (self.df_idot['time'] < self.t_end))]

    def get_df_idot_smoothed(self):
        return self.df_idot.rolling(self.N_smoothing, min_periods=1).mean()

    def get_dt(self):
        return np.gradient(self.df_current['time'].values).mean()

    def get_n_smooth(self):
        return int(self.SettingsBox.SmoothingSettingsLine.value * 1.0e-9 / self.dt)

    def get_df_idot(self):
        df_idot = pd.DataFrame({
            'time': self.df_current['time'],
            'Units': np.gradient(self.df_current['Units'].values) / np.gradient(self.df_current['time'].values)
        })
        return df_idot

    def on_settings_box(self):
        self.N_smoothing = self.get_n_smooth()
        self.df_idot_smoothed = self.get_df_idot_smoothed()
        self.df_idot_smoothed_to_plot = self.get_idot_smoothed_to_plot()
        self.IdotPlot_smoothed.set_data(
            self.df_idot_smoothed_to_plot['time'] * 1e6,
            self.df_idot_smoothed_to_plot['Units'] * 1e-12)
        super().on_settings_box()

    def refresh(self):
        try:
            self.df_idot = self.get_df_idot()
            self.df_idot_to_plot = self.get_idot_to_plot()
            self.dt = self.get_dt()
            self.df_current = self.CurrentQWidget.CurrentDF.copy()
        except Exception as ex:
            print(ex)
        self.IdotPlot.set_data(
            self.df_idot_to_plot['time'] * 1e6,
            self.df_idot_to_plot['Units'] * 1e-12)
        self.on_settings_box()

    def save_report(self):
        self.MPLQWidget.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
        self.df_idot_smoothed_to_plot.to_csv(f'{self.parent.report_path}/{self.settings_key}.csv')

    def save_origin_pro(self, op):
        sheet = op.new_sheet(lname=self.settings_key)
        sheet.from_df(self.df_idot_smoothed_to_plot)
        graph = op.new_graph(lname=self.settings_key)
        plot = graph[0].add_plot(sheet, colx=0, coly=1)
        graph[0].rescale()
