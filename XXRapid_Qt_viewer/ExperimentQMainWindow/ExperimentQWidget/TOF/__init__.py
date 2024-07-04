from .TOFResultQTabWidget import *
from .MotionQWidget import *
from .PhysicalExpansionQWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class XXRapidTOFQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'TOF')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.XXRapidFrontingQWidget = self.parent.XXRapidFrontingQWidget
        self.FoilQWidget = self.parent.FoilQWidget

        self.WaveformTimingQWidget = self.parent.WaveformQTabWidget.WaveformProcessingQTabWidget.WaveformTimingQWidget
        try:
            self.PhysicalExpansionQWidget = PhysicalExpansionQWidget(self)
            self.addTab(self.PhysicalExpansionQWidget, self.PhysicalExpansionQWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.MotionQTabWidget = MotionQWidget(self)
            self.addTab(self.MotionQTabWidget, self.MotionQTabWidget.settings_key)
        except Exception as ex:
            print(ex)
        try:
            self.TOFResultQTabWidget = TOFResultQTabWidget(self)
            self.addTab(self.TOFResultQTabWidget, self.TOFResultQTabWidget.settings_key)
        except Exception as ex:
            print(ex)

    def refresh(self):
        self.changed.emit()

    def get_explosion_time(self, width=5.0, quart=1):
        approximation_data = self.XXRapidTOFVelocityQTabWidget.get_velocity_dict()
        approximation_data_quart = approximation_data[f'Quart_{quart}']
        index = np.max(np.where(approximation_data_quart['width'] < width))
        t_exp = approximation_data_quart['onset_time'][index]
        return t_exp
        pass

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)
        try:
            self.PhysicalExpansionQWidget.save_report()
        except Exception as ex:
            print(f'PhysicalExpansionQWidget.save_report {ex}')
        try:
            self.MotionQTabWidget.save_report()
        except Exception as ex:
            print(f'MotionQTabWidget.save_report {ex}')

        try:
            self.TOFResultQTabWidget.save_report()
        except Exception as ex:
            print(f'XXRapidTOFVelocityQTabWidget.save_report {ex}')

    def save_origin_pro(self, op):
        try:
            self.PhysicalExpansionQWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        try:
            self.MotionQTabWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
        try:
            self.TOFResultQTabWidget.save_origin_pro(op)
        except Exception as ex:
            print(ex)
