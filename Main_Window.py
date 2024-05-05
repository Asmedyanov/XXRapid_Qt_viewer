import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QFileDialog
from MPL_tab import MPL_tab
from PyQt5.QtGui import QKeySequence
import os
import pandas as pd
from rtv_reader import open_rtv
from Waveform_tab import Waveform_tab
from Single_camera_tab import Single_camera
from Eight_frames_tab import Eight_frames
from Four_overlapped_frames_tab import Four_overlapped_frames
import numpy as np
from Fronting_tab import Fronting
from Histogram_tab import Histogram_tab
from scipy import ndimage


class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XXRapid_Qt_viewer")
        # self.setGeometry(100, 100, 800, 600)

        # Create a tab widget
        tab_widget = QTabWidget(self)

        # Create a dictionary of MPL_tab instances
        tab_titles = ["3 camera overlapped"]
        self.tab_dict = {title: MPL_tab(title) for title in tab_titles}

        self.Waveform_tab = Waveform_tab()
        tab_widget.addTab(self.Waveform_tab, "Waveform original")

        self.Single_camera_tab_dict = dict()
        for i in range(4):
            self.Single_camera_tab_dict[f'Camera {i + 1}'] = Single_camera()
            tab_widget.addTab(self.Single_camera_tab_dict[f'Camera {i + 1}'], f'Camera {i + 1}')

        self.Eight_frames_tab = Eight_frames()

        tab_widget.addTab(self.Eight_frames_tab, "8 frames")
        self.Four_overlapped_frames_tab = Four_overlapped_frames()
        tab_widget.addTab(self.Four_overlapped_frames_tab, "4 overlapped frames")

        self.Fronting_tab = Fronting()
        self.Fronting_tab.fronting_changed.connect(self.On_fronting_changed)
        tab_widget.addTab(self.Fronting_tab, "Fronting")
        self.Histogram_tab = Histogram_tab()
        tab_widget.addTab(self.Histogram_tab, "Histogram")

        # Add the MPL_tab instances to the tab widget
        for title, tab in self.tab_dict.items():
            tab_widget.addTab(tab, title)

        # Set the tab widget as the central widget
        self.setCentralWidget(tab_widget)

        # Create a menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        # Add "Open Folder" action to the menu
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder_dialog)
        open_folder_action.setShortcut(QKeySequence("Ctrl+O"))  # Set the shortcut
        file_menu.addAction(open_folder_action)
        self.main_settings = dict()
        self.init_plots()

    def closeEvent(self, event):
        try:
            fronting_file = open('Fronting.txt', 'w')
            fronting_file.write(str(self.Fronting_tab.Frame_data_dict))
            fronting_file.close()
        except Exception as ex:
            print(ex)

    def On_fronting_changed(self):
        pass


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
        os.chdir(folder_path)

        self.setWindowTitle(f"XXRapid_Qt_viewer {folder_path.split('/')[-1]}")
        self.update()

    def update(self):
        self.folder_list = os.listdir()
        print(f'Folder contains files\n{self.folder_list}')
        self.update_info()
        self.update_waveform()

        self.update_before()
        self.update_shot()
        self.update_histogram()
        # self.update_black()
        self.update_plots()
        self.update_overlap()
        self.update_fronting()

    def update_histogram(self):
        self.Histogram_tab.set_data(self.before_image_array, self.shot_image_array)

    def update_fronting(self):
        self.Fronting_tab.set_data(self.Overlapped_image, self.info_file_df['Value']['dx'])

    def update_overlap(self):
        overlapped = np.where(self.shot_image_array > self.before_image_array, self.before_image_array,
                              self.shot_image_array)
        mask_list = []
        for i in range(4):
            mask = np.where(self.before_image_array[i] <= self.before_image_array[i].mean(), 0, 1)
            # mask = ndimage.uniform_filter(mask, size=2)
            # mask = ndimage.maximum_filter(mask, size=10)
            # mask = ndimage.minimum_filter(mask, size=2)

            mask_list.append(mask)
        mask = np.array(mask_list)

        print(f'before_array_min = {self.before_image_array.min()}')
        print(f'before_array_max = {self.before_image_array.max()}')
        print(f'before_array_mean = {self.before_image_array.mean()}')
        overlapped = np.where(self.before_image_array > 1, overlapped / self.before_image_array, 1) * mask
        self.Overlapped_image = overlapped
        try:

            if self.info_file_df['Value']['Transverse'] == 1:
                transpose_list = []
                for i in range(4):
                    transpose_list.append(self.Overlapped_image[i].transpose())
                self.Overlapped_image = np.array(transpose_list)
        except:
            pass
        self.Four_overlapped_frames_tab.set_data(self.Overlapped_image, self.info_file_df['Value']['dx'])

    def update_before(self):
        before_files_list = [name for name in self.folder_list if
                             name.startswith('before') and name.endswith('rtv')]
        print(f'Folder contains before files\n{before_files_list}\nI took the last one')
        self.before_file_name = before_files_list[-1]
        self.before_image_array = open_rtv(self.before_file_name)

    def update_black(self):
        black_files_list = [name for name in self.folder_list if
                            name.startswith('black') and name.endswith('rtv')]
        print(f'Folder contains before files\n{black_files_list}\nI took the last one')
        self.black_file_name = black_files_list[-1]
        self.black_image_array = open_rtv(self.black_file_name)

    def update_shot(self):
        shot_files_list = [name for name in self.folder_list if
                           name.startswith('shot') and name.endswith('rtv')]
        print(f'Folder contains shot files\n{shot_files_list}\nI took the last one')
        self.shot_file_name = shot_files_list[-1]
        self.shot_image_array = open_rtv(self.shot_file_name)

    def update_plots(self):
        for i in range(4):
            # self.tab_dict[f'Camera {i + 1}'].ax.clear()
            self.Single_camera_tab_dict[f'Camera {i + 1}'].set_data(self.before_image_array[i],
                                                                    self.shot_image_array[i])
        self.Eight_frames_tab.set_data(self.before_image_array, self.shot_image_array)
        # self.tab_dict["Raw comparison"].compare_2_image_arrays(self.before_image_array, self.shot_image_array)
        self.tab_dict["3 camera overlapped"].overlap_3_camera(self.before_image_array,
                                                              self.shot_image_array,
                                                              self.info_file_df['Value']['dx'])

    def update_waveform(self):
        waveform_files_list = [name for name in self.folder_list if
                               name.startswith('shot') and name.endswith('csv')]
        print(f'Folder contains waveform files\n{waveform_files_list}\nI took the last one')
        self.waveform_file_name = waveform_files_list[-1]
        waveform_df = pd.read_csv(self.waveform_file_name)
        self.Waveform_tab.set_data(waveform_df)

    def update_info(self):
        info_files_list = [name for name in self.folder_list if name.startswith('info')]
        print(f'Folder contains info files\n{info_files_list}\nI took the last one')
        self.info_file_name = info_files_list[-1]
        data = pd.read_excel(self.info_file_name)
        data = data.set_index('Parameter')
        self.info_file_df = data
