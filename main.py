import sys
import qdarktheme
from PyQt5.QtWidgets import QApplication

# from Main_Window import MainWindow
from XXRapid_Qt_viewer.Main_Window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
