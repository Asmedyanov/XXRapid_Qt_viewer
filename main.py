import sys
import qdarktheme
import matplotlib.pyplot as plt
plt.style.use('dark_background')

from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QAction, QFileDialog, QShortcut

from Main_Window import Main_window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = Main_window()
    window.show()
    sys.exit(app.exec_())
