from .TOFResultsQWidget import *
from SettingsQWidgets.ChildQTabWidget import *


class TOFResultQTabWidget(ChildQTabWidget):
    def __init__(self, parent):
        super().__init__(parent, 'Result')
        self.report_path = f'{self.parent.report_path}/{self.settings_key}'
        self.MotionQTabWidget = self.parent.MotionQTabWidget
        self.MotionQTabWidget.changed.connect(self.refresh)
        self.motion_approximated_dict = self.MotionQTabWidget.motion_approximated_dict
        self.velocity_dict = self.get_velocity_dict()
        self.velocity_smoothed_dict = dict()
        self.TOFResultsQWidgetDict = dict()
        for my_key, my_df in self.velocity_dict.items():
            self.current_key = my_key
            self.current_df = my_df
            try:
                self.TOFResultsQWidgetDict[my_key] = TOFResultsQWidget(self)
                self.addTab(self.TOFResultsQWidgetDict[my_key], my_key)
            except Exception as ex:
                print(f'XXRapidTOFVelocityQWidgetDict[{my_key}] {ex}')

    def refresh(self):
        self.motion_approximated_dict = self.MotionQTabWidget.motion_approximated_dict
        self.velocity_dict = self.get_velocity_dict()
        for my_key, my_df in self.velocity_dict.items():
            self.current_key = my_key
            self.current_df = my_df
            try:
                self.TOFResultsQWidgetDict[my_key].refresh()
            except Exception as ex:
                print(f'XXRapidTOFVelocityQWidgetDict[{my_key}] {ex}')
        self.changed.emit()

    def on_graph_changed(self):
        self.changed.emit()

    def get_velocity_dict(self):
        velocity_dict = dict()
        for my_key, my_quart in self.motion_approximated_dict.items():
            velocity_list = []
            velocity_error_list = []
            onset_list = []
            onset_error_list = []
            x_list = []
            cross_section_list = []
            for motion_data in my_quart:
                x_list.append(motion_data['x'])
                cross_section_list.append(motion_data['width'])
                velocity_list.append(motion_data['velocity'] * 1e3)
                velocity_error_list.append(motion_data['velocity_error'] * 1e3)
                onset_list.append(motion_data['onset_time'])
                onset_error_list.append(motion_data['onset_time_error'])
            velocity_dict[my_key] = pd.DataFrame({
                'x': x_list,
                'width': cross_section_list,
                'velocity': velocity_list,
                'velocity_error': velocity_error_list,
                'onset_time': onset_list,
                'onset_time_error': onset_error_list,
            })
        return velocity_dict

    def save_report(self):
        os.makedirs(self.report_path, exist_ok=True)

        for graphics in self.TOFResultsQWidgetDict.values():
            try:
                graphics.save_report()
            except Exception as ex:
                print(ex)

    def save_origin_pro(self, op):
        name_workbook = self.settings_key
        workbook = op.new_book(lname=name_workbook)
        for my_key, my_df in self.velocity_dict.items():
            sheet_name = my_key
            sheet = workbook.add_sheet(name=sheet_name)
            sheet.from_df(my_df)
            graph = op.new_graph(template='3Ys_Y-Y-Y', lname=f'{name_workbook}_{sheet_name}')
            layer_onset_time = graph[0]
            layer_velocity = graph[1]
            plot_onset_time = graph[0].add_plot(sheet, colx=1, coly=4, colyerr=5)
            plot_velocity = layer_velocity.add_plot(sheet, colx=1, coly=2, colyerr=3)

            layer_onset_time.rescale()
            layer_velocity.rescale()
