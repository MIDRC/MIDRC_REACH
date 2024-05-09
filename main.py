import sys
from typing import Optional
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSplashScreen, QWidget
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from jsdcontroller import JSDController
from jsdmodel import JSDTableModel
from jsdview import JsdWindow
from jsdconfig import JSDConfig


class SplashScreen(QSplashScreen):
    """
    Class: SplashScreen

    This class is a subclass of QSplashScreen and represents a splash screen for a GUI application.
    It provides a static method _create_pixmap() to create a pixmap with a centered splash screen message.
    The __init__() method initializes the object and sets the pixmap.
    """
    @staticmethod
    def _create_pixmap():
        """
        Function: _create_pixmap

        Create a pixmap with the splash screen message centered on it.

        Returns:
            QPixmap: The created QPixmap object.
        """
        SPLASH_WIDTH = 800
        SPLASH_HEIGHT = 600
        FONT_FAMILY = 'Arial'
        FONT_SIZE = 36
        SPLASH_SCREEN_MESSAGE = 'MIDRC Diversity Calculator\n' \
                                '\n' \
                                'Loading Excel files, please wait...'
        BACKGROUND_COLOR = QColor(Qt.white)

        pixmap = QPixmap(SPLASH_WIDTH, SPLASH_HEIGHT)
        font = QFont(FONT_FAMILY, pointSize=FONT_SIZE)
        with QPainter(pixmap) as painter:
            painter.setRenderHint(QPainter.Antialiasing)
            painter.fillRect(pixmap.rect(), BACKGROUND_COLOR)
            painter.setFont(font)
            painter.drawText(pixmap.rect(), Qt.AlignCenter, SPLASH_SCREEN_MESSAGE)
        return pixmap

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        Initialize the object.

        Args:
            parent: The parent widget.
        """
        super().__init__(parent)
        pixmap = self._create_pixmap()
        self.setPixmap(pixmap)


def launch_diversity_calculator():
    """
    Function: launch_diversity_calculator

    This function launches the diversity calculator application.
    * It checks if a QApplication instance already exists, and if not, creates one.
    * It then creates a SplashScreen object and displays it.
    * Next, it initializes a JSDConfig object and retrieves the data source list from the configuration.
    * It creates a JsdWindow object with the data source list and sets the JSDController with a JSDTableModel and the
    configuration.
    * Finally, it shows the JsdWindow, finishes the SplashScreen, and exits the application.

    Returns:
        None
    """
    q_app = QApplication.instance()
    if q_app is None:
        q_app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()
    q_app.processEvents()

    config = JSDConfig()
    data_source_list = config.data['data sources']
    w = JsdWindow(data_source_list)  # Note: We should have the controller populate this once the tablemodel is loaded
    w.jsd_controller = JSDController(w,
                                     JSDTableModel(data_source_list, config.data.get('custom age ranges', None)),
                                     config)
    w.show()

    splash.finish(w)
    sys.exit(q_app.exec())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    launch_diversity_calculator()

