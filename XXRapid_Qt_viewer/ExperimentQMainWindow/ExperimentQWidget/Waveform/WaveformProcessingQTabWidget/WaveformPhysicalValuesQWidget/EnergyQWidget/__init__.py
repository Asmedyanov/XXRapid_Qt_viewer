from MPLQWidgets.MatplotlibSingeAxTwingQWidget import *


class EnergyQWidget(MatplotlibSingeAxTwinxQWidget):
    def __init__(self, parent):
        self.parent = parent
        self.settings_key = 'Energy'
        self.parent.test_settings_key(self.settings_key)
        self.SettingsDict = self.parent.SettingsDict[self.settings_key]
        self.PowerQWidget = self.parent.PowerQWidget
        self.PowerQWidget.changed.connect(self.refresh)
        self.CurrentQWidget = self.parent.CurrentQWidget
        self.df_power = self.PowerQWidget.df_power.copy()
        self.df_current = self.CurrentQWidget.current_df_to_plot.copy()
        super().__init__('Energy')
        self.ax.set(
            xlabel='t, us',
            ylabel='E, kJ',
            title='Energy'
        )
        self.ax_2.set(
            ylabel='I, kA',
        )
        self.df_current_to_plot = self.get_df_current_to_plot()
        self.dt = self.get_dt()
        self.energy_function_vect = np.vectorize(self.energy_function)
        self.df_energy = self.get_df_energy()

        self.CurrentLine, = self.ax_2.plot(self.df_current_to_plot['time'] * 1e6,
                                           self.df_current_to_plot['Units'] * 1e-3, ':r')
        self.EnergyLine, = self.ax.plot(self.df_energy['time'] * 1e6, self.df_energy['Units'] * 1e-3)

    def get_df_energy(self):
        return pd.DataFrame({
            'time': self.df_power['time'],
            'Units': self.energy_function_vect(self.df_power['time'].values)
        })

    def get_df_current_to_plot(self):
        return pd.DataFrame({
            'time': self.df_current['time'],
            'Units': np.where(self.df_current['Units'].values < 0, 0, self.df_current['Units'].values)
        })

    def get_dt(self):
        return np.mean(np.gradient(self.df_power['time']))

    def energy_function(self, time):
        power_to_sum = self.df_power.loc[self.df_power['time'] < time]
        energy = power_to_sum['Units'].sum() * self.dt
        return energy

    def set_data(self, df_current, df_power=None):
        self.df_current = df_current.copy()
        self.df_power = df_power.copy()
        self.df_current_to_plot = self.get_df_current_to_plot()
        self.dt = self.get_dt()
        self.energy_function_vect = np.vectorize(self.energy_function)
        self.df_energy = self.get_df_energy()
        self.CurrentLine.set_data(self.df_current_to_plot['time'] * 1e6, self.df_current_to_plot['Units'] * 1e-3)
        self.EnergyLine.set_data(self.df_energy['time'] * 1e6, self.df_energy['Units'] * 1e-3)
        self.changed.emit()

    def save_report(self):
        self.figure.savefig(f'{self.parent.report_path}/{self.settings_key}.png')
        self.df_energy.to_csv(f'{self.parent.report_path}/{self.settings_key}.csv')

    def refresh(self):
        self.df_current = self.CurrentQWidget.current_df_to_plot.copy()
        self.df_current_to_plot = self.get_df_current_to_plot()
        self.dt = self.get_dt()
        self.df_energy = self.get_df_energy()
        self.CurrentLine.set_data(self.df_current_to_plot['time'] * 1e6,
                                  self.df_current_to_plot['Units'] * 1e-3)
        self.EnergyLine.set_data(self.df_energy['time'] * 1e6, self.df_energy['Units'] * 1e-3)
        super().changed.emit()
