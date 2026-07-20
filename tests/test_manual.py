"""Manual trading: position sizing math and the Manual tab end to end."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
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
from backtester.ui.chart.order_lines import ENTRY, SL, TP
from backtester.ui.manual_panel import MARKET, PENDING
from backtester.ui.manual_tab import WARMUP_BARS, ManualTab

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


# ------------------------------------------------------------- manual tab

@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def tab(qapp, tmp_path):
    store = DataStore(tmp_path)
    store.save_bars(
        "TEST", "H1", make_wave(400, period=80),
        spec={"point": 1e-5, "digits": 5, "contract_size": CONTRACT},
    )
    widget = ManualTab(store)
    widget.dataset_combo.setCurrentText("TEST_H1")
    yield widget
    widget.shutdown()


def test_session_warms_up_then_pauses(tab):
    tab.start_session()
    assert tab._controller is not None
    assert not tab._controller.playing          # hands over paused
    assert tab._controller.bars_done == WARMUP_BARS
    assert tab.chart.candles.visible_length == WARMUP_BARS
    assert tab._last_close is not None
    assert tab.lines.is_visible(SL) and tab.lines.is_visible(TP)


def test_next_candle_advances_one_bar(tab):
    tab.start_session()
    before = tab._controller.bars_done
    tab._step()
    assert tab._controller.bars_done == before + 1


def test_market_buy_fills_on_next_bar(tab):
    tab.start_session()
    price = tab._last_close
    tab.panel.type_combo.setCurrentText(MARKET)
    tab.lines.set_price(SL, price - 0.005)
    tab.lines.set_price(TP, price + 0.005)

    tab._place(Direction.LONG)
    assert tab._broker.positions == []          # queued, not yet filled
    tab._step()

    assert len(tab._broker.positions) == 1
    position = tab._broker.positions[0]
    assert position.is_long
    assert position.sl == pytest.approx(price - 0.005)
    assert tab.panel.close_button.isEnabled()


def test_pending_order_uses_entry_line(tab):
    tab.start_session()
    price = tab._last_close
    tab.panel.type_combo.setCurrentText(PENDING)
    tab._sync_line_visibility()
    tab.lines.set_price(ENTRY, price + 0.01)    # above price → buy stop
    tab.lines.set_price(SL, price + 0.004)
    tab.lines.set_price(TP, price + 0.02)

    tab._place(Direction.LONG)
    assert tab._pending_order is not None
    assert tab._pending_order in tab._broker.pending
    assert tab._pending_order.price == pytest.approx(price + 0.01)
    assert tab.panel.cancel_button.isEnabled()

    tab._cancel_pending()
    assert tab._broker.pending == []


def test_invalid_stop_side_is_refused(tab, monkeypatch):
    tab.start_session()
    warned = []
    monkeypatch.setattr(
        "backtester.ui.manual_tab.QMessageBox.warning",
        lambda *args, **kwargs: warned.append(args[-1]),
    )
    price = tab._last_close
    tab.lines.set_price(SL, price + 0.005)      # stop above entry on a buy
    tab._place(Direction.LONG)

    assert warned and "below the entry" in warned[0]
    assert tab._broker.positions == [] and tab._broker.pending == []


def test_risk_sizing_without_stop_is_refused(tab, monkeypatch):
    tab.start_session()
    warned = []
    monkeypatch.setattr(
        "backtester.ui.manual_tab.QMessageBox.warning",
        lambda *args, **kwargs: warned.append(args[-1]),
    )
    tab.panel.sl_check.setChecked(False)        # no stop, still on % risk
    tab._place(Direction.LONG)

    assert warned and "needs a stop loss" in warned[0]
    assert tab._broker.positions == []


def test_fixed_lots_works_without_a_stop(tab):
    tab.start_session()
    tab.panel.sl_check.setChecked(False)
    tab.panel.tp_check.setChecked(False)
    tab.panel._radios[RiskMode.LOTS].setChecked(True)
    tab.panel._spins[RiskMode.LOTS].setValue(0.20)

    tab._place(Direction.LONG)
    tab._step()

    assert len(tab._broker.positions) == 1
    position = tab._broker.positions[0]
    assert position.lots == pytest.approx(0.20)
    assert position.sl is None and position.tp is None


def test_percent_risk_sizes_the_position(tab):
    tab.start_session()
    price = tab._last_close
    tab.panel._radios[RiskMode.PERCENT_BALANCE].setChecked(True)
    tab.panel._spins[RiskMode.PERCENT_BALANCE].setValue(1.0)  # 1% of 10,000 = 100
    tab.lines.set_price(SL, price - 0.0020)                   # 100/(0.002*100k) = 0.5
    tab.lines.set_price(TP, price + 0.0040)

    tab._place(Direction.LONG)
    tab._step()
    assert tab._broker.positions[0].lots == pytest.approx(0.50)


def test_dragging_stop_modifies_open_position(tab):
    tab.start_session()
    price = tab._last_close
    tab.lines.set_price(SL, price - 0.005)
    tab.lines.set_price(TP, price + 0.005)
    tab._place(Direction.LONG)
    tab._step()
    position = tab._broker.positions[0]

    tab.lines.set_price(SL, price - 0.002)      # trail it up
    tab._on_line_move_finished(SL)
    assert position.sl == pytest.approx(price - 0.002)


def test_close_button_exits_on_next_bar(tab):
    tab.start_session()
    price = tab._last_close
    tab.lines.set_price(SL, price - 0.005)
    tab.lines.set_price(TP, price + 0.005)
    tab._place(Direction.LONG)
    tab._step()
    assert len(tab._broker.positions) == 1

    tab._close_position()
    tab._step()
    assert tab._broker.positions == []
    assert tab._broker.trades[-1].reason is CloseReason.MANUAL


def test_session_completes_and_reports_results(tab):
    tab.start_session()
    price = tab._last_close
    tab.lines.set_price(SL, price - 0.005)
    tab.lines.set_price(TP, price + 0.005)
    tab._place(Direction.LONG)

    completed = []
    tab.run_completed.connect(lambda r, t, s: completed.append((r, t, s)))
    tab._controller.fast_forward()

    assert tab.result is not None
    assert len(completed) == 1
    result, title, switch = completed[0]
    assert switch is True and "manual" in title
    assert result.final_balance == pytest.approx(
        result.initial_balance + sum(t.net for t in result.trades)
    )
    assert not tab.panel.buy_button.isEnabled()


def test_preview_flags_risk_overshoot_from_minimum_lot(tab):
    tab.start_session()
    price = tab._last_close
    tab.panel._radios[RiskMode.CASH].setChecked(True)
    tab.panel._spins[RiskMode.CASH].setValue(1.0)   # want to risk 1.00
    tab.lines.set_price(SL, price - 0.05)           # min lot already risks far more
    tab._update_preview()

    text = tab.panel.preview_label.text()
    assert "⚠" in text and "over your" in text


def test_preview_has_no_warning_when_risk_is_honoured(tab):
    tab.start_session()
    price = tab._last_close
    tab.panel._radios[RiskMode.PERCENT_BALANCE].setChecked(True)
    tab.panel._spins[RiskMode.PERCENT_BALANCE].setValue(1.0)
    tab.lines.set_price(SL, price - 0.0020)         # sizes cleanly to 0.50 lots
    tab._update_preview()
    assert "⚠" not in tab.panel.preview_label.text()


def test_speed_slider_drives_the_controller(tab):
    tab.start_session()
    tab.speed_slider.setValue(42)
    assert tab._controller.speed == pytest.approx(42.0)
    assert "42" in tab.speed_label.text()


def test_tab_renders(tab):
    tab.start_session()
    tab.resize(1200, 800)
    assert not tab.grab().isNull()
