import sys

# Third party imports
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject

# Local imports
from main_window import MainWindow


class BorbinSmash(QObject):
    def __init__(self):
        super().__init__()

        # Initialize Qt sys
        self.app = QApplication(sys.argv)
        self.app.setStyle("fusion")

        # Instance of GUI window
        self.main_window = MainWindow()


# Create instance of main control class
instance = BorbinSmash()

# Start by showing the main window
instance.main_window.show()

# Execute and close on end on program exit
sys.exit(instance.app.exec())
