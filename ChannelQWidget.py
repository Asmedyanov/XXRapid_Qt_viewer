from MatplotlibQWidget import *
from ChannelSettingsQWidget import *


class ChannelQWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.MainQHBoxLayout = QHBoxLayout()
        self.setLayout(self.MainQHBoxLayout)
        self.MainMatplotlibQWidget = MatplotlibQWidget()
        self.MainQHBoxLayout.addWidget(self.MainMatplotlibQWidget)
        self.ChannelSettingsWidget = QWidget()
        self.MainQHBoxLayout.addWidget(self.ChannelSettingsWidget)
        self.ChannelSettingsQWidget = ChannelSettingsQWidget()
        self.MainQHBoxLayout.addWidget(self.ChannelSettingsQWidget)

        self.NSmooth = self.ChannelSettingsWidget.SmoothingSettingsQWidget.value


        self.Axis = self.MainMatplotlibQWidget.figure.add_subplot(111)
        self.Axis.set(
            xlabel='t, s',
            ylabel='U, V'
        )
        self.OriginalPlot, = self.Axis.plot([0, 0], [0, 0], label='Original')
        self.SmoothedPlot, = self.Axis.plot([0, 0], [0, 0], label='Smoothed')
        self.Axis.legend()

    def set_data(self, df_original):
        self.df_original = df_original
        self.OriginalPlot.set_data(
            self.df_original['time'],
            self.df_original['Volts'],
        )
        self.Axis.relim()
        self.Axis.autoscale_view()

