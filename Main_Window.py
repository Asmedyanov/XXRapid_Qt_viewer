import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QFileDialog
from MPL_tab import MPL_tab
from PyQt5.QtGui import QKeySequence
import os
import pandas as pd
import numpy as np
from rtv_reader import open_rtv


class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XXRapid_Qt_viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create a tab widget
        tab_widget = QTabWidget(self)

        # Create a dictionary of MPL_tab instances
        tab_titles = ["Waveform", "Camera 1", "Camera 2", "Camera 3", "Camera 4", "Raw comparison",
                      "Overlapped comparison"]
        self.tab_dict = {title: MPL_tab(title) for title in tab_titles}

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

    def init_plots(self):
        self.waveform_plots_dict = dict()
        t = np.arange(0, 2.0 * np.pi, 0.1)
        x = np.cos(t)
        y = np.sin(t)
        self.tab_dict['Waveform'].ax.clear()
        self.tab_dict['Waveform'].ax.set(
            xlabel='t, sec',
            ylabel='u, V',
            title='Waveform original'
        )
        for i in range(4):
            self.waveform_plots_dict[f'channel_{i}'], = self.tab_dict['Waveform'].ax.plot(
                x * (i + 1),
                y * (i + 1),
                label=f'channel_{i}')
        self.tab_dict['Waveform'].ax.legend()

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder",
                                                       os.path.expanduser("~"))
        if folder_path:
            print(f"Selected folder: {folder_path}")
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
        self.update_plots()

    def update_before(self):
        self.before_files_list = [name for name in self.folder_list if
                                  name.startswith('before') and name.endswith('rtv')]
        print(f'Folder contains before files\n{self.before_files_list}\nI took the last one')
        self.before_file_name = self.before_files_list[-1]
        self.before_image_array = open_rtv(self.before_file_name)

    def update_shot(self):
        self.shot_files_list = [name for name in self.folder_list if
                                name.startswith('shot') and name.endswith('rtv')]
        print(f'Folder contains shot files\n{self.shot_files_list}\nI took the last one')
        self.shot_file_name = self.shot_files_list[-1]
        self.shot_image_array = open_rtv(self.shot_file_name)

    def update_plots(self):
        for my_key, my_plot in self.waveform_plots_dict.items():
            my_plot.set_data(
                self.waveform_dict[f'{my_key}_time'],
                self.waveform_dict[f'{my_key}'],
            )
        self.tab_dict['Waveform'].ax.relim()
        self.tab_dict['Waveform'].ax.autoscale_view()
        self.tab_dict['Waveform'].figure.canvas.draw()

        for i in range(4):
            # self.tab_dict[f'Camera {i + 1}'].ax.clear()
            self.tab_dict[f'Camera {i + 1}'].compare_2_image(self.before_image_array[i], self.shot_image_array[i], )
        self.tab_dict["Raw comparison"].compare_2_image_arrays(self.before_image_array, self.shot_image_array)

    def update_waveform(self):
        """
            the function read the waveform file *.csv:
            current,synchro:camera and maxwell, voltage divider
            :param Inductance:
            :param fname: file name
            :param Rogovski_ampl: coefficient to transform voltage from the Rogovski coil to Amper
            :param Rogovski_conv: the number of points to smooth the current
            :return:
            {
                'time': current_time,
                'current': current_amp,
                'peaks': peak_times
            }
            """
        self.waveform_files_list = [name for name in self.folder_list if
                                    name.startswith('shot') and name.endswith('csv')]
        print(f'Folder contains waveform files\n{self.waveform_files_list}\nI took the last one')
        self.waveform_file_name = self.waveform_files_list[-1]
        waveform_df = pd.read_csv(self.waveform_file_name)
        self.waveform_dict = dict()
        for i, my_key in enumerate(self.waveform_plots_dict.keys()):
            self.waveform_dict[my_key] = waveform_df.iloc[:, 1::2].iloc[:, i].values
            self.waveform_dict[f'{my_key}_time'] = waveform_df.iloc[:, ::2].iloc[:, i].values

    def update_info(self):
        self.info_files_list = [name for name in self.folder_list if name.startswith('info')]
        print(f'Folder contains info files\n{self.info_files_list}\nI took the last one')
        self.info_file_name = self.info_files_list[-1]
        data = pd.read_excel(self.info_file_name)
        data = data.set_index('Parameter')
        self.info_file_df = data
