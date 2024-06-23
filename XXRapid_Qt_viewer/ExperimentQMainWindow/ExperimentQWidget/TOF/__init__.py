from .TOFVelocityQTabWidget import *
from .MotionQWidget import *
from .PhysicalExpansionQWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class XXRapidTOFQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'TOF')
        self.XXRapidFrontingQWidget = self.parent.XXRapidFrontingQWidget

        self.WaveformTimingQWidget = self.parent.WaveformQTabWidget.WaveformProcessingQTabWidget.WaveformTimingQWidget
        self.WaveformTimingQWidget.changed.connect(self.refresh)
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

    def refresh(self):
        self.changed.emit()

        '''key = 'Physical_expansion'
        settings = dict()
        if key in settings_dict.keys():
            settings = settings_dict[key]
        try:
            self.XXRapidTOFPhysicalExpansionQTabWidget = XXRapidTOFPhysicalExpansionQWidget(timing_dict,
                                                                                            expansion_dict,
                                                                                            settings)
            self.addTab(self.XXRapidTOFPhysicalExpansionQTabWidget, key)
            self.XXRapidTOFPhysicalExpansionQTabWidget.changed.connect(self.on_XXRapidTOFPhysicalExpansionQTabWidget)
            self.SettingsDict[key] = self.XXRapidTOFPhysicalExpansionQTabWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidTOFPhysicalExpansionQTabWidget {ex}')

        key = 'Motion'
        try:
            settings = settings_dict[key]
        except:
            settings = dict()
        try:
            self.XXRapidTOFMotionQWidget = XXRapidTOFMotionQWidget(
                motion_dict=self.XXRapidTOFPhysicalExpansionQTabWidget.get_motion_dict(), settings_dict=settings)
            self.addTab(self.XXRapidTOFMotionQWidget, key)
            self.XXRapidTOFMotionQWidget.changed.connect(self.on_XXRapidTOFMotionQWidget)
            self.SettingsDict[key] = self.XXRapidTOFMotionQWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidTOFMotionQWidget {ex}')
        key = 'Velocity'
        try:
            settings = settings_dict[key]
        except:
            settings = dict()
        try:
            self.XXRapidTOFVelocityQTabWidget = XXRapidTOFVelocityQTabWidget(
                motion_approximated_dict=self.XXRapidTOFMotionQWidget.get_approximation(), settings_dict=settings)
            self.addTab(self.XXRapidTOFVelocityQTabWidget, key)
            # self.XXRapidTOFMotionQWidget.changed.connect(self.on_XXRapidTOFMotionQWidget)
            self.SettingsDict[key] = self.XXRapidTOFVelocityQTabWidget.SettingsDict
        except Exception as ex:
            print(f'XXRapidTOFVelocityQTabWidget {ex}')'''

    def get_explosion_time(self, width=5.0, quart=1):
        approximation_data = self.XXRapidTOFVelocityQTabWidget.get_velocity_dict()
        approximation_data_quart = approximation_data[f'Quart_{quart}']
        index = np.max(np.where(approximation_data_quart['width'] < width))
        t_exp = approximation_data_quart['onset_time'][index]
        return t_exp
        pass

    def on_XXRapidTOFPhysicalExpansionQTabWidget(self):
        try:
            self.XXRapidTOFMotionQWidget.set_data(self.XXRapidTOFPhysicalExpansionQTabWidget.get_motion_dict())
        except Exception as ex:
            print(f'self.XXRapidTOFPhysicalExpansionQTabWidget.set_data {ex}')
        # self.changed.emit()

    def set_data(self, timing_dict, expansion_dict):
        try:
            self.XXRapidTOFPhysicalExpansionQTabWidget.set_data(timing_dict, expansion_dict)
        except Exception as ex:
            print(f'self.XXRapidTOFPhysicalExpansionQTabWidget.set_data {ex}')

    def on_XXRapidTOFMotionQWidget(self):
        try:
            self.XXRapidTOFVelocityQTabWidget.set_data(self.XXRapidTOFMotionQWidget.motion_approximated_dict())
        except Exception as ex:
            print(f'self.XXRapidTOFPhysicalExpansionQTabWidget.set_data {ex}')
        self.changed.emit()

    def save_report(self, folder_name):
        if 'XXRapid_TOF' not in os.listdir(folder_name):
            os.makedirs(f'{folder_name}/XXRapid_TOF')
        try:
            self.XXRapidTOFPhysicalExpansionQTabWidget.save_report(f'{folder_name}/XXRapid_TOF')
        except Exception as ex:
            print(f'XXRapidTOFPhysicalExpansionQTabWidget.save_report {ex}')
        try:
            self.XXRapidTOFMotionQWidget.save_report(f'{folder_name}/XXRapid_TOF')
        except Exception as ex:
            print(f'XXRapidTOFMotionQWidget.save_report {ex}')

        try:
            self.XXRapidTOFVelocityQTabWidget.save_report(f'{folder_name}/XXRapid_TOF')
        except Exception as ex:
            print(f'XXRapidTOFVelocityQTabWidget.save_report {ex}')
