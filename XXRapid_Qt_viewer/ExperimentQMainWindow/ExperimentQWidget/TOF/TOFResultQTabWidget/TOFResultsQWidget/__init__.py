from MPLQWidgets.SettingsMPLQWidget import *
from .Graphics import *
from .Settings import *


class TOFResultsQWidget(SettingsMPLQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = self.parent.current_key
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.report_path = self.parent.report_path

        self.velocity_df = self.parent.current_df
        self.dw = np.gradient(self.velocity_df['width']).mean()
        self.Settings = Settings(self)
        self.velocity_smoothed_df = self.get_velocity_smoothed_df()
        self.parent.velocity_smoothed_dict[self.settings_key] = self.velocity_smoothed_df

        super().__init__(
            MPLQWidget=Graphics(self),
            settings_box=self.Settings
        )

    def get_velocity_smoothed_df(self):
        w_smooth = self.Settings.SmoothingSettingLine.value
        n_smooth = int(w_smooth / self.dw) + 1
        smoothed_df = self.velocity_df.rolling(n_smooth, min_periods=1).mean()
        return smoothed_df

    def on_settings_box(self):
        self.velocity_smoothed_df = self.get_velocity_smoothed_df()
        self.MPLQWidget.refresh()
        self.parent.velocity_smoothed_dict[self.settings_key] = self.velocity_smoothed_df
        super().on_settings_box()

    def save_report(self):
        self.MPLQWidget.figure.savefig(f'{self.report_path}/{self.settings_key}.png')
        self.velocity_smoothed_df.to_csv(f'{self.report_path}/{self.settings_key}.csv')
