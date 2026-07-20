"""Manual trading: position sizing math, and the Backtest tab's Manual mode."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from backtester.data.store import DataStore
from backtester.engine.orders import CloseReason, Direction
from backtester.engine.sizing import (
    RiskMode,
    cash_at_risk,
    compute_lots,
    risk_cash,
    round_lots,
)
from backtester.ui.backtest_tab import (
    MODE_MANUAL,
    MODE_STRATEGY,
    WARMUP_BARS,
    BacktestTab,
)
from backtester.ui.chart.order_lines import ENTRY, SL, TP
from backtester.ui.manual_panel import MARKET, PENDING

from tests.engine_utils import make_wave

CONTRACT = 100_000.0


# ---------------------------------------------------------------- sizing

def test_risk_cash_modes():
    assert risk_cash(RiskMode.PERCENT_BALANCE, 2.0, 10_000) == pytest.approx(200.0)
    assert risk_cash(RiskMode.CASH, 250.0, 10_000) == pytest.approx(250.0)
    assert risk_cash(RiskMode.LOTS, 0.5, 10_000) is None


def test_compute_lots_from_percent_risk():
    # Risk 200 over a 0.0050 stop on a 100k contract → 200 / (0.005 * 100000) = 0.4
    lots = compute_lots(
        RiskMode.PERCENT_BALANCE, 2.0, 10_000,
        entry=1.1000, sl=1.0950, contract_size=CONTRACT,
    )
    assert lots == pytest.approx(0.40)
    assert cash_at_risk(lots, 1.1000, 1.0950, CONTRACT) == pytest.approx(200.0)


def test_compute_lots_from_cash_risk_rounds_down():
    # 100 / (0.0030 * 100000) = 0.3333… → floors to 0.33 so risk is never overshot
    lots = compute_lots(
        RiskMode.CASH, 100.0, 10_000,
        entry=1.1000, sl=1.0970, contract_size=CONTRACT,
    )
    assert lots == pytest.approx(0.33)
    assert cash_at_risk(lots, 1.1000, 1.0970, CONTRACT) <= 100.0


def test_fixed_lots_mode_ignores_stop():
    assert compute_lots(
        RiskMode.LOTS, 0.25, 10_000, entry=None, sl=None, contract_size=CONTRACT
    ) == pytest.approx(0.25)


def test_risk_sizing_needs_a_stop():
    assert compute_lots(
        RiskMode.CASH, 100.0, 10_000, entry=1.10, sl=None, contract_size=CONTRACT
    ) is None
    # zero distance is equally unusable
    assert compute_lots(
        RiskMode.CASH, 100.0, 10_000, entry=1.10, sl=1.10, contract_size=CONTRACT
    ) is None


def test_round_lots_floors_but_respects_minimum():
    assert round_lots(0.567) == pytest.approx(0.56)
    assert round_lots(0.0001) == pytest.approx(0.01)  # min tradeable size


# --------------------------------------------------- Backtest tab, manual

@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def tab(qapp, tmp_path, monkeypatch):
    monkeypatch.setattr(
        "backtester.ui.backtest_tab.app_settings",
        lambda: QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat),
    )
    store = DataStore(tmp_path)
    store.save_bars(
        "TEST", "H1", make_wave(400, period=80),
        spec={"point": 1e-5, "digits": 5, "contract_size": CONTRACT},
    )
    widget = BacktestTab(store)
    widget.dataset_combo.setCurrentText("TEST_H1")
    widget.mode_combo.setCurrentText(MODE_MANUAL)
    yield widget
    widget.shutdown()


def no_popups(monkeypatch) -> list:
    """Capture warnings instead of opening a modal that would block the test."""
    warned: list = []
    monkeypatch.setattr(
        "backtester.ui.backtest_tab.QMessageBox.warning",
        lambda *args, **kwargs: warned.append(args[-1]),
    )
    return warned


def arm(tab, stop_offset=0.005, target_offset=0.005):
    """Start a session and position the SL/TP lines around price."""
    tab._start()
    price = tab.manual.last_close
    tab.manual.lines.set_price(SL, price - stop_offset)
    tab.manual.lines.set_price(TP, price + target_offset)
    return price


# --- mode switching

def test_manual_mode_swaps_the_setup_panel(tab):
    assert tab.is_manual
    assert tab.manual_panel.isVisibleTo(tab)
    assert not tab.strategy_group.isVisibleTo(tab)
    assert not tab.params_group.isVisibleTo(tab)
    assert not tab.fast_button.isVisibleTo(tab)   # nothing to fast-run
    assert "Manual" in tab.start_button.text()


def test_switching_back_restores_strategy_mode(tab):
    tab.mode_combo.setCurrentText(MODE_STRATEGY)
    assert not tab.is_manual
    assert tab.strategy_group.isVisibleTo(tab)
    assert tab.params_group.isVisibleTo(tab)
    assert tab.fast_button.isVisibleTo(tab)
    assert not tab.manual_panel.isVisibleTo(tab)
    assert not tab.manual.active


def test_strategy_mode_still_runs(tab):
    """Regression: the automatic replay is unaffected by manual mode."""
    tab.mode_combo.setCurrentText(MODE_STRATEGY)
    tab._start()
    tab._fast_forward()
    assert tab.result is not None
    assert tab.result.stats["trades"] >= 0
    assert not tab.manual.active


# --- session

def test_session_warms_up_then_pauses(tab):
    tab._start()
    assert tab._controller is not None
    assert not tab._controller.playing          # hands over paused
    assert tab._controller.bars_done == WARMUP_BARS
    assert tab.chart.candles.visible_length == WARMUP_BARS
    assert tab.manual.active and tab.manual.last_close is not None
    assert tab.manual.lines.is_visible(SL) and tab.manual.lines.is_visible(TP)


def test_next_candle_advances_one_bar(tab):
    tab._start()
    before = tab._controller.bars_done
    tab._step()
    assert tab._controller.bars_done == before + 1


# --- orders

def test_market_buy_fills_on_next_bar(tab):
    price = arm(tab)
    tab.manual_panel.type_combo.setCurrentText(MARKET)

    tab.manual.place(Direction.LONG)
    assert tab.manual.broker.positions == []    # queued, not yet filled
    tab._step()

    position = tab.manual.broker.positions[0]
    assert position.is_long
    assert position.sl == pytest.approx(price - 0.005)
    assert tab.manual_panel.close_button.isEnabled()


def test_pending_order_uses_entry_line(tab):
    price = arm(tab, stop_offset=-0.004, target_offset=0.02)
    tab.manual_panel.type_combo.setCurrentText(PENDING)
    tab.manual.sync_line_visibility()
    tab.manual.lines.set_price(ENTRY, price + 0.01)   # above price → buy stop

    tab.manual.place(Direction.LONG)
    order = tab.manual._pending_order
    assert order is not None and order in tab.manual.broker.pending
    assert order.price == pytest.approx(price + 0.01)
    assert tab.manual_panel.cancel_button.isEnabled()

    tab.manual.cancel_pending()
    assert tab.manual.broker.pending == []


def test_invalid_stop_side_is_refused(tab, monkeypatch):
    warned = no_popups(monkeypatch)
    price = arm(tab)
    tab.manual.lines.set_price(SL, price + 0.005)     # stop above entry on a buy
    tab.manual.place(Direction.LONG)

    assert warned and "below the entry" in warned[0]
    assert tab.manual.broker.positions == [] and tab.manual.broker.pending == []


def test_risk_sizing_without_stop_is_refused(tab, monkeypatch):
    warned = no_popups(monkeypatch)
    tab._start()
    tab.manual_panel.sl_check.setChecked(False)       # no stop, still on % risk
    tab.manual.place(Direction.LONG)

    assert warned and "needs a stop loss" in warned[0]
    assert tab.manual.broker.positions == []


def test_fixed_lots_works_without_a_stop(tab):
    tab._start()
    tab.manual_panel.sl_check.setChecked(False)
    tab.manual_panel.tp_check.setChecked(False)
    tab.manual_panel._radios[RiskMode.LOTS].setChecked(True)
    tab.manual_panel._spins[RiskMode.LOTS].setValue(0.20)

    tab.manual.place(Direction.LONG)
    tab._step()

    position = tab.manual.broker.positions[0]
    assert position.lots == pytest.approx(0.20)
    assert position.sl is None and position.tp is None


def test_percent_risk_sizes_the_position(tab):
    price = arm(tab, stop_offset=0.0020, target_offset=0.0040)
    tab.manual_panel._radios[RiskMode.PERCENT_BALANCE].setChecked(True)
    tab.manual_panel._spins[RiskMode.PERCENT_BALANCE].setValue(1.0)  # 1% of 10k = 100

    tab.manual.place(Direction.LONG)                 # 100/(0.002*100k) = 0.5
    tab._step()
    assert tab.manual.broker.positions[0].lots == pytest.approx(0.50)


def test_dragging_stop_modifies_open_position(tab):
    price = arm(tab)
    tab.manual.place(Direction.LONG)
    tab._step()
    position = tab.manual.broker.positions[0]

    tab.manual.lines.set_price(SL, price - 0.002)    # trail it up
    tab.manual._on_line_move_finished(SL)
    assert position.sl == pytest.approx(price - 0.002)


def test_close_button_exits_on_next_bar(tab):
    arm(tab)
    tab.manual.place(Direction.LONG)
    tab._step()
    assert len(tab.manual.broker.positions) == 1

    tab.manual.close_position()
    tab._step()
    assert tab.manual.broker.positions == []
    assert tab.manual.broker.trades[-1].reason is CloseReason.MANUAL


# --- preview

def test_preview_flags_risk_overshoot_from_minimum_lot(tab):
    price = arm(tab, stop_offset=0.05)
    tab.manual_panel._radios[RiskMode.CASH].setChecked(True)
    tab.manual_panel._spins[RiskMode.CASH].setValue(1.0)   # wants to risk 1.00
    tab.manual.update_preview()

    text = tab.manual_panel.preview_label.text()
    assert "⚠" in text and "over your" in text


def test_preview_has_no_warning_when_risk_is_honoured(tab):
    arm(tab, stop_offset=0.0020)
    tab.manual_panel._radios[RiskMode.PERCENT_BALANCE].setChecked(True)
    tab.manual_panel._spins[RiskMode.PERCENT_BALANCE].setValue(1.0)
    tab.manual.update_preview()
    assert "⚠" not in tab.manual_panel.preview_label.text()


# --- completion / playback

def test_session_completes_and_reports_results(tab):
    arm(tab)
    tab.manual.place(Direction.LONG)

    completed = []
    tab.run_completed.connect(lambda r, t, s: completed.append((r, t, s)))
    tab._controller.fast_forward()

    assert tab.result is not None
    assert len(completed) == 1
    result, title, _switch = completed[0]
    assert "manual session" in title
    assert result.final_balance == pytest.approx(
        result.initial_balance + sum(t.net for t in result.trades)
    )
    assert not tab.manual_panel.buy_button.isEnabled()   # session over


def test_speed_slider_drives_the_controller(tab):
    tab._start()
    tab.speed_slider.setValue(42)
    assert tab._controller.speed == pytest.approx(42.0)
    assert "42" in tab.speed_label.text()


def test_tab_renders(tab):
    tab._start()
    tab.resize(1200, 800)
    assert not tab.grab().isNull()
