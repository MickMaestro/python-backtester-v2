"""Backtest tab: configure a run, then watch it replay on the chart.

Left panel: dataset, strategy (parameter form auto-generated from the
strategy's ``params`` declaration), and account settings. Right side: the
replay chart with playback controls, live trade drawing, and an equity
sub-chart synced to the replay clock.
"""

from __future__ import annotations

import pyqtgraph as pg
from PySide6.QtCore import Qt
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
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from backtester.data.store import DataStore, StoreError
from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.events import BarEvent, EquityEvent
from backtester.engine.instrument import InstrumentSpec
from backtester.strategy.examples import STRATEGIES
from backtester.ui.chart.chart_widget import BACKGROUND, ChartWidget
from backtester.ui.chart.replay_controller import ReplayController
from backtester.ui.chart.trade_markers import TradeLayer

SPEEDS = [1, 2, 5, 10, 25, 50, 100, 250]
INITIAL_WINDOW = 300


class BacktestTab(QWidget):
    def __init__(self, store: DataStore, parent: QWidget | None = None):
        super().__init__(parent)
        self.store = store
        self._df = None
        self._loaded_key: str | None = None
        self._controller: ReplayController | None = None
        self._param_widgets: dict[str, QWidget] = {}
        self._equity_x: list[int] = []
        self._equity_balance: list[float] = []
        self._equity_equity: list[float] = []
        self.result = None

        layout = QHBoxLayout(self)
        layout.addWidget(self._build_setup_panel())
        layout.addLayout(self._build_replay_side(), stretch=1)
        self.refresh_datasets()

    # ------------------------------------------------------------ UI build

    def _build_setup_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(300)
        column = QVBoxLayout(panel)

        self.dataset_combo = QComboBox()
        self.dataset_combo.currentTextChanged.connect(self._on_dataset_changed)
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems(sorted(STRATEGIES))
        self.strategy_combo.currentTextChanged.connect(self._rebuild_param_form)

        data_group = QGroupBox("Setup")
        data_form = QFormLayout(data_group)
        data_form.addRow("Dataset:", self.dataset_combo)
        data_form.addRow("Strategy:", self.strategy_combo)

        self.params_group = QGroupBox("Strategy Parameters")
        self.params_form = QFormLayout(self.params_group)
        self._rebuild_param_form(self.strategy_combo.currentText())

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

        account_group = QGroupBox("Account")
        account_form = QFormLayout(account_group)
        account_form.addRow("Balance:", self.balance_spin)
        account_form.addRow(self.spread_data_check)
        account_form.addRow("Fixed spread (pts):", self.spread_spin)
        account_form.addRow("Commission/lot/side:", self.commission_spin)

        self.start_button = QPushButton("▶  Start Replay")
        self.start_button.clicked.connect(self._start)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._reset)
        self.setup_note = QLabel("")
        self.setup_note.setWordWrap(True)
        self.setup_note.setStyleSheet("color: gray;")

        column.addWidget(data_group)
        column.addWidget(self.params_group)
        column.addWidget(account_group)
        column.addWidget(self.start_button)
        column.addWidget(self.reset_button)
        column.addWidget(self.setup_note)
        column.addStretch()
        return panel

    def _build_replay_side(self) -> QVBoxLayout:
        self.play_button = QPushButton("Play")
        self.play_button.setFixedWidth(70)
        self.play_button.clicked.connect(self._toggle_play)
        self.step_button = QPushButton("Step")
        self.step_button.setFixedWidth(60)
        self.step_button.clicked.connect(self._step)
        self.ff_button = QPushButton("To End")
        self.ff_button.setFixedWidth(70)
        self.ff_button.clicked.connect(self._fast_forward)
        self.speed_combo = QComboBox()
        self.speed_combo.addItems([f"{s} bars/s" for s in SPEEDS])
        self.speed_combo.setCurrentIndex(3)  # 10 bars/s
        self.speed_combo.currentIndexChanged.connect(self._on_speed_changed)
        self.follow_check = QCheckBox("Follow")
        self.follow_check.setChecked(True)
        self.follow_check.toggled.connect(self._on_follow_toggled)
        self.progress_label = QLabel("no run")
        for button in (self.play_button, self.step_button, self.ff_button):
            button.setEnabled(False)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.play_button)
        toolbar.addWidget(self.step_button)
        toolbar.addWidget(self.ff_button)
        toolbar.addWidget(self.speed_combo)
        toolbar.addWidget(self.follow_check)
        toolbar.addSpacing(16)
        toolbar.addWidget(self.progress_label)
        toolbar.addStretch()

        self.badge_label = QLabel(" ")
        self.badge_label.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px; padding: 2px;"
        )

        self.chart = ChartWidget()
        self.chart.follow_changed.connect(self.follow_check.setChecked)
        self.trade_layer = TradeLayer(self.chart.plot.getPlotItem())

        self.equity_plot = pg.PlotWidget()
        self.equity_plot.setBackground(BACKGROUND)
        self.equity_plot.setFixedHeight(140)
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
        if self._loaded_key is None and keys:
            self._on_dataset_changed(self.dataset_combo.currentText())

    def showEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        self.refresh_datasets()
        super().showEvent(event)

    def _on_dataset_changed(self, key: str) -> None:
        if not key or key == self._loaded_key:
            return
        symbol, _, timeframe = key.rpartition("_")
        try:
            self._df = self.store.load_bars(symbol, timeframe)
        except (StoreError, ValueError) as exc:
            QMessageBox.warning(self, "Load dataset", str(exc))
            return
        self._loaded_key = key
        self._stop_controller()
        self._clear_run_visuals()
        self.chart.set_data(self._df, title=key.replace("_", " "))
        self.progress_label.setText(f"{len(self._df):,} bars loaded")

    # -------------------------------------------------------------- params

    def _rebuild_param_form(self, strategy_name: str) -> None:
        while self.params_form.rowCount():
            self.params_form.removeRow(0)
        self._param_widgets.clear()
        if strategy_name not in STRATEGIES:
            return
        for name, default in STRATEGIES[strategy_name].params.items():
            if isinstance(default, bool):
                widget = QCheckBox()
                widget.setChecked(default)
            elif isinstance(default, int):
                widget = QSpinBox()
                widget.setRange(1, 100_000)
                widget.setValue(default)
            elif isinstance(default, float):
                widget = QDoubleSpinBox()
                widget.setRange(0.0, 1e9)
                widget.setDecimals(2)
                widget.setSingleStep(0.01 if default < 1 else 1.0)
                widget.setValue(default)
            else:
                continue  # only numeric/bool params are editable for now
            self.params_form.addRow(f"{name}:", widget)
            self._param_widgets[name] = widget

    def _collect_params(self) -> dict:
        values: dict = {}
        for name, widget in self._param_widgets.items():
            if isinstance(widget, QCheckBox):
                values[name] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                values[name] = widget.value()
            else:
                values[name] = float(widget.value())
        return values

    # ----------------------------------------------------------------- run

    def _start(self) -> None:
        if self._df is None or len(self._df) == 0:
            QMessageBox.information(self, "Backtest", "Load a dataset first.")
            return
        self._stop_controller()
        self._clear_run_visuals()

        strategy = STRATEGIES[self.strategy_combo.currentText()](
            **self._collect_params()
        )
        config = BacktestConfig(
            initial_balance=self.balance_spin.value(),
            spread_points=(
                None if self.spread_data_check.isChecked() else self.spread_spin.value()
            ),
            commission_per_lot=self.commission_spin.value(),
            instrument=self._instrument(),
        )
        backtester = Backtester(self._df, strategy, config)

        self.chart.set_data(self._df, title=self._loaded_key.replace("_", " "))
        self.chart.reveal_to(0)
        self.chart.plot.setXRange(0, min(INITIAL_WINDOW, len(self._df)), padding=0.02)
        self.chart.set_follow(self.follow_check.isChecked())

        self._controller = ReplayController(backtester, parent=self)
        self._controller.events_batch.connect(self._on_events)
        self._controller.progress.connect(self._on_progress)
        self._controller.finished.connect(self._on_finished)
        self._controller.state_changed.connect(
            lambda playing: self.play_button.setText("Pause" if playing else "Play")
        )
        self._on_speed_changed(self.speed_combo.currentIndex())

        for button in (self.play_button, self.step_button, self.ff_button):
            button.setEnabled(True)
        self.badge_label.setText(" ")
        self._controller.play()

    def _instrument(self) -> InstrumentSpec:
        symbol, _, timeframe = (self._loaded_key or "_").rpartition("_")
        info = self.store.get(symbol, timeframe) if symbol else None
        if info is not None and info.point and info.contract_size:
            self.setup_note.setText("")
            return InstrumentSpec.from_meta(
                symbol, info.point, info.digits or 5, info.contract_size
            )
        self.setup_note.setText(
            "No stored contract spec for this dataset — assuming a 5-digit "
            "forex pair. Re-download the data to capture the broker's spec."
        )
        return InstrumentSpec.forex_major(symbol or "FX")

    # ------------------------------------------------------ replay wiring

    def _on_events(self, events: list) -> None:
        last_bar = -1
        balance = equity = None
        for event in events:
            if isinstance(event, BarEvent):
                last_bar = max(last_bar, event.index)
            elif isinstance(event, EquityEvent):
                self._equity_x.append(event.index)
                self._equity_balance.append(event.balance)
                self._equity_equity.append(event.equity)
                balance, equity = event.balance, event.equity
            else:
                self.trade_layer.handle(event)
        if last_bar >= 0:
            self.chart.reveal_to(last_bar + 1)
        if balance is not None:
            self._balance_curve.setData(self._equity_x, self._equity_balance)
            self._equity_curve.setData(self._equity_x, self._equity_equity)
            floating = equity - balance
            self.badge_label.setText(
                f"Balance {balance:,.2f}   Equity {equity:,.2f}   "
                f"Floating {floating:+,.2f}   "
                f"Open {self.trade_layer.open_count}   "
                f"Closed {self.trade_layer.closed_count}"
            )

    def _on_progress(self, done: int, total: int) -> None:
        self.progress_label.setText(f"Bar {done:,} / {total:,}")

    def _on_finished(self, result) -> None:
        self.result = result
        stats = result.stats
        self.progress_label.setText(
            f"Finished — {stats['trades']} trades, "
            f"net {stats['net_profit']:+,.2f} "
            f"({stats['return_pct']:+.2f}%), "
            f"PF {stats['profit_factor']:.2f}, "
            f"max DD {stats['max_drawdown_pct']:.1f}%"
        )
        self.play_button.setText("Play")
        self.play_button.setEnabled(False)
        self.step_button.setEnabled(False)
        self.ff_button.setEnabled(False)

    # ------------------------------------------------------------ controls

    def _toggle_play(self) -> None:
        if self._controller is not None:
            self._controller.toggle()

    def _step(self) -> None:
        if self._controller is not None:
            self._controller.pause()
            self._controller.step()

    def _fast_forward(self) -> None:
        if self._controller is not None:
            self._controller.fast_forward()

    def _on_speed_changed(self, index: int) -> None:
        if self._controller is not None and 0 <= index < len(SPEEDS):
            self._controller.set_speed(SPEEDS[index])

    def _on_follow_toggled(self, checked: bool) -> None:
        self.chart.set_follow(checked)

    def _reset(self) -> None:
        self._stop_controller()
        self._clear_run_visuals()
        if self._df is not None:
            self.chart.set_data(self._df, title=(self._loaded_key or "").replace("_", " "))
            self.progress_label.setText(f"{len(self._df):,} bars loaded")

    # ----------------------------------------------------------- lifecycle

    def _stop_controller(self) -> None:
        if self._controller is not None:
            self._controller.pause()
            self._controller.deleteLater()
            self._controller = None
        for button in (self.play_button, self.step_button, self.ff_button):
            button.setEnabled(False)
        self.play_button.setText("Play")

    def _clear_run_visuals(self) -> None:
        self.trade_layer.clear()
        self._equity_x.clear()
        self._equity_balance.clear()
        self._equity_equity.clear()
        self._balance_curve.setData([], [])
        self._equity_curve.setData([], [])
        self.badge_label.setText(" ")
        self.result = None
