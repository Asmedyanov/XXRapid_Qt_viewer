import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QFileDialog, QMessageBox
from MPL_tab import MPL_tab
from PyQt5.QtGui import QKeySequence
import os
import pandas as pd
from rtv_reader import *
from WaveformOriginalQWidget import *
from Single_camera_tab import Single_camera_tab
from Eight_frames_tab import Eight_frames
from Four_overlapped_frames_tab import Four_overlapped_frames
from Expansion_widget import Expansion_widget
import numpy as np
from Fronting_tab import Fronting
from Histogram_tab import Histogram_tab
from scipy import ndimage
from dict2xml import dict2xml
import xmltodict
from WaveformProcessingWidget import *
from TOF_tab import TOF_tab
from Action_integral_tab import Action_integral_tab
from J_comsol_widget import J_comsol_widget
from ExperimentQWidget import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XXRapid_Qt_viewer")
        # self.setGeometry(100, 100, 800, 600)
        self.setDocumentMode(True)

        # Create a tab widget
        self.tab_widget = QTabWidget(self)
        self.DefaultExperiment = ExperimentQWidget()
        self.ExperimentQWidgetDict = dict()
        self.tab_widget.addTab(self.DefaultExperiment, 'Default')

        '''self.Waveform_tab = WaveformOriginalQWidget()
        tab_widget.addTab(self.Waveform_tab, "Waveform original")
        self.Waveform_processing_tab = WaveformProcessingWidget()
        tab_widget.addTab(self.Waveform_processing_tab, "Waveform processing")
        self.Waveform_processing_tab.changed.connect(self.On_waveform_processing_changed)
        self.Single_camera_tab = Single_camera_tab()
        tab_widget.addTab(self.Single_camera_tab, "Single camera")'''

        '''self.Eight_frames_tab = Eight_frames()
        tab_widget.addTab(self.Eight_frames_tab, "8 frames")'''
        '''self.Four_overlapped_frames_tab = Four_overlapped_frames()
        self.Four_overlapped_frames_tab.changed.connect(self.On_overlapped_changed)
        tab_widget.addTab(self.Four_overlapped_frames_tab, "4 overlapped frames")'''

        '''self.Fronting_tab = Fronting()
        self.Fronting_tab.changed.connect(self.On_fronting_changed)
        tab_widget.addTab(self.Fronting_tab, "Fronting")'''

        '''self.Expansion_widget = Expansion_widget()
        self.Expansion_widget.changed.connect(self.On_Expansion_widget_changed)
        self.Additional_window = QMainWindow()
        self.Additional_window.setCentralWidget(self.Expansion_widget)'''

        '''self.TOF_tab = TOF_tab()
        self.TOF_tab.changed.connect(self.On_TOF_tab_changed)
        tab_widget.addTab(self.TOF_tab, "TOF")'''

        '''self.Action_integral_tab = Action_integral_tab()
        self.Action_integral_tab.changed.connect(self.On_Action_integral_tab_changed)
        tab_widget.addTab(self.Action_integral_tab, 'Action integral')'''

        '''self.J_comsol_widget = J_comsol_widget()
        self.J_comsol_widget.changed.connect(self.On_J_comsol_widget_changed)
        tab_widget.addTab(self.J_comsol_widget, 'J_comsol')'''

        # Set the tab widget as the central widget
        self.setCentralWidget(self.tab_widget)

        # Create a menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        # Add "Open Folder" action to the menu
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder_dialog)
        open_folder_action.setShortcut(QKeySequence("Ctrl+O"))  # Set the shortcut
        file_menu.addAction(open_folder_action)

        window_menu = menu_bar.addMenu("Window")
        expansion_action = QAction("Expansion window", self)
        expansion_action.triggered.connect(self.On_expansion_window)
        expansion_action.setShortcut(QKeySequence("Ctrl+E"))
        window_menu.addAction(expansion_action)

        self.main_settings = dict()
        # self.init_plots()

    def On_J_comsol_widget_changed(self):
        pass

    def On_TOF_tab_changed(self):
        pass
        '''self.Action_integral_tab.set_data(self.TOF_tab.Movement_widget.approximation_dict,
                                          self.Waveform_processing_tab.Waveform_timing_tab.df_current,
                                          {
                                              'Waist': self.info_file_df['Value']['Waist'],
                                              'Thickness': self.info_file_df['Value']['Thickness'],
                                              'Length': self.info_file_df['Value']['Length'],
                                              'Width': self.info_file_df['Value']['Width'],

                                          },
                                          self.J_comsol_widget.ratio_array,
                                          self.J_comsol_widget.time_array,
                                          self.J_comsol_widget.width_array)'''

    def On_Action_integral_tab_changed(self):
        pass

    def On_Expansion_widget_changed(self):
        pass
        '''self.TOF_tab.set_data(self.Expansion_widget.expansion_by_cross_section_dict, self.shutter_times,
                              self.Expansion_widget.dx)'''

    def On_overlapped_changed(self):
        self.Overlapped_image = self.Four_overlapped_frames_tab.Overlapped_image

    def On_waveform_processing_changed(self):
        self.shutter_times = self.Waveform_processing_tab.shutter_times

    def On_expansion_window(self):
        self.Additional_window.show()

    def closeEvent(self, event):
        self.DefaultExperiment.SaveSettings()
        for experiment in self.ExperimentQWidgetDict.values():
            experiment.SaveSettings()
        pass
        '''self.Additional_window.close()
        qm = QMessageBox.question(self, 'Save update', 'Save update?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if qm == QMessageBox.No:
            return
        try:
            fronting_file = open('Fronting.xml', 'w')
            fronting_file.write(dict2xml({'Camera data': self.Fronting_tab.Frame_data_dict}))
            fronting_file.close()
        except Exception as ex:
            print(ex)'''

    def On_fronting_changed(self):
        self.udate_expantion()

    def init_plots(self):
        os.chdir('./Default_shot')
        self.setWindowTitle("XXRapid_Qt_viewer Default_shot_57")

        self.update()

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder",
                                                       os.path.expanduser("~"))
        if folder_path:
            print(f"Selected folder: {folder_path}")
        else:
            return

        key = folder_path.split('/')[-1]
        self.ExperimentQWidgetDict[key] = ExperimentQWidget(folder_path)
        self.tab_widget.addTab(self.ExperimentQWidgetDict[key], key)

    def update(self):
        self.folder_list = os.listdir()
        print(f'Folder contains files\n{self.folder_list}')
        self.update_info()
        self.update_waveform()
        self.update_waveform_processing()
        '''self.J_comsol_widget.set_data()

        self.update_before()
        self.update_shot()
        self.update_single_camera()
        # self.update_histogram()
        # self.update_black()
        # self.update_plots()
        self.update_overlap()
        self.update_fronting()
        self.Additional_window.show()
        self.udate_expantion()
        self.TOF_tab.set_data(self.Expansion_widget.expansion_by_cross_section_dict, self.shutter_times,
                              self.Expansion_widget.dx)'''

        '''def cross_section(z):
            """
            The function to calculate the foil cross-section in direction of the current z
            :param z:
            distance from the butterfly waist in direction of current in mm
            :return:
            cross-section of the foil in square mm
            """
            s = 0.5 * self.info_file_df['Value']['Waist'] + (
                    self.info_file_df['Value']['Width'] - self.info_file_df['Value']['Waist']) * z / \
                self.info_file_df['Value']['Length']
            return 2 * s# * self.info_file_df['Value']['Thickness']

        for my_key, df in self.TOF_tab.Movement_widget.approximation_dict.items():
            df['w(x)'] = cross_section(df['x'] * 1e3)
            df.to_csv(f'SW_onset_{my_key}.csv')
        self.Action_integral_tab.set_data(self.TOF_tab.Movement_widget.approximation_dict,
                                          self.Waveform_processing_tab.Waveform_timing_tab.df_current,
                                          {
                                              'Waist': self.info_file_df['Value']['Waist'],
                                              'Thickness': self.info_file_df['Value']['Thickness'],
                                              'Length': self.info_file_df['Value']['Length'],
                                              'Width': self.info_file_df['Value']['Width'],

                                          },
                                          self.J_comsol_widget.finit_list,
                                          self.J_comsol_widget.possible_width,
                                          )'''

    def update_single_camera(self):
        self.Single_camera_tab.set_data(self.before_image_array, self.shot_image_array)

    def update_waveform_processing(self):
        self.Waveform_processing_tab.set_data(self.Waveform_tab.ChannelDFDict, self.info_file_df)

    def udate_expantion(self):
        try:
            self.Expansion_widget.set_data(self.Fronting_tab.Frame_data_dict, self.info_file_df['Value']['dx'])
        except Exception as ex:
            print(ex)

    def update_histogram(self):
        self.Histogram_tab.set_data(self.before_image_array, self.shot_image_array)

    def update_fronting(self):
        try:
            fronting_file = open('fronting.xml', 'r')
            fronting_string = fronting_file.read()
            fronting_dict = xmltodict.parse(fronting_string)['Camera_data']

            self.Fronting_tab.set_data(self.Overlapped_image, self.info_file_df['Value']['dx'], base_dict=fronting_dict)
        except Exception as ex:
            print(ex)
            self.Fronting_tab.set_data(self.Overlapped_image, self.info_file_df['Value']['dx'])

    def update_overlap(self):
        self.Four_overlapped_frames_tab.set_data(self.before_image_array, self.shot_image_array,
                                                 self.info_file_df['Value']['dx'])
        try:

            if self.info_file_df['Value']['Transverse'] == 1:
                self.Four_overlapped_frames_tab.transverse()
        except:
            pass

    def update_before(self):
        before_files_list = [name for name in self.folder_list if
                             name.startswith('before') and name.endswith('rtv')]
        # print(f'Folder contains before files\n{before_files_list}\nI took the last one')
        self.before_file_name = before_files_list[-1]
        self.before_image_array = open_rtv(self.before_file_name)

    def update_black(self):
        black_files_list = [name for name in self.folder_list if
                            name.startswith('black') and name.endswith('rtv')]
        # print(f'Folder contains before files\n{black_files_list}\nI took the last one')
        self.black_file_name = black_files_list[-1]
        self.black_image_array = open_rtv(self.black_file_name)

    def update_shot(self):
        shot_files_list = [name for name in self.folder_list if
                           name.startswith('shot') and name.endswith('rtv')]
        # print(f'Folder contains shot files\n{shot_files_list}\nI took the last one')
        self.shot_file_name = shot_files_list[-1]
        self.shot_image_array = open_rtv(self.shot_file_name)

    def update_plots(self):
        for i in range(4):
            # self.tab_dict[f'Camera {i + 1}'].ax.clear()
            self.Single_camera_tab_dict[f'Camera {i + 1}'].set_data(self.before_image_array[i],
                                                                    self.shot_image_array[i])
        self.Eight_frames_tab.set_data(self.before_image_array, self.shot_image_array)
        # self.tab_dict["Raw comparison"].compare_2_image_arrays(self.before_image_array, self.shot_image_array)
        '''self.tab_dict["3 camera overlapped"].overlap_3_camera(self.before_image_array,
                                                              self.shot_image_array,
                                                              self.info_file_df['Value']['dx'])'''

    def update_waveform(self):
        waveform_files_list = [name for name in self.folder_list if
                               name.startswith('shot') and name.endswith('csv')]
        # print(f'Folder contains waveform files\n{waveform_files_list}\nI took the last one')
        self.waveform_file_name = waveform_files_list[-1]
        waveform_df = pd.read_csv(self.waveform_file_name)
        self.Waveform_tab.set_data(waveform_df)

    def update_info(self):
        info_files_list = [name for name in self.folder_list if name.startswith('info')]
        # print(f'Folder contains info files\n{info_files_list}\nI took the last one')
        self.info_file_name = info_files_list[-1]
        data = pd.read_excel(self.info_file_name)
        data = data.set_index('Parameter')
        self.info_file_df = data
