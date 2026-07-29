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
from backtester.ui.backtest_tab import MODE_MANUAL, MODE_STRATEGY, BacktestTab
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


def make_rewindable(n=200, fast=5, slow=20):
    """A controller that can rebuild its run — the rewind precondition."""
    df = make_wave(n)

    def build():
        return Backtester(df, MaCross(fast=fast, slow=slow))

    return ReplayController(build(), rebuild=build)


def test_rewind_steps_back_one_bar(qapp):
    controller = make_rewindable()
    controller.advance(40)
    assert controller.bars_done == 40
    controller.rewind()
    assert controller.bars_done == 39


def test_rewind_reproduces_the_state_it_returns_to(qapp):
    """The rebuilt run must match a fresh run advanced to the same bar."""
    controller = make_rewindable()
    controller.advance(80)
    controller.rewind(30)
    assert controller.bars_done == 50

    reference = make_rewindable()
    reference.advance(50)

    rewound, expected = controller.backtester.broker, reference.backtester.broker
    assert rewound.balance == pytest.approx(expected.balance)
    assert len(rewound.trades) == len(expected.trades)
    assert len(rewound.positions) == len(expected.positions)
    assert [t.exit_index for t in rewound.trades] == [
        t.exit_index for t in expected.trades
    ]
    assert [t.net for t in rewound.trades] == pytest.approx(
        [t.net for t in expected.trades]
    )


def test_rewind_emits_rewound_before_replaying_kept_bars(qapp):
    controller = make_rewindable()
    controller.advance(60)
    order = []
    controller.rewound.connect(lambda bar: order.append(("rewound", bar)))
    controller.events_batch.connect(lambda batch: order.append(("events", len(batch))))
    controller.rewind(10)

    assert order[0] == ("rewound", 50)
    assert [kind for kind, _ in order[1:]] == ["events"]


def test_rewind_past_the_start_lands_on_bar_zero(qapp):
    controller = make_rewindable()
    controller.advance(5)
    batches = []
    controller.events_batch.connect(batches.append)
    controller.rewind(500)
    assert controller.bars_done == 0
    assert batches == []  # nothing to replay, so nothing is emitted


def test_rewind_reopens_a_finished_run(qapp):
    controller = make_rewindable(n=120)
    controller.fast_forward()
    assert controller.done

    controller.rewind(1)
    assert not controller.done
    controller.step()
    assert controller.bars_done == 120


def test_rewind_can_finish_again_after_rewinding(qapp):
    """A rebuilt run still terminates and reports a result."""
    controller = make_rewindable(n=120)
    finished = []
    controller.fast_forward()
    controller.finished.connect(finished.append)
    controller.rewind(20)
    controller.fast_forward()
    assert controller.done
    assert len(finished) == 1
    assert finished[0].final_balance == pytest.approx(
        finished[0].initial_balance + sum(t.net for t in finished[0].trades)
    )


def test_rewind_without_a_rebuild_factory_is_a_no_op(qapp):
    controller, _ = make_controller(n=50)
    assert not controller.can_rewind
    controller.advance(20)
    controller.rewind(5)
    assert controller.bars_done == 20


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
    tab.mode_combo.setCurrentText(MODE_STRATEGY)  # don't inherit the saved mode
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


def make_tab(store_path, n=300, mode=MODE_STRATEGY):
    """A tab pinned to ``mode`` — the tab otherwise restores the mode saved in
    the developer's own QSettings, which would decide these tests for them."""
    store = DataStore(store_path)
    store.save_bars(
        "TEST", "H1", make_wave(n),
        spec={"point": 1e-5, "digits": 5, "contract_size": 100_000.0},
    )
    tab = BacktestTab(store)
    tab.mode_combo.setCurrentText(mode)
    return tab


def test_backtest_tab_rewind_redraws_the_run(qapp, tmp_path):
    tab = make_tab(tmp_path)
    tab._start()
    tab._controller.pause()
    tab._controller.advance(200)
    drawn_at_200 = tab.trade_layer.closed_count
    assert tab.chart.candles.visible_length == 200

    tab._rewind()

    assert tab._controller.bars_done == 199
    assert tab.chart.candles.visible_length == 199
    # Visuals were rebuilt from the replayed events, not left stale.
    assert tab.trade_layer.closed_count <= drawn_at_200
    assert len(tab._equity_x) == 199
    assert tab._equity_x == list(range(199))
    assert tab.rewind_button.isEnabled()


def test_backtest_tab_rewind_survives_running_to_the_end_again(qapp, tmp_path):
    tab = make_tab(tmp_path)
    tab._start()
    tab._fast_forward()
    trades_first_pass = len(tab.result.trades)

    tab._rewind()
    assert tab.result is None          # the finished result no longer holds
    assert tab.play_button.isEnabled()
    tab._fast_forward()

    assert tab.result is not None
    assert len(tab.result.trades) == trades_first_pass
    assert tab.trade_layer.closed_count == len(tab.result.trades)


def test_rewind_is_unavailable_in_manual_mode(qapp, tmp_path):
    """A rebuilt run would not contain the trades the user placed by hand."""
    tab = make_tab(tmp_path, mode=MODE_MANUAL)
    tab._start()
    assert tab._controller is not None
    assert not tab._controller.can_rewind
    assert not tab.rewind_button.isEnabled()
