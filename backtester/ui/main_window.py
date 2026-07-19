"""Application main window: tabbed shell hosting each feature area."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QTabWidget

from backtester import __version__
from backtester.data.store import DataStore
from backtester.ui.chart_tab import ChartTab
from backtester.ui.data_tab import DataTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Python Backtester {__version__}")
        self.resize(1200, 800)

        store = DataStore()
        self.data_tab = DataTab(store)
        self.chart_tab = ChartTab(store)
        self.data_tab.datasets_changed.connect(self.chart_tab.refresh_datasets)

        tabs = QTabWidget()
        tabs.addTab(self.data_tab, "Data Manager")
        tabs.addTab(
            _placeholder(
                "Backtest setup GUI arrives with the replay (Phases 4-5).\n"
                "Until then, run backtests with:  python run_backtest.py SYMBOL TF"
            ),
            "Backtest",
        )
        tabs.addTab(self.chart_tab, "Chart")
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
