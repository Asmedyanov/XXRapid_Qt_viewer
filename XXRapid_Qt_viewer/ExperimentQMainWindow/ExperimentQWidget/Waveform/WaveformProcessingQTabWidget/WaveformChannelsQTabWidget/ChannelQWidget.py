from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *
from .ChannelSettingsQWidget import *


class ChannelQWidget(SettingsMPLQWidget):
    def __init__(self, df, settings_dict=None):
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=ChannelSettingsQWidget(settings_dict)
        )
        self.df_original = df
        self.MPLQWidget.ax.set(
            xlabel='t, s',
            ylabel='Units'
        )
        self.df_scaled = pd.DataFrame({
            'time': self.df_original['time'],
            'Units': self.df_original[
                         'Volts'] * self.SettingsBox.Coefficient + self.SettingsBox.Shift
        })
        self.dt = np.mean(np.gradient(self.df_original['time']))
        self.NSmooth = int(self.SettingsBox.TauSmooth / self.dt) + 1
        self.df_smoothed = self.df_scaled.rolling(self.NSmooth, min_periods=1).mean()
        self.ScaledPlot, = self.MPLQWidget.ax.plot(self.df_scaled['time'],
                                                   self.df_scaled['Units'], label='Original')
        self.SmoothedPlot, = self.MPLQWidget.ax.plot(self.df_smoothed['time'],
                                                     self.df_smoothed['Units'], label='Smoothed')

        self.MPLQWidget.ax.legend()

    def on_settings_box(self):
        n_smooth = int(self.SettingsBox.TauSmooth / self.dt) + 1
        self.df_scaled['Units'] = self.df_original[
                                      'Volts'] * self.SettingsBox.Coefficient + self.SettingsBox.Shift
        self.df_smoothed = self.df_scaled.rolling(n_smooth, min_periods=1).mean()
        self.SmoothedPlot.set_data(
            self.df_smoothed['time'],
            self.df_smoothed['Units']
        )
        self.ScaledPlot.set_data(
            self.df_scaled['time'],
            self.df_scaled['Units']
        )
        self.MPLQWidget.ax.relim()
        self.MPLQWidget.ax.autoscale_view()
        super().on_settings_box()

    def set_data(self, df_original):
        self.df_original = df_original
        self.OriginalPlot.set_data(
            self.df_original['time'],
            self.df_original['Volts'],
        )
        self.dt = np.mean(np.gradient(self.df_original['time']))
        self.NSmooth = int(self.TauSmooth / self.dt) + 1

        self.df_smoothed = self.df_original.rolling(self.NSmooth, min_periods=1).mean()

        self.SmoothedPlot.set_data(
            self.df_smoothed['time'],
            self.df_smoothed['Volts']
        )
        self.ax.relim()
        self.ax.autoscale_view()

    def save_report(self, folder_name):
        self.MPLQWidget.figure.savefig(f'{folder_name}/{self.SettingsBox.Diagnostics}.png')
        self.df_smoothed.to_csv(f'{folder_name}/{self.SettingsBox.Diagnostics}.csv')

    def set_settings(self, settings_dict=None):
        self.SettingsBox.set_settings(settings_dict)
        self.SettingsDict = self.SettingsBox.SettingsDict
