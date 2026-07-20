"""Phase 6: intrabar precision, optimizer, strategy loader, optimizer tab."""

import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PROJECT_ROOT = Path(__file__).resolve().parents[1]

import pandas as pd
import pytest
from PySide6.QtWidgets import QApplication

from backtester.data.store import DataStore
from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.optimizer import build_grid, optimize, steps
from backtester.engine.orders import CloseReason
from backtester.strategy import loader

from tests.engine_utils import Scripted, make_df, make_wave


# ------------------------------------------------------------- intrabar

def test_intrabar_resolves_tp_before_sl():
    # One H1 bar whose range covers both SL and TP. Pessimistic single-bar
    # resolution says SL; the M5 sub-bars show price went UP first.
    h1 = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1000, 1.1200, 1.0900, 1.1005),  # covers SL 1.0950 and TP 1.1100
            (1.1000, 1.1010, 1.0990, 1.1005),
        ]
    )
    sub_bars = [
        (1.1000, 1.1120, 1.0995, 1.1100),  # rallies through TP first
        (1.1100, 1.1200, 1.0900, 1.1005),  # then collapses through SL
    ]
    m5 = make_df(sub_bars, start="2024-01-01 01:00", freq="5min")

    script = {0: [lambda s: s.buy(lots=1.0, sl=1.0950, tp=1.1100)]}

    pessimistic = Backtester(h1, Scripted(script)).run_all()
    assert pessimistic.trades[0].reason is CloseReason.STOP_LOSS

    accurate = Backtester(h1, Scripted(script), intrabar_df=m5).run_all()
    assert accurate.trades[0].reason is CloseReason.TAKE_PROFIT
    assert accurate.trades[0].exit_price == pytest.approx(1.1100)


def test_intrabar_falls_back_outside_coverage():
    h1 = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1000, 1.1005, 1.0940, 1.0990),  # SL 1.0950 hit; no sub data here
        ]
    )
    # Sub data exists only for a much later period.
    m5 = make_df([(1.0990, 1.1000, 1.0980, 1.0990)] * 4, start="2024-06-01", freq="5min")
    result = Backtester(
        h1, Scripted({0: [lambda s: s.buy(lots=1.0, sl=1.0950)]}), intrabar_df=m5
    ).run_all()
    trade = result.trades[0]
    assert trade.reason is CloseReason.STOP_LOSS
    assert trade.exit_price == pytest.approx(1.0950)


# ------------------------------------------------------------ optimizer

def test_build_grid_and_steps():
    assert steps(5, 15, 5, as_int=True) == [5, 10, 15]
    assert steps(0.5, 1.0, 0.25) == [0.5, 0.75, 1.0]
    grid = build_grid({"fast": [5, 10], "slow": [20, 30, 40]})
    assert len(grid) == 6
    assert {"fast": 10, "slow": 40} in grid


def test_optimize_serial_ranks_and_captures_errors():
    df = make_wave(200)
    grid = build_grid({"fast": [5, 10], "slow": [20, 2]})  # slow=2 < fast → runs, fine
    grid.append({"fast": 10, "slow": 20, "bogus": 1})      # unknown param → error
    results = optimize(df, ("builtin", "ma_cross"), grid, BacktestConfig(), workers=0)
    assert len(results) == 5
    errors = [r for r in results if r.error]
    assert len(errors) == 1 and "bogus" in errors[0].error
    ok = [r for r in results if not r.error]
    assert all("net_profit" in r.stats for r in ok)


def test_optimize_should_stop():
    df = make_wave(150)
    grid = build_grid({"fast": [3, 4, 5, 6, 7, 8]})
    calls = []
    results = optimize(
        df, ("builtin", "ma_cross"), grid, BacktestConfig(), workers=0,
        progress=lambda d, t: calls.append(d),
        should_stop=lambda: len(calls) >= 2,
    )
    assert len(results) == 2


def test_optimize_multiprocess_two_workers():
    # Real spawn-based multiprocessing must run in its own interpreter: mixing
    # multiprocessing 'spawn' with Qt (loaded by the GUI tests) in the shared
    # pytest process crashes later Qt tests on Windows. Running the pool in a
    # clean subprocess exercises the genuine ProcessPoolExecutor path safely.
    code = textwrap.dedent(
        """
        from backtester.engine.backtester import BacktestConfig
        from backtester.engine.optimizer import build_grid, optimize
        from tests.engine_utils import make_wave

        df = make_wave(150)
        grid = build_grid({"fast": [5, 8], "slow": [20, 30]})
        results = optimize(
            df, ("builtin", "ma_cross"), grid, BacktestConfig(), workers=2
        )
        assert len(results) == 4, len(results)
        assert not [r for r in results if r.error]
        print("MP_OK")
        """
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert "MP_OK" in proc.stdout, f"stdout={proc.stdout!r}\nstderr={proc.stderr!r}"


# --------------------------------------------------------------- loader

STRATEGY_SOURCE = textwrap.dedent(
    """
    from backtester.strategy.base import Strategy

    class MyStrat(Strategy):
        params = {"n": %d}

        def on_bar(self, bar):
            pass
    """
)


def test_loader_discovers_and_hot_reloads(tmp_path):
    file = tmp_path / "custom.py"
    file.write_text(STRATEGY_SOURCE % 10, encoding="utf-8")

    registry, errors = loader.discover(tmp_path)
    assert errors == []
    assert "ma_cross" in registry               # built-ins present
    cls, spec = registry["custom.MyStrat"]
    assert cls.params == {"n": 10}
    assert spec == ("file", str(file), "MyStrat")

    file.write_text(STRATEGY_SOURCE % 99, encoding="utf-8")  # edit the file
    registry, _ = loader.discover(tmp_path)
    assert registry["custom.MyStrat"][0].params == {"n": 99}


def test_loader_reports_broken_files(tmp_path):
    (tmp_path / "broken.py").write_text("def x(:\n", encoding="utf-8")
    registry, errors = loader.discover(tmp_path)
    assert len(errors) == 1 and "broken.py" in errors[0]
    assert "ma_cross" in registry               # built-ins unaffected


def test_bundled_trailing_strategy_runs():
    # Guards the price-series/method split: TrailingTrend uses both
    # self.closes (array) and self.close(position) (method), which used to
    # collide. Also exercises the trailing modify() path end to end.
    registry, errors = loader.discover()  # scans the real strategies/ folder
    assert not errors, errors
    assert "trailing_trend.TrailingTrend" in registry
    cls = registry["trailing_trend.TrailingTrend"][0]
    result = Backtester(make_wave(400, period=60), cls(lots=1.0)).run_all()
    assert result.stats["trades"] > 0
    assert result.final_balance == pytest.approx(
        result.initial_balance + sum(t.net for t in result.trades)
    )


def test_optimizer_uses_file_strategy_spec(tmp_path):
    file = tmp_path / "custom.py"
    file.write_text(STRATEGY_SOURCE % 10, encoding="utf-8")
    results = optimize(
        make_wave(80), ("file", str(file), "MyStrat"),
        [{"n": 1}, {"n": 2}], BacktestConfig(), workers=0,
    )
    assert all(not r.error for r in results)


# --------------------------------------------------------- optimizer tab

@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


def test_optimizer_tab_end_to_end(qapp, tmp_path):
    from backtester.ui.optimizer_tab import OptimizerTab

    store = DataStore(tmp_path)
    store.save_bars(
        "TEST", "H1", make_wave(200),
        spec={"point": 1e-5, "digits": 5, "contract_size": 100_000.0},
    )
    tab = OptimizerTab(store)
    tab.strategy_combo.setCurrentText("ma_cross")
    tab.workers_spin.setValue(0)  # in-process for the test

    fast_row = next(r for r in tab._param_rows if r.name == "fast")
    fast_row.check.setChecked(True)
    fast_row.from_spin.setValue(5)
    fast_row.to_spin.setValue(10)
    fast_row.step_spin.setValue(5)

    chosen = []
    tab.params_chosen.connect(lambda name, params: chosen.append((name, params)))
    tab._run()
    deadline = time.time() + 20
    while tab._worker is not None and time.time() < deadline:
        qapp.processEvents()
        time.sleep(0.01)

    assert tab.table.rowCount() == 2            # fast = 5 and 10
    assert "results" in tab.status_label.text()

    tab._on_double_clicked(tab.table.item(0, 1))
    assert len(chosen) == 1
    name, params = chosen[0]
    assert name == "ma_cross" and params["fast"] in (5, 10)


def test_backtest_tab_lists_user_strategies_and_intrabar(qapp, tmp_path, monkeypatch):
    from PySide6.QtCore import QSettings

    monkeypatch.setattr(
        "backtester.ui.backtest_tab.app_settings",
        lambda: QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat),
    )
    from backtester.ui.backtest_tab import BacktestTab

    store = DataStore(tmp_path / "data")
    spec = {"point": 1e-5, "digits": 5, "contract_size": 100_000.0}
    store.save_bars("TEST", "H1", make_wave(100), spec=spec)
    store.save_bars("TEST", "M15", make_wave(400, period=200), spec=spec)

    tab = BacktestTab(store)
    names = [tab.strategy_combo.itemText(i) for i in range(tab.strategy_combo.count())]
    assert "ma_cross" in names
    assert "trailing_trend.TrailingTrend" in names  # from strategies/ folder

    tab.dataset_combo.setCurrentText("TEST_H1")
    intrabar = [
        tab.intrabar_combo.itemText(i) for i in range(tab.intrabar_combo.count())
    ]
    assert intrabar[0].startswith("Off")
    assert "TEST_M15" in intrabar               # finer TF of same symbol offered
