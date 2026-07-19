"""Application main window: tabbed shell hosting each feature area."""

from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QTabWidget

from backtester import __version__
from backtester.data.store import DataStore
from backtester.ui.backtest_tab import BacktestTab
from backtester.ui.chart_tab import ChartTab
from backtester.ui.data_tab import DataTab
from backtester.ui.results_tab import ResultsTab
from backtester.ui.settings import app_settings


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"Python Backtester {__version__}")
        self.resize(1200, 800)

        store = DataStore()
        self.data_tab = DataTab(store)
        self.chart_tab = ChartTab(store)
        self.backtest_tab = BacktestTab(store)
        self.results_tab = ResultsTab()
        self.data_tab.datasets_changed.connect(self.chart_tab.refresh_datasets)
        self.data_tab.datasets_changed.connect(self.backtest_tab.refresh_datasets)
        self.backtest_tab.run_completed.connect(self._on_run_completed)
        self.results_tab.trade_selected.connect(self._on_trade_selected)

        self.tabs = QTabWidget()
        self.tabs.addTab(self.data_tab, "Data Manager")
        self.tabs.addTab(self.backtest_tab, "Backtest")
        self.tabs.addTab(self.chart_tab, "Chart")
        self.tabs.addTab(self.results_tab, "Results")
        self.setCentralWidget(self.tabs)

        self.statusBar().showMessage("Ready")

        geometry = app_settings().value("window/geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)

    def _on_run_completed(self, result, title: str, switch: bool) -> None:
        self.results_tab.show_result(result, title)
        if switch:
            self.tabs.setCurrentWidget(self.results_tab)
        self.statusBar().showMessage(
            f"Run finished: {result.stats['trades']} trades, "
            f"net {result.stats['net_profit']:+,.2f}"
        )

    def _on_trade_selected(self, trade) -> None:
        self.tabs.setCurrentWidget(self.backtest_tab)
        self.backtest_tab.focus_trade(trade)

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        app_settings().setValue("window/geometry", self.saveGeometry())
        self.backtest_tab.shutdown()
        self.data_tab.shutdown()
        super().closeEvent(event)
