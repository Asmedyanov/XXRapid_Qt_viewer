from MPLQWidgets.SettingsMPLQWidget import *
from MPLQWidgets.MatplotlibSingeAxQWidget import *
from .Settings import *


class ChannelQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.focused_df = self.parent.focused_df
        self.settings_key = self.parent.focused_key
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        super().__init__(
            MPLQWidget=MatplotlibSingeAxQWidget(),
            settings_box=Settings(self)
        )
        self.df_original = self.focused_df.copy()
        self.MPLQWidget.ax.set(
            xlabel='t, s',
            ylabel='Units'
        )
        self.df_scaled = self.get_df_scaled()
        self.df_smoothed = self.get_df_smoothed()

        self.ScaledPlot, = self.MPLQWidget.ax.plot(self.df_scaled['time'],
                                                   self.df_scaled['Units'], label='Original')
        self.SmoothedPlot, = self.MPLQWidget.ax.plot(self.df_smoothed['time'],
                                                     self.df_smoothed['Units'], label='Smoothed')

        self.MPLQWidget.ax.legend()

    def get_df_scaled(self):
        return pd.DataFrame({
            'time': self.df_original['time']+self.SettingsBox.Delay,
            'Units': self.df_original[
                         'Volts'] * self.SettingsBox.Coefficient + self.SettingsBox.Shift
        })

    def get_df_smoothed(self):
        self.dt = np.mean(np.gradient(self.df_original['time']))
        self.NSmooth = int(self.SettingsBox.TauSmooth / self.dt) + 1
        df_smoothed = self.df_scaled.rolling(self.NSmooth, min_periods=1).mean()
        return df_smoothed

    def on_settings_box(self):
        self.df_scaled = self.get_df_scaled()
        self.df_smoothed = self.get_df_smoothed()
        self.SmoothedPlot.set_data(
            self.df_smoothed['time'],
            self.df_smoothed['Units']
        )
        self.ScaledPlot.set_data(
            self.df_scaled['time'],
            self.df_scaled['Units']
        )
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
        self.MPLQWidget.changed.emit()

    def save_report(self, folder_name):
        self.MPLQWidget.figure.savefig(f'{folder_name}/{self.SettingsBox.Diagnostics}.png')
        self.df_smoothed.to_csv(f'{folder_name}/{self.SettingsBox.Diagnostics}.csv')

    def set_settings(self, settings_dict=None):
        self.SettingsBox.set_settings(settings_dict)
        self.SettingsDict = self.SettingsBox.SettingsDict
