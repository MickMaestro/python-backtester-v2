"""Application main window: tabbed shell hosting each feature area."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QTabWidget

from backtester import __version__
from backtester.ui.data_tab import DataTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Python Backtester {__version__}")
        self.resize(1200, 800)

        self.data_tab = DataTab()

        tabs = QTabWidget()
        tabs.addTab(self.data_tab, "Data Manager")
        tabs.addTab(_placeholder("Backtest setup arrives in Phase 2."), "Backtest")
        tabs.addTab(_placeholder("Chart and replay arrive in Phases 3-4."), "Chart")
        tabs.addTab(_placeholder("Results and statistics arrive in Phase 5."), "Results")
        self.setCentralWidget(tabs)

        self.statusBar().showMessage("Ready")

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        self.data_tab.shutdown()
        super().closeEvent(event)


def _placeholder(text: str) -> QLabel:
    label = QLabel(text)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("color: gray; font-size: 14px;")
    return label
