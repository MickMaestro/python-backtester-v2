"""Entry point: python app.py"""

import sys

from PySide6.QtWidgets import QApplication

from backtester.ui.main_window import MainWindow
from backtester.ui.theme import apply_theme, load_theme


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("Python Backtester")
    apply_theme(app, load_theme())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
