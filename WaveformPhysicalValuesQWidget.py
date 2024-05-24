from PyQt5.QtWidgets import QTabWidget
from WaveformCurrentQWidget import *
from WaveformFullVoltageQWidget import *
from WaveformIdotQWidget import *


class WaveformPhysicalValuesQWidget(QTabWidget):
    changed = pyqtSignal()

    def __init__(self, physical_df_dict=None, settings_dict=None, timeshift=0):
        super().__init__()
        self.WaveformCurrentQWidget = WaveformCurrentQWidget(physical_df_dict['Current'], timeshift)
        self.addTab(self.WaveformCurrentQWidget, 'Waveform_current')
        self.WaveformFullVoltageQWidget = WaveformFullVoltageQWidget(physical_df_dict['Voltage'], timeshift)
        self.addTab(self.WaveformFullVoltageQWidget, 'Full voltage')
        settings_dict_default = None
        try:
            settings_dict_default = settings_dict['I_dot']
        except:
            pass
        self.WaveformIdotQWidget = WaveformIdotQWidget(df_current=physical_df_dict['Current'], timeshift=timeshift,
                                                       settings_dict=settings_dict_default)
        self.SettingsDict = {'I_dot': self.WaveformIdotQWidget.SettingsDict}
        self.WaveformIdotQWidget.changed.connect(self.OnWaveformIdotQWidgetChanged)

        self.addTab(self.WaveformIdotQWidget, 'Current derivative')

    def OnWaveformIdotQWidgetChanged(self):
        self.SettingsDict['I_dot'] = self.WaveformIdotQWidget.SettingsDict
        self.changed.emit()

    def set_data(self, physical_df_dict=None, timeshift=0):
        self.WaveformCurrentQWidget.set_data(physical_df_dict['Current'], timeshift)
        self.WaveformFullVoltageQWidget.set_data(physical_df_dict['Voltage'], timeshift)
        self.WaveformIdotQWidget.set_data(physical_df_dict['Current'])
        self.changed.emit()
