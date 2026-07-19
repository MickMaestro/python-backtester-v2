"""Offscreen tests for the replay: controller, trade layer, Backtest tab."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pyqtgraph as pg
import pytest
from PySide6.QtWidgets import QApplication

from backtester.data.store import DataStore
from backtester.engine.backtester import Backtester
from backtester.engine.events import (
    EquityEvent,
    PositionClosed,
    PositionModified,
    PositionOpened,
)
from backtester.engine.orders import CloseReason, Direction, Position, Trade
from backtester.strategy.examples import MaCross
from backtester.ui.backtest_tab import BacktestTab
from backtester.ui.chart.replay_controller import ReplayController
from backtester.ui.chart.trade_markers import TradeLayer

from tests.engine_utils import make_wave


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


def make_controller(n=120):
    bt = Backtester(make_wave(n), MaCross(fast=5, slow=20))
    return ReplayController(bt), bt


def test_step_through_to_completion(qapp):
    controller, _ = make_controller(n=120)
    batches, progresses, finished = [], [], []
    controller.events_batch.connect(batches.append)
    controller.progress.connect(lambda d, t: progresses.append((d, t)))
    controller.finished.connect(finished.append)

    guard = 0
    while not controller.done:
        controller.step()
        guard += 1
        assert guard < 130, "controller failed to finish"

    assert progresses[-1] == (120, 120)
    assert len(finished) == 1
    result = finished[0]
    equity_events = [
        e for batch in batches for e in batch if isinstance(e, EquityEvent)
    ]
    assert len(equity_events) >= 120
    assert result.final_balance == pytest.approx(
        result.initial_balance + sum(t.net for t in result.trades)
    )


def test_step_advances_exactly_one_bar(qapp):
    controller, _ = make_controller(n=50)
    controller.step()
    assert controller.bars_done == 1
    controller.step()
    assert controller.bars_done == 2


def test_fast_forward_completes_in_one_call(qapp):
    controller, bt = make_controller(n=200)
    finished = []
    controller.finished.connect(finished.append)
    controller.step()
    controller.fast_forward()
    assert controller.done
    assert len(finished) == 1
    controller.fast_forward()  # idempotent: no second emission
    assert len(finished) == 1
    assert len(finished[0].trades) == len(bt.broker.trades)


def make_position(pos_id=1, direction=Direction.LONG, sl=1.09, tp=1.12):
    return Position(
        id=pos_id, direction=direction, lots=1.0, entry_price=1.10,
        entry_time=None, entry_index=5, sl=sl, tp=tp,
    )


def test_trade_layer_lifecycle(qapp):
    plot = pg.PlotWidget()
    layer = TradeLayer(plot.getPlotItem())
    position = make_position()

    layer.handle(PositionOpened(5, position))
    assert layer.open_count == 1
    assert len(layer._buy_points) == 1

    position.sl = 1.095  # trailing stop moved
    layer.handle(PositionModified(8, position, old_sl=1.09, old_tp=1.12))
    assert layer._open_lines[1]["sl"].value() == pytest.approx(1.095)

    trade = Trade(
        id=1, direction=Direction.LONG, lots=1.0,
        entry_price=1.10, entry_time=None, entry_index=5,
        exit_price=1.12, exit_time=None, exit_index=12,
        profit=200.0, commission=0.0, swap=0.0, reason=CloseReason.TAKE_PROFIT,
    )
    layer.handle(PositionClosed(12, trade))
    assert layer.open_count == 0
    assert layer.closed_count == 1
    assert len(layer._win_link_points) == 2  # one entry->exit pair

    layer.clear()
    assert layer.closed_count == 0 and layer.open_count == 0


def test_trade_layer_modify_can_remove_and_add_levels(qapp):
    plot = pg.PlotWidget()
    layer = TradeLayer(plot.getPlotItem())
    position = make_position(sl=1.09, tp=None)
    layer.handle(PositionOpened(5, position))
    assert layer._open_lines[1]["tp"] is None

    position.sl, position.tp = None, 1.13
    layer.handle(PositionModified(6, position, old_sl=1.09, old_tp=None))
    assert layer._open_lines[1]["sl"] is None
    assert layer._open_lines[1]["tp"].value() == pytest.approx(1.13)


def test_backtest_tab_end_to_end(qapp, tmp_path):
    store = DataStore(tmp_path)
    store.save_bars(
        "TEST", "H1", make_wave(300),
        spec={"point": 1e-5, "digits": 5, "contract_size": 100_000.0},
    )
    tab = BacktestTab(store)
    assert tab.dataset_combo.currentText() == "TEST_H1"
    assert tab._df is not None and len(tab._df) == 300

    tab._start()
    assert tab._controller is not None
    tab._fast_forward()

    assert tab.result is not None
    assert tab.trade_layer.closed_count == len(tab.result.trades)
    assert len(tab._equity_x) >= 300
    assert "Finished" in tab.progress_label.text()
    assert tab.chart.candles.visible_length == 300
    assert not tab.grab().isNull()

    # Reset restores browse mode.
    tab._reset()
    assert tab.trade_layer.closed_count == 0
    assert tab.result is None
