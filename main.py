import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QAction, QFileDialog, QShortcut
from PyQt5.QtGui import QKeySequence
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class MPL_tab(QWidget):
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.layout = QVBoxLayout()

        # Create a Matplotlib figure and axis
        self.figure, self.ax = plt.subplots()
        self.ax.plot([0, 1, 2, 3, 4], [0, 1, 4, 9, 16])
        self.ax.set_title(self.title)
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")

        # Create a canvas to embed the Matplotlib plot
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(NavigationToolbar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        # Create a tab widget
        tab_widget = QTabWidget(self)

        # Add the MPL_tab to the tab widget
        tab_widget.addTab(MPL_tab("Waveform"), "Waveform")
        tab_widget.addTab(MPL_tab("Camera 1"), "Camera 1")
        tab_widget.addTab(MPL_tab("Camera 2"), "Camera 2")
        tab_widget.addTab(MPL_tab("Camera 3"), "Camera 3")
        tab_widget.addTab(MPL_tab("Camera 4"), "Camera 4")
        tab_widget.addTab(MPL_tab("Raw comparison"), "Raw comparison")
        tab_widget.addTab(MPL_tab("Overlapped comparison"), "Overlapped comparison")

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

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", os.path.expanduser("~"))
        if folder_path:
            print(f"Selected folder: {folder_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main_window()
    window.show()
    sys.exit(app.exec_())
