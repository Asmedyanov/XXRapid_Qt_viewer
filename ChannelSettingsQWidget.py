from PyQt5.QtWidgets import QVBoxLayout

from MySettingsQWidget import *


class ChannelSettingsQWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.QVBoxLayout = QVBoxLayout()
        self.setLayout(self.QVBoxLayout)
        self.DiagnosticsSettingsQWidget = MySettingsQWidget(
            name='Diagnostics',
            options_list=['Rogowski_coil',
                          'Systron',
                          'XXRapid_trig_out',
                          'Tektronix_VD']
        )
        self.QVBoxLayout.addWidget(self.DiagnosticsSettingsQWidget)
        self.SmoothingSettingsQWidget = MySettingsQWidget(
            name='Smoothing',
            default=200,
            comment='counts'
        )
        self.QVBoxLayout.addWidget(self.SmoothingSettingsQWidget)
        self.CoefficientSettingsQWidget = MySettingsQWidget(
            name='Coefficient',
            default=300,
            comment='Unit/Volt'
        )
        self.QVBoxLayout.addWidget(self.CoefficientSettingsQWidget)
