"""Offscreen tests for Phase 5: results tab, fast run, settings persistence."""

import os
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pandas as pd
import pytest
from PySide6.QtCore import QSettings, Qt
from PySide6.QtWidgets import QApplication

from backtester.data.store import DataStore
from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.orders import Trade
from backtester.strategy.examples import MaCross
from backtester.ui.backtest_tab import BacktestTab, FastRunWorker
from backtester.ui.results_tab import ResultsTab

from tests.engine_utils import make_wave


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture(scope="module")
def result():
    bt = Backtester(
        make_wave(300), MaCross(fast=5, slow=20), BacktestConfig()
    )
    return bt.run_all()


def test_results_tab_populates(qapp, result):
    tab = ResultsTab()
    tab.show_result(result, "TEST H1 — ma_cross")
    assert tab.table.rowCount() == len(result.trades)
    assert "Trades:" in tab.stats_label.text()
    assert "ma_cross" in tab.context_label.text()
    # Pips column filled because the result carries its config.
    assert tab.table.item(0, 8).text() != "-"


def test_trade_table_sorts_numerically(qapp, result):
    tab = ResultsTab()
    tab.show_result(result, "t")
    net_column = 9
    tab.table.sortItems(net_column, Qt.SortOrder.DescendingOrder)
    values = [
        tab.table.item(row, net_column).sort_value
        for row in range(tab.table.rowCount())
    ]
    assert values == sorted(values, reverse=True)


def test_double_click_emits_trade(qapp, result):
    tab = ResultsTab()
    tab.show_result(result, "t")
    captured = []
    tab.trade_selected.connect(captured.append)
    tab._on_double_clicked(tab.table.item(0, 3))
    assert len(captured) == 1
    assert isinstance(captured[0], Trade)


def test_exports(qapp, result, tmp_path):
    tab = ResultsTab()
    tab.show_result(result, "TEST EXPORT")
    csv_path = tmp_path / "trades.csv"
    tab.export_trades_csv(str(csv_path))
    frame = pd.read_csv(csv_path)
    assert len(frame) == len(result.trades)
    assert "net" in frame.columns

    summary_path = tmp_path / "summary.txt"
    tab.export_summary(str(summary_path))
    text = summary_path.read_text(encoding="utf-8")
    assert "TEST EXPORT" in text and "Profit factor" in text


def test_fast_worker_runs_synchronously(qapp):
    bt = Backtester(make_wave(200), MaCross(fast=5, slow=20))
    worker = FastRunWorker(bt)
    progresses, results = [], []
    worker.progress.connect(lambda d, t: progresses.append((d, t)))
    worker.finished_result.connect(results.append)
    worker.run()  # direct call: synchronous
    assert progresses[-1] == (200, 200)
    assert len(results) == 1
    assert results[0].config is not None


def make_store(tmp_path) -> DataStore:
    store = DataStore(tmp_path)
    store.save_bars(
        "TEST", "H1", make_wave(300),
        spec={"point": 1e-5, "digits": 5, "contract_size": 100_000.0},
    )
    return store


def use_ini_settings(monkeypatch, tmp_path):
    def factory():
        return QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat)

    monkeypatch.setattr("backtester.ui.backtest_tab.app_settings", factory)
    return factory


def test_backtest_tab_fast_run(qapp, tmp_path, monkeypatch):
    use_ini_settings(monkeypatch, tmp_path)
    tab = BacktestTab(make_store(tmp_path))
    completed = []
    tab.run_completed.connect(lambda r, t, s: completed.append((r, t, s)))

    tab._run_fast()
    deadline = time.time() + 15
    while tab.result is None and time.time() < deadline:
        qapp.processEvents()
        time.sleep(0.01)

    assert tab.result is not None, "fast run did not finish in time"
    assert len(completed) == 1
    _, title, switch = completed[0]
    assert switch is True and "ma_cross" in title
    assert tab.trade_layer.closed_count == len(tab.result.trades)
    assert len(tab._equity_x) == 300
    assert "Finished" in tab.progress_label.text()
    assert tab.fast_button.isEnabled()


def test_settings_roundtrip(qapp, tmp_path, monkeypatch):
    use_ini_settings(monkeypatch, tmp_path)
    store = make_store(tmp_path)

    tab = BacktestTab(store)
    tab.balance_spin.setValue(5_000)
    tab.commission_spin.setValue(7.5)
    tab.spread_data_check.setChecked(False)
    tab.spread_spin.setValue(25)
    tab._param_widgets["fast"].setValue(12)
    tab._save_settings()

    fresh = BacktestTab(store)
    assert fresh.balance_spin.value() == pytest.approx(5_000)
    assert fresh.commission_spin.value() == pytest.approx(7.5)
    assert fresh.spread_data_check.isChecked() is False
    assert fresh.spread_spin.value() == 25
    assert fresh._param_widgets["fast"].value() == 12
