"""Manual trading tab: play the replay and trade it by hand.

The session runs the normal engine with a :class:`ManualStrategy` that never
trades on its own; orders come from the user via three draggable chart lines
(entry / take-profit / stop-loss) and the order panel. Because everything goes
through the same ``SimBroker``, fills, SL/TP, costs, equity, and the final
statistics behave exactly as they do for an automated strategy.
"""

from __future__ import annotations

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from backtester.data.store import DataStore, StoreError
from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.events import BarEvent, EquityEvent
from backtester.engine.instrument import InstrumentSpec
from backtester.engine.orders import Direction
from backtester.engine.sizing import RiskMode, cash_at_risk, compute_lots, risk_cash
from backtester.strategy.manual import ManualStrategy
from backtester.ui.chart.chart_widget import BACKGROUND, ChartWidget
from backtester.ui.chart.order_lines import ENTRY, SL, TP, OrderLines
from backtester.ui.chart.replay_controller import ReplayController
from backtester.ui.chart.trade_markers import TradeLayer
from backtester.ui.manual_panel import ManualPanel

#: Bars revealed before handing control over, so there is context to trade from.
WARMUP_BARS = 100
VIEW_BARS = 200


def instrument_for(store: DataStore, symbol: str, timeframe: str):
    """(spec, from_broker) for a dataset — forex defaults when unknown."""
    info = store.get(symbol, timeframe)
    if info is not None and info.point and info.contract_size:
        return (
            InstrumentSpec.from_meta(
                symbol, info.point, info.digits or 5, info.contract_size
            ),
            True,
        )
    return InstrumentSpec.forex_major(symbol or "FX"), False


class ManualTab(QWidget):
    run_completed = Signal(object, str, bool)

    def __init__(self, store: DataStore, parent: QWidget | None = None):
        super().__init__(parent)
        self.store = store
        self._df = None
        self._loaded_key: str | None = None
        self._bt: Backtester | None = None
        self._controller: ReplayController | None = None
        self._broker = None
        self._instrument = InstrumentSpec.forex_major()
        self._pending_order = None
        self._last_close: float | None = None
        self._bar_index = -1
        self._lines_seeded = False
        self._equity_x: list[int] = []
        self._equity_balance: list[float] = []
        self._equity_equity: list[float] = []
        self.result = None

        layout = QHBoxLayout(self)
        layout.addWidget(self._build_left_panel())
        layout.addLayout(self._build_chart_side(), stretch=1)
        self.refresh_datasets()

    # ------------------------------------------------------------ UI build

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(300)
        column = QVBoxLayout(panel)

        self.dataset_combo = QComboBox()
        self.balance_spin = QDoubleSpinBox()
        self.balance_spin.setRange(1, 1e9)
        self.balance_spin.setDecimals(2)
        self.balance_spin.setValue(10_000)
        self.spread_data_check = QCheckBox("Use spread from data")
        self.spread_data_check.setChecked(True)
        self.spread_spin = QSpinBox()
        self.spread_spin.setRange(0, 10_000)
        self.spread_spin.setValue(10)
        self.spread_spin.setEnabled(False)
        self.spread_data_check.toggled.connect(
            lambda checked: self.spread_spin.setEnabled(not checked)
        )
        self.commission_spin = QDoubleSpinBox()
        self.commission_spin.setRange(0, 1_000)
        self.commission_spin.setDecimals(2)

        setup_group = QGroupBox("Session")
        setup_form = QFormLayout(setup_group)
        setup_form.addRow("Dataset:", self.dataset_combo)
        setup_form.addRow("Balance:", self.balance_spin)
        setup_form.addRow(self.spread_data_check)
        setup_form.addRow("Fixed spread (pts):", self.spread_spin)
        setup_form.addRow("Commission/lot/side:", self.commission_spin)

        self.start_button = QPushButton("▶  Start session")
        self.start_button.clicked.connect(self.start_session)

        self.panel = ManualPanel()
        self.panel.buy_clicked.connect(lambda: self._place(Direction.LONG))
        self.panel.sell_clicked.connect(lambda: self._place(Direction.SHORT))
        self.panel.close_clicked.connect(self._close_position)
        self.panel.cancel_clicked.connect(self._cancel_pending)
        self.panel.settings_changed.connect(self._update_preview)
        self.panel.lines_toggled.connect(self._sync_line_visibility)

        self.note_label = QLabel("")
        self.note_label.setWordWrap(True)
        self.note_label.setStyleSheet("color: gray;")

        column.addWidget(setup_group)
        column.addWidget(self.start_button)
        column.addWidget(self.panel)
        column.addWidget(self.note_label)
        column.addStretch()
        return panel

    def _build_chart_side(self) -> QVBoxLayout:
        self.play_button = QPushButton("Play")
        self.play_button.setFixedWidth(70)
        self.play_button.clicked.connect(self._toggle_play)
        self.next_button = QPushButton("Next candle")
        self.next_button.clicked.connect(self._step)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 100)
        self.speed_slider.setValue(5)
        self.speed_slider.setFixedWidth(160)
        self.speed_slider.valueChanged.connect(self._on_speed_changed)
        self.speed_label = QLabel("5 bars/s")
        self.follow_check = QCheckBox("Follow")
        self.follow_check.setChecked(True)
        self.follow_check.toggled.connect(self._on_follow_toggled)
        self.progress_label = QLabel("no session")
        for button in (self.play_button, self.next_button):
            button.setEnabled(False)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.play_button)
        toolbar.addWidget(self.next_button)
        toolbar.addWidget(QLabel("Speed:"))
        toolbar.addWidget(self.speed_slider)
        toolbar.addWidget(self.speed_label)
        toolbar.addWidget(self.follow_check)
        toolbar.addSpacing(12)
        toolbar.addWidget(self.progress_label)
        toolbar.addStretch()

        self.badge_label = QLabel(" ")
        self.badge_label.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px; padding: 2px;"
        )

        self.chart = ChartWidget()
        self.chart.follow_changed.connect(self.follow_check.setChecked)
        self.trade_layer = TradeLayer(self.chart.plot.getPlotItem())
        self.lines = OrderLines(self.chart.plot.getPlotItem())
        self.lines.moved.connect(self._on_line_moved)
        self.lines.move_finished.connect(self._on_line_move_finished)

        self.equity_plot = pg.PlotWidget()
        self.equity_plot.setBackground(BACKGROUND)
        self.equity_plot.setFixedHeight(120)
        self.equity_plot.showGrid(x=True, y=True, alpha=0.12)
        self.equity_plot.getPlotItem().setXLink(self.chart.plot.getPlotItem())
        self.equity_plot.getPlotItem().hideAxis("bottom")
        self._balance_curve = pg.PlotDataItem(pen=pg.mkPen("#787b86", width=1))
        self._equity_curve = pg.PlotDataItem(pen=pg.mkPen("#42a5f5", width=1.5))
        self.equity_plot.addItem(self._balance_curve)
        self.equity_plot.addItem(self._equity_curve)

        side = QVBoxLayout()
        side.addLayout(toolbar)
        side.addWidget(self.badge_label)
        side.addWidget(self.chart, stretch=1)
        side.addWidget(self.equity_plot)
        return side

    # ------------------------------------------------------------ datasets

    def refresh_datasets(self) -> None:
        keys = [info.key for info in self.store.datasets()]
        current = self.dataset_combo.currentText()
        self.dataset_combo.blockSignals(True)
        self.dataset_combo.clear()
        self.dataset_combo.addItems(keys)
        if current in keys:
            self.dataset_combo.setCurrentText(current)
        self.dataset_combo.blockSignals(False)

    def showEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        self.refresh_datasets()
        super().showEvent(event)

    # ------------------------------------------------------------- session

    def start_session(self) -> None:
        key = self.dataset_combo.currentText()
        if not key:
            QMessageBox.information(self, "Manual", "Download a dataset first.")
            return
        symbol, _, timeframe = key.rpartition("_")
        try:
            self._df = self.store.load_bars(symbol, timeframe)
        except (StoreError, ValueError) as exc:
            QMessageBox.warning(self, "Manual", str(exc))
            return
        if len(self._df) <= WARMUP_BARS + 5:
            QMessageBox.warning(self, "Manual", "Dataset is too short for a session.")
            return

        self._loaded_key = key
        self._instrument, from_broker = instrument_for(self.store, symbol, timeframe)
        self.note_label.setText(
            ""
            if from_broker
            else "No stored contract spec for this dataset — assuming a 5-digit "
                 "forex pair. Re-download it to capture the broker's spec."
        )

        self._stop_controller()
        self._reset_visuals()

        config = BacktestConfig(
            initial_balance=self.balance_spin.value(),
            spread_points=(
                None if self.spread_data_check.isChecked() else self.spread_spin.value()
            ),
            commission_per_lot=self.commission_spin.value(),
            instrument=self._instrument,
        )
        self._bt = Backtester(self._df, ManualStrategy(), config)
        self._broker = self._bt.broker

        self.chart.set_data(self._df, title=key.replace("_", " "))
        self.chart.reveal_to(0)

        self._controller = ReplayController(self._bt, parent=self)
        self._controller.events_batch.connect(self._on_events)
        self._controller.progress.connect(self._on_progress)
        self._controller.finished.connect(self._on_finished)
        self._controller.state_changed.connect(
            lambda playing: self.play_button.setText("Pause" if playing else "Play")
        )
        self._on_speed_changed(self.speed_slider.value())

        # Warm up so the trader has price history, then hand over — paused.
        self._controller.advance(WARMUP_BARS)
        self.chart.set_follow(self.follow_check.isChecked())
        self._seed_lines()

        for button in (self.play_button, self.next_button):
            button.setEnabled(True)
        self.panel.set_enabled(True)
        self.start_button.setText("↻  Restart session")
        self._update_preview()

    def _seed_lines(self) -> None:
        """Place the three lines around price, spaced by recent volatility."""
        if self._last_close is None or self._df is None:
            return
        window = self._df.iloc[max(0, self._bar_index - 20): self._bar_index + 1]
        spread = float((window["high"] - window["low"]).mean()) if len(window) else 0.0
        offset = max(spread * 2.0, self._instrument.point * 20)
        self.lines.seed_around(self._last_close, offset)
        self._lines_seeded = True
        self._sync_line_visibility()

    def _sync_line_visibility(self) -> None:
        """Entry line only matters for pending orders; TP/SL follow their checkboxes."""
        if not self._lines_seeded:
            return
        self.lines.set_visible(ENTRY, self.panel.is_pending)
        self.lines.set_visible(TP, self.panel.use_tp)
        self.lines.set_visible(SL, self.panel.use_sl)

    # -------------------------------------------------------- replay wiring

    def _on_events(self, events: list) -> None:
        last_bar = -1
        balance = equity = None
        for event in events:
            if isinstance(event, BarEvent):
                last_bar = max(last_bar, event.index)
                self._last_close = event.close
            elif isinstance(event, EquityEvent):
                self._equity_x.append(event.index)
                self._equity_balance.append(event.balance)
                self._equity_equity.append(event.equity)
                balance, equity = event.balance, event.equity
            else:
                self.trade_layer.handle(event)
        if last_bar >= 0:
            self._bar_index = last_bar
            self.chart.reveal_to(last_bar + 1)
        if balance is not None:
            self._balance_curve.setData(self._equity_x, self._equity_balance)
            self._equity_curve.setData(self._equity_x, self._equity_equity)
            self._update_badge(balance, equity)
        self._sync_position_state()
        self._update_preview()

    def _update_badge(self, balance: float, equity: float) -> None:
        position = self._position()
        if position is not None:
            side = "LONG" if position.is_long else "SHORT"
            detail = f"   {side} {position.lots:g} @ {position.entry_price:g}"
        else:
            detail = "   flat"
        self.badge_label.setText(
            f"Balance {balance:,.2f}   Equity {equity:,.2f}   "
            f"Floating {equity - balance:+,.2f}{detail}"
        )

    def _sync_position_state(self) -> None:
        position = self._position()
        self.panel.set_position_open(position is not None)
        pending_live = (
            self._pending_order is not None
            and self._broker is not None
            and self._pending_order in self._broker.pending
        )
        if not pending_live:
            self._pending_order = None
        self.panel.set_pending_open(pending_live)
        # Keep the SL/TP lines showing the live position's actual levels.
        if position is not None:
            if position.sl is not None:
                self.lines.set_price(SL, position.sl)
            if position.tp is not None:
                self.lines.set_price(TP, position.tp)

    def _on_progress(self, done: int, total: int) -> None:
        self.progress_label.setText(f"Bar {done:,} / {total:,}")

    def _on_finished(self, result) -> None:
        self.result = result
        stats = result.stats
        self.progress_label.setText(
            f"Session over — {stats['trades']} trades, "
            f"net {stats['net_profit']:+,.2f} ({stats['return_pct']:+.2f}%)"
        )
        self.play_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.panel.set_enabled(False)
        title = f"{(self._loaded_key or '').replace('_', ' ')} — manual session"
        self.run_completed.emit(result, title, True)

    # -------------------------------------------------------------- orders

    def _position(self):
        if self._broker is None or not self._broker.positions:
            return None
        return self._broker.positions[0]

    def _entry_estimate(self) -> float | None:
        """Price the order is expected to enter at (for risk sizing)."""
        if self.panel.is_pending:
            return self.lines.price(ENTRY)
        return self._last_close  # market fills at the next open ≈ this close

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

    def _levels(self) -> tuple[float | None, float | None]:
        sl = self.lines.visible_price(SL) if self.panel.use_sl else None
        tp = self.lines.visible_price(TP) if self.panel.use_tp else None
        return sl, tp

    def _validate(self, direction, entry, sl, tp) -> str | None:
        """Reason the order is invalid, or None if it's fine."""
        if entry is None:
            return "No price yet — start the session."
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

    def _place(self, direction: Direction) -> None:
        if self._broker is None:
            return
        entry = self._entry_estimate()
        sl, tp = self._levels()

        problem = self._validate(direction, entry, sl, tp)
        if problem:
            QMessageBox.warning(self, "Order", problem)
            return
        lots = self._resolve_lots(entry, sl)
        if lots is None:
            QMessageBox.warning(
                self,
                "Order",
                "Can't size this trade. Risk-based sizing needs a stop loss — "
                "enable one, or switch to fixed lots.",
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

        self._sync_position_state()
        self._update_preview()

    def _close_position(self) -> None:
        position = self._position()
        if position is not None and self._broker is not None:
            self._broker.close_position(position)  # fills at the next bar's open

    def _cancel_pending(self) -> None:
        if self._pending_order is not None and self._broker is not None:
            self._broker.cancel_order(self._pending_order)
            self._pending_order = None
            self._sync_position_state()

    # --------------------------------------------------------------- lines

    def _on_line_moved(self, _key: str) -> None:
        self._update_preview()

    def _on_line_move_finished(self, key: str) -> None:
        """On release, push new SL/TP to an open position (like a trailing stop)."""
        position = self._position()
        if position is None or self._broker is None or key not in (SL, TP):
            return
        sl, tp = self._levels()
        self._broker.modify_position(position, sl=sl, tp=tp)
        self._update_preview()

    def _update_preview(self) -> None:
        if self._broker is None:
            self.panel.set_preview("Start a session to trade.")
            return
        position = self._position()
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

    # ------------------------------------------------------------ playback

    def _toggle_play(self) -> None:
        if self._controller is not None:
            self._controller.toggle()

    def _step(self) -> None:
        if self._controller is not None:
            self._controller.pause()
            self._controller.step()

    def _on_speed_changed(self, value: int) -> None:
        self.speed_label.setText(f"{value} bars/s")
        if self._controller is not None:
            self._controller.set_speed(float(value))

    def _on_follow_toggled(self, checked: bool) -> None:
        self.chart.set_follow(checked)

    # ----------------------------------------------------------- lifecycle

    def _reset_visuals(self) -> None:
        self.trade_layer.clear()
        self.lines.hide_all()
        self._lines_seeded = False
        self._pending_order = None
        self._last_close = None
        self._bar_index = -1
        self._equity_x.clear()
        self._equity_balance.clear()
        self._equity_equity.clear()
        self._balance_curve.setData([], [])
        self._equity_curve.setData([], [])
        self.badge_label.setText(" ")
        self.result = None

    def _stop_controller(self) -> None:
        if self._controller is not None:
            self._controller.pause()
            self._controller.deleteLater()
            self._controller = None
        for button in (self.play_button, self.next_button):
            button.setEnabled(False)
        self.play_button.setText("Play")
        self.panel.set_enabled(False)

    def shutdown(self) -> None:
        self._stop_controller()
