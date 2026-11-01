"""Manual order management for a replay session.

Owns the three draggable chart lines and drives the order panel, translating
what the user sets on the chart into orders on the live ``SimBroker``. Kept
separate from the Backtest tab so the tab stays readable and this logic is
testable on its own.
"""

from __future__ import annotations

import pyqtgraph as pg
from PySide6.QtCore import QObject, Signal

from backtester.engine.instrument import InstrumentSpec
from backtester.engine.orders import Direction
from backtester.engine.sizing import cash_at_risk, compute_lots, risk_cash
from backtester.ui.chart.order_lines import ENTRY, SL, TP, OrderLines
from backtester.ui.manual_panel import ManualPanel


class ManualTrader(QObject):
    """Turns chart lines + panel settings into broker orders."""

    warning = Signal(str)

    def __init__(
        self,
        plot_item: pg.PlotItem,
        panel: ManualPanel,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self.lines = OrderLines(plot_item, parent=self)
        self.panel = panel

        self._broker = None
        self._df = None
        self._instrument = InstrumentSpec.forex_major()
        self._pending_order = None
        self._last_close: float | None = None
        self._bar_index = -1
        self._seeded = False
        # In market mode the entry line tracks live price until the user drags
        # it; a drag pins it so their adjustment sticks.
        self._entry_follow = True

        panel.buy_clicked.connect(lambda: self.place(Direction.LONG))
        panel.sell_clicked.connect(lambda: self.place(Direction.SHORT))
        panel.close_clicked.connect(self.close_position)
        panel.cancel_clicked.connect(self.cancel_pending)
        panel.settings_changed.connect(self.update_preview)
        panel.lines_toggled.connect(self.sync_line_visibility)
        panel.type_combo.currentTextChanged.connect(self._on_order_type_changed)
        self.lines.moved.connect(self._on_line_moved)
        self.lines.move_finished.connect(self._on_line_move_finished)

    # ------------------------------------------------------------ lifecycle

    def attach(self, broker, instrument: InstrumentSpec, df) -> None:
        self._broker = broker
        self._instrument = instrument
        self._df = df
        self._pending_order = None
        self._last_close = None
        self._bar_index = -1
        self._seeded = False
        self._entry_follow = True
        self.panel.set_enabled(True)

    def detach(self) -> None:
        self._broker = None
        self._pending_order = None
        self._seeded = False
        self.lines.hide_all()
        self.panel.set_enabled(False)
        self.panel.set_preview("—")

    @property
    def active(self) -> bool:
        return self._broker is not None

    @property
    def broker(self):
        return self._broker

    @property
    def last_close(self) -> float | None:
        return self._last_close

    # --------------------------------------------------------------- clock

    def on_bars_advanced(self, bar_index: int, last_close: float) -> None:
        self._bar_index = bar_index
        self._last_close = last_close
        # Refresh position/order state first so TP/SL only ride along with the
        # entry line while nothing live owns them.
        self._sync_position_state()
        if not self._seeded:
            self.seed_lines()
        elif self._entry_follow and not self.panel.is_pending:
            # Market mode: the entry line follows live price (bars are bid).
            self.lines.move_entry(last_close)
        self.update_preview()

    def seed_lines(self) -> None:
        """Place the lines around price, spaced by recent volatility."""
        if self._last_close is None or self._df is None:
            return
        window = self._df.iloc[max(0, self._bar_index - 20): self._bar_index + 1]
        spread = float((window["high"] - window["low"]).mean()) if len(window) else 0.0
        offset = max(spread * 2.0, self._instrument.point * 20)
        self.lines.seed_around(self._last_close, offset)
        self._seeded = True
        self.sync_line_visibility()

    def sync_line_visibility(self) -> None:
        """The entry line is always shown; TP/SL follow their checkboxes."""
        if not self._seeded:
            return
        self.lines.set_visible(ENTRY, True)
        self.lines.set_visible(TP, self.panel.use_tp)
        self.lines.set_visible(SL, self.panel.use_sl)

    def _on_order_type_changed(self, _text: str) -> None:
        """Switching back to Market resumes following live price."""
        if not self.panel.is_pending and self._seeded and self._last_close is not None:
            self._entry_follow = True
            self.lines.move_entry(self._last_close)
        self.sync_line_visibility()
        self.update_preview()

    def sync(self) -> None:
        self._sync_position_state()
        self.update_preview()

    # -------------------------------------------------------------- orders

    def position(self):
        if self._broker is None or not self._broker.positions:
            return None
        return self._broker.positions[0]

    def _entry_estimate(self) -> float | None:
        # The entry line is the intended price in both modes — the trigger for
        # a pending order, and the live-tracked price for a market order.
        if self._last_close is None:
            return None
        return self.lines.price(ENTRY)

    def _levels(self) -> tuple[float | None, float | None]:
        sl = self.lines.visible_price(SL) if self.panel.use_sl else None
        tp = self.lines.visible_price(TP) if self.panel.use_tp else None
        return sl, tp

    def _resolve_lots(self, entry: float | None, sl: float | None) -> float | None:
        if self._broker is None:
            return None
        return compute_lots(
            self.panel.risk_mode,
            self.panel.risk_value,
            self._broker.balance,
            entry,
            sl,
            self._instrument.contract_size,
        )

    def _validate(self, direction, entry, sl, tp) -> str | None:
        if entry is None:
            return "No price yet — start the replay first."
        if direction is Direction.LONG:
            if sl is not None and sl >= entry:
                return "For a buy, the stop loss must sit below the entry."
            if tp is not None and tp <= entry:
                return "For a buy, the take profit must sit above the entry."
        else:
            if sl is not None and sl <= entry:
                return "For a sell, the stop loss must sit above the entry."
            if tp is not None and tp >= entry:
                return "For a sell, the take profit must sit below the entry."
        return None

    def place(self, direction: Direction) -> None:
        if self._broker is None:
            return
        entry = self._entry_estimate()
        sl, tp = self._levels()

        problem = self._validate(direction, entry, sl, tp)
        if problem:
            self.warning.emit(problem)
            return
        lots = self._resolve_lots(entry, sl)
        if lots is None:
            self.warning.emit(
                "Can't size this trade. Risk-based sizing needs a stop loss — "
                "enable one, or switch to fixed lots."
            )
            return

        if self.panel.is_pending:
            price = self.lines.price(ENTRY)
            breakout = (
                price > self._last_close
                if direction is Direction.LONG
                else price < self._last_close
            )
            place = self._broker.stop_order if breakout else self._broker.limit_order
            self._pending_order = place(direction, lots, price, sl=sl, tp=tp)
        else:
            self._broker.market_order(direction, lots, sl=sl, tp=tp)
        self.sync()

    def close_position(self) -> None:
        position = self.position()
        if position is not None and self._broker is not None:
            self._broker.close_position(position)  # fills at the next bar's open

    def cancel_pending(self) -> None:
        if self._pending_order is not None and self._broker is not None:
            self._broker.cancel_order(self._pending_order)
            self._pending_order = None
            self.sync()

    def _on_line_moved(self, key: str) -> None:
        if key == ENTRY:
            # The user is positioning the entry themselves — stop auto-following.
            self._entry_follow = False
        self.update_preview()

    def _on_line_move_finished(self, key: str) -> None:
        """On release, push new SL/TP to an open position (like a trailing stop)."""
        position = self.position()
        if position is None or self._broker is None or key not in (SL, TP):
            return
        sl, tp = self._levels()
        self._broker.modify_position(position, sl=sl, tp=tp)
        self.update_preview()

    # ------------------------------------------------------------- display

    def _sync_position_state(self) -> None:
        position = self.position()
        self.panel.set_position_open(position is not None)
        pending_live = (
            self._pending_order is not None
            and self._broker is not None
            and self._pending_order in self._broker.pending
        )
        if not pending_live:
            self._pending_order = None
        self.panel.set_pending_open(pending_live)
        self.lines.brackets_follow_entry = position is None and not pending_live
        if position is not None:
            if position.sl is not None:
                self.lines.set_price(SL, position.sl)
            if position.tp is not None:
                self.lines.set_price(TP, position.tp)

    def update_preview(self) -> None:
        if self._broker is None:
            self.panel.set_preview("Start the replay in Manual mode to trade.")
            return
        position = self.position()
        if position is not None:
            self.panel.set_preview(
                f"Managing {'LONG' if position.is_long else 'SHORT'} "
                f"{position.lots:g} @ {position.entry_price:g} — drag SL/TP to adjust."
            )
            return

        entry = self._entry_estimate()
        sl, tp = self._levels()
        lots = self._resolve_lots(entry, sl)
        if entry is None:
            self.panel.set_preview("—")
            return
        if lots is None:
            self.panel.set_preview(
                "Set a stop loss to size by risk, or choose fixed lots."
            )
            return

        kind = "Pending" if self.panel.is_pending else "Market"
        risk = cash_at_risk(lots, entry, sl, self._instrument.contract_size)
        risk_text = f" · risking {risk:,.2f}" if risk is not None else " · no stop"
        target = f" · TP {tp:g}" if tp is not None else ""
        text = f"{kind} @ {entry:g} · {lots:g} lots{risk_text}{target}"

        # The minimum lot size can force far more risk than was asked for —
        # say so loudly rather than quietly printing a scary number.
        wanted = risk_cash(
            self.panel.risk_mode, self.panel.risk_value, self._broker.balance
        )
        if risk is not None and wanted is not None and risk > wanted * 1.05:
            text += (
                f"\n⚠ Smallest tradeable size risks {risk:,.2f}, well over your "
                f"{wanted:,.2f} target — widen the stop, or check the contract spec."
            )
        self.panel.set_preview(text)
