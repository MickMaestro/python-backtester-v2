"""Backtest tab: configure a run, then watch it replay on the chart.

Left panel: dataset, strategy (parameter form auto-generated from the
strategy's ``params`` declaration), and account settings. Right side: the
replay chart with playback controls, live trade drawing, and an equity
sub-chart synced to the replay clock.
"""

from __future__ import annotations

import pyqtgraph as pg
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QProgressDialog,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from backtester.data.models import Timeframe
from backtester.data.store import DataStore, StoreError
from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.events import BarEvent, EquityEvent
from backtester.engine.instrument import InstrumentSpec
from backtester.engine.trade_log import count_moments, log_run, run_folder_name
from backtester.strategy import loader
from backtester.strategy.manual import ManualStrategy
from backtester.ui.chart.chart_widget import BACKGROUND, ChartWidget
from backtester.ui.chart.replay_controller import ReplayController
from backtester.ui.chart.trade_markers import TradeLayer
from backtester.ui.indicators_dialog import load_selection
from backtester.ui.manual_panel import ManualPanel
from backtester.ui.manual_trader import ManualTrader
from backtester.ui.settings import app_settings, cast_like
from backtester.ui.trade_log import TradeLogDialog, TradeLogSettings

INITIAL_WINDOW = 300
#: Bars played before a manual session hands over, so there is context to trade.
WARMUP_BARS = 100

MODE_STRATEGY = "Strategy replay"
MODE_MANUAL = "Manual trading"


class FastRunWorker(QThread):
    """Runs a backtest to completion off the UI thread, reporting progress."""

    progress = Signal(int, int)
    finished_result = Signal(object)
    failed = Signal(str)

    def __init__(self, backtester: Backtester, parent=None):
        super().__init__(parent)
        self._bt = backtester

    def run(self) -> None:
        total = len(self._bt.df)
        try:
            for event in self._bt.run():
                if isinstance(event, EquityEvent) and event.index % 500 == 0:
                    self.progress.emit(event.index + 1, total)
            self.progress.emit(total, total)
            self.finished_result.emit(self._bt.result())
        except Exception as exc:  # surface engine/strategy errors to the UI
            self.failed.emit(f"{type(exc).__name__}: {exc}")


class BacktestTab(QWidget):
    #: (result, title, switch_to_results) — emitted when any run completes.
    run_completed = Signal(object, str, bool)

    def __init__(self, store: DataStore, parent: QWidget | None = None):
        super().__init__(parent)
        self.store = store
        self._df = None
        self._loaded_key: str | None = None
        self._controller: ReplayController | None = None
        self._fast_worker: FastRunWorker | None = None
        self._backtester: Backtester | None = None
        self._indicators = load_selection()
        self._param_widgets: dict[str, QWidget] = {}
        self._strategies: dict[str, loader.StrategyEntry] = {}
        self._equity_x: list[int] = []
        self._equity_balance: list[float] = []
        self._equity_equity: list[float] = []
        self.result = None

        layout = QHBoxLayout(self)
        layout.addWidget(self._build_setup_panel())
        layout.addLayout(self._build_replay_side(), stretch=1)
        self.reload_strategies()
        self.refresh_datasets()
        self._restore_settings()

    def reload_strategies(self) -> None:
        """(Re)discover built-in and user strategies; hot-reloads .py edits."""
        current = self.strategy_combo.currentText()
        self._strategies, errors = loader.discover()
        self.strategy_combo.blockSignals(True)
        self.strategy_combo.clear()
        self.strategy_combo.addItems(sorted(self._strategies))
        if current in self._strategies:
            self.strategy_combo.setCurrentText(current)
        self.strategy_combo.blockSignals(False)
        self._rebuild_param_form(self.strategy_combo.currentText())
        if errors:
            self.setup_note.setText("Strategy load errors:\n" + "\n".join(errors))

    def _strategy_class(self) -> type | None:
        entry = self._strategies.get(self.strategy_combo.currentText())
        return entry[0] if entry else None

    # ------------------------------------------------------------ UI build

    def _build_setup_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(300)
        column = QVBoxLayout(panel)

        self.dataset_combo = QComboBox()
        self.dataset_combo.currentTextChanged.connect(self._on_dataset_changed)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems([MODE_STRATEGY, MODE_MANUAL])
        self.mode_combo.currentTextChanged.connect(self._on_mode_changed)
        self.mode_combo.setToolTip(
            "Strategy replay: watch a strategy trade.\n"
            "Manual trading: place and manage the trades yourself as it plays."
        )
        self.intrabar_combo = QComboBox()
        self.intrabar_combo.addItem("Off (main TF only)")
        self.intrabar_combo.setToolTip(
            "Resolve SL/TP inside each bar using a finer-timeframe dataset "
            "of the same symbol (download one in the Data Manager)."
        )

        data_group = QGroupBox("Setup")
        data_form = QFormLayout(data_group)
        data_form.addRow("Dataset:", self.dataset_combo)
        data_form.addRow("Mode:", self.mode_combo)
        data_form.addRow("Intrabar:", self.intrabar_combo)

        self.strategy_combo = QComboBox()
        self.strategy_combo.currentTextChanged.connect(self._rebuild_param_form)
        reload_button = QPushButton("Reload strategies")
        reload_button.clicked.connect(self.reload_strategies)
        self.strategy_group = QGroupBox("Strategy")
        strategy_form = QFormLayout(self.strategy_group)
        strategy_form.addRow("Strategy:", self.strategy_combo)
        strategy_form.addRow(reload_button)

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
        self.fast_button = QPushButton("⏩  Run Fast")
        self.fast_button.clicked.connect(self._run_fast)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self._reset)
        self.setup_note = QLabel("")
        self.setup_note.setWordWrap(True)
        self.setup_note.setStyleSheet("color: gray;")

        run_row = QHBoxLayout()
        run_row.addWidget(self.start_button)
        run_row.addWidget(self.fast_button)

        self.manual_panel = ManualPanel()
        self.manual_panel.setVisible(False)

        column.addWidget(data_group)
        column.addWidget(self.strategy_group)
        column.addWidget(self.params_group)
        column.addWidget(account_group)
        column.addLayout(run_row)
        column.addWidget(self.reset_button)
        column.addWidget(self._build_trade_log_row())
        column.addWidget(self.log_note)
        column.addWidget(self.manual_panel)
        column.addWidget(self.setup_note)
        column.addStretch()
        return panel

    def _build_trade_log_row(self) -> QWidget:
        """Log-trade-context toggle plus its settings dialog button."""
        self._log_settings = TradeLogSettings.load()

        self.log_check = QCheckBox("Log trade context data")
        self.log_check.setToolTip(
            "After the run, write the bars and every indicator value around "
            "each trade entry, SL/TP modification, and exit."
        )
        self.log_check.setChecked(self._log_settings.enabled)
        self.log_check.toggled.connect(self._on_trade_log_toggled)
        self.log_button = QPushButton("Trade log…")
        self.log_button.setToolTip("What to log, how much context, folder")
        self.log_button.clicked.connect(self._edit_trade_log_settings)

        self.log_note = QLabel("")
        self.log_note.setWordWrap(True)
        self.log_note.setStyleSheet("color: gray;")

        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.log_check, stretch=1)
        layout.addWidget(self.log_button)
        self.log_row = row
        return row

    # ---------------------------------------------------------------- mode

    @property
    def is_manual(self) -> bool:
        return self.mode_combo.currentText() == MODE_MANUAL

    def _on_mode_changed(self, _mode: str) -> None:
        """Swap the setup panel between picking a strategy and trading by hand."""
        manual = self.is_manual
        self.strategy_group.setVisible(not manual)
        self.params_group.setVisible(not manual)
        self.manual_panel.setVisible(manual)
        # A fast run has nothing to drive in manual mode — you are the strategy.
        self.fast_button.setVisible(not manual)
        # The log documents a strategy's decisions; in manual mode they are
        # yours, and you were there.
        self.log_row.setVisible(not manual)
        self.log_note.setVisible(not manual)
        self.start_button.setText(
            "▶  Start Manual Session" if manual else "▶  Start Replay"
        )
        self._stop_controller()
        self.manual.detach()
        self._clear_run_visuals()
        if self._df is not None:
            self.chart.set_data(
                self._df, title=(self._loaded_key or "").replace("_", " ")
            )
            self.apply_indicators()

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
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 250)
        self.speed_slider.setValue(10)
        self.speed_slider.setFixedWidth(150)
        self.speed_slider.valueChanged.connect(self._on_speed_changed)
        self.speed_label = QLabel("10 bars/s")
        self.follow_check = QCheckBox("Follow")
        self.follow_check.setChecked(True)
        self.follow_check.toggled.connect(self._on_follow_toggled)
        self.shift_check = QCheckBox("Shift")
        self.shift_check.setToolTip("Leave blank space to the right of the newest candle.")
        self.shift_check.toggled.connect(self._on_shift_toggled)
        self.progress_label = QLabel("no run")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(160)
        self.progress_bar.setVisible(False)
        for button in (self.play_button, self.step_button, self.ff_button):
            button.setEnabled(False)

        toolbar = QHBoxLayout()
        toolbar.addWidget(self.play_button)
        toolbar.addWidget(self.step_button)
        toolbar.addWidget(self.ff_button)
        toolbar.addWidget(QLabel("Speed:"))
        toolbar.addWidget(self.speed_slider)
        toolbar.addWidget(self.speed_label)
        toolbar.addWidget(self.follow_check)
        toolbar.addWidget(self.shift_check)
        toolbar.addSpacing(16)
        toolbar.addWidget(self.progress_label)
        toolbar.addWidget(self.progress_bar)
        toolbar.addStretch()

        self.badge_label = QLabel(" ")
        self.badge_label.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px; padding: 2px;"
        )

        self.chart = ChartWidget()
        self.chart.follow_changed.connect(self.follow_check.setChecked)
        self.trade_layer = TradeLayer(self.chart.plot.getPlotItem())
        self.manual = ManualTrader(
            self.chart.plot.getPlotItem(), self.manual_panel, parent=self
        )
        self.manual.warning.connect(
            lambda message: QMessageBox.warning(self, "Order", message)
        )

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
        self._refresh_intrabar_choices()
        self.chart.set_data(self._df, title=key.replace("_", " "))
        self.apply_indicators()
        self.progress_label.setText(f"{len(self._df):,} bars loaded")

    # -------------------------------------------------------------- params

    def _rebuild_param_form(self, strategy_name: str) -> None:
        while self.params_form.rowCount():
            self.params_form.removeRow(0)
        self._param_widgets.clear()
        entry = self._strategies.get(strategy_name)
        if entry is None:
            return
        settings = app_settings()
        for name, default in entry[0].params.items():
            stored = cast_like(
                settings.value(f"params/{strategy_name}/{name}"), default
            )
            if isinstance(default, bool):
                widget = QCheckBox()
                widget.setChecked(stored)
            elif isinstance(default, int):
                widget = QSpinBox()
                widget.setRange(1, 100_000)
                widget.setValue(stored)
            elif isinstance(default, float):
                widget = QDoubleSpinBox()
                widget.setRange(0.0, 1e9)
                widget.setDecimals(2)
                widget.setSingleStep(0.01 if default < 1 else 1.0)
                widget.setValue(stored)
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

    def _make_backtester(self) -> Backtester | None:
        if self._df is None or len(self._df) == 0:
            QMessageBox.information(self, "Backtest", "Load a dataset first.")
            return None
        if self.is_manual:
            strategy = ManualStrategy()  # you place the orders, not a strategy
        else:
            strategy_cls = self._strategy_class()
            if strategy_cls is None:
                QMessageBox.information(self, "Backtest", "Pick a strategy first.")
                return None
            try:
                strategy = strategy_cls(**self._collect_params())
            except ValueError as exc:
                QMessageBox.warning(self, "Backtest", str(exc))
                return None
        config = BacktestConfig(
            initial_balance=self.balance_spin.value(),
            spread_points=(
                None if self.spread_data_check.isChecked() else self.spread_spin.value()
            ),
            commission_per_lot=self.commission_spin.value(),
            instrument=self._instrument(),
        )
        self._save_settings()
        # Kept so the post-run log can read the strategy's indicator series.
        self._backtester = Backtester(
            self._df,
            strategy,
            config,
            intrabar_df=self._intrabar_df(),
            record_events=self._logging_enabled(),
        )
        return self._backtester

    def _intrabar_df(self):
        key = self.intrabar_combo.currentText()
        if self.intrabar_combo.currentIndex() <= 0 or not key:
            return None
        symbol, _, timeframe = key.rpartition("_")
        try:
            return self.store.load_bars(symbol, timeframe)
        except (StoreError, ValueError):
            return None

    def _refresh_intrabar_choices(self) -> None:
        """Offer finer-timeframe datasets of the loaded symbol."""
        current = self.intrabar_combo.currentText()
        self.intrabar_combo.blockSignals(True)
        self.intrabar_combo.clear()
        self.intrabar_combo.addItem("Off (main TF only)")
        if self._loaded_key:
            symbol, _, timeframe = self._loaded_key.rpartition("_")
            try:
                main_seconds = Timeframe(timeframe).seconds
            except ValueError:
                main_seconds = 0
            for info in self.store.datasets():
                if info.symbol != symbol or info.key == self._loaded_key:
                    continue
                if Timeframe(info.timeframe).seconds < main_seconds:
                    self.intrabar_combo.addItem(info.key)
        if self.intrabar_combo.findText(current) >= 0:
            self.intrabar_combo.setCurrentText(current)
        self.intrabar_combo.blockSignals(False)

    def _run_title(self) -> str:
        dataset = (self._loaded_key or "").replace("_", " ")
        if self.is_manual:
            return f"{dataset} — manual session"
        return (
            f"{dataset} — {self.strategy_combo.currentText()} {self._collect_params()}"
        )

    def _start(self) -> None:
        backtester = self._make_backtester()
        if backtester is None:
            return
        self._stop_controller()
        self._clear_run_visuals()

        self.chart.set_data(self._df, title=self._loaded_key.replace("_", " "))
        self.apply_indicators()
        self.chart.reveal_to(0)
        self.chart.plot.setXRange(0, min(INITIAL_WINDOW, len(self._df)), padding=0.02)
        self.chart.set_follow(self.follow_check.isChecked())
        self.chart.set_shift(self.shift_check.isChecked())

        self._controller = ReplayController(backtester, parent=self)
        self._controller.events_batch.connect(self._on_events)
        self._controller.progress.connect(self._on_progress)
        self._controller.finished.connect(self._on_finished)
        self._controller.state_changed.connect(
            lambda playing: self.play_button.setText("Pause" if playing else "Play")
        )
        self._on_speed_changed(self.speed_slider.value())

        for button in (self.play_button, self.step_button, self.ff_button):
            button.setEnabled(True)
        self.badge_label.setText(" ")

        if self.is_manual:
            # Play a warm-up so there is price history to trade from, then hand
            # over paused — the trader decides when to advance.
            self.manual.attach(backtester.broker, self._instrument(), self._df)
            self._controller.advance(min(WARMUP_BARS, len(self._df) // 2))
            self.chart.set_follow(self.follow_check.isChecked())
        else:
            self._controller.play()

    def _run_fast(self) -> None:
        backtester = self._make_backtester()
        if backtester is None:
            return
        self._stop_controller()
        self._clear_run_visuals()

        self.progress_bar.setRange(0, len(self._df))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.progress_label.setText("Running…")
        for button in (self.start_button, self.fast_button, self.reset_button):
            button.setEnabled(False)

        # No parent: the worker is owned solely via self._fast_worker and
        # released with deleteLater(). Parenting it to the tab as well would
        # let the tab's destructor delete it out from under a still-queued
        # deleteLater event, crashing a later event loop.
        self._fast_worker = FastRunWorker(backtester)
        self._fast_worker.progress.connect(
            lambda done, total: self.progress_bar.setValue(done)
        )
        self._fast_worker.finished_result.connect(self._on_fast_finished)
        self._fast_worker.failed.connect(self._on_fast_failed)
        self._fast_worker.start()

    def _on_fast_finished(self, result) -> None:
        self.result = result
        self._finish_fast_ui()
        self.chart.set_data(self._df, title=(self._loaded_key or "").replace("_", " "))
        self.apply_indicators()
        self.trade_layer.load_trades(result.trades)
        self._equity_x = list(range(len(result.equity)))
        self._equity_balance = result.equity["balance"].tolist()
        self._equity_equity = result.equity["equity"].tolist()
        self._balance_curve.setData(self._equity_x, self._equity_balance)
        self._equity_curve.setData(self._equity_x, self._equity_equity)
        self.badge_label.setText(
            f"Balance {result.final_balance:,.2f}   Equity {result.final_balance:,.2f}   "
            f"Floating +0.00   Open 0   Closed {len(result.trades)}"
        )
        self._show_summary(result)
        self.run_completed.emit(result, self._run_title(), True)
        self._write_trade_log(result)

    def _on_fast_failed(self, message: str) -> None:
        self._finish_fast_ui()
        self.progress_label.setText("Run failed")
        QMessageBox.warning(self, "Backtest failed", message)

    def _finish_fast_ui(self) -> None:
        self.progress_bar.setVisible(False)
        for button in (self.start_button, self.fast_button, self.reset_button):
            button.setEnabled(True)
        if self._fast_worker is not None:
            # Join before releasing (see OptimizerTab._finish_ui).
            self._fast_worker.wait()
            self._fast_worker.deleteLater()
            self._fast_worker = None

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
        last_close = None
        balance = equity = None
        for event in events:
            if isinstance(event, BarEvent):
                last_bar = max(last_bar, event.index)
                last_close = event.close
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
        if self.manual.active and last_close is not None:
            self.manual.on_bars_advanced(last_bar, last_close)

    def _on_progress(self, done: int, total: int) -> None:
        self.progress_label.setText(f"Bar {done:,} / {total:,}")

    def _on_finished(self, result) -> None:
        self.result = result
        self.manual.detach()  # session over — no more orders
        self._show_summary(result)
        self.play_button.setText("Play")
        self.play_button.setEnabled(False)
        self.step_button.setEnabled(False)
        self.ff_button.setEnabled(False)
        self.run_completed.emit(result, self._run_title(), False)
        self._write_trade_log(result)

    def _show_summary(self, result) -> None:
        stats = result.stats
        self.progress_label.setText(
            f"Finished — {stats['trades']} trades, "
            f"net {stats['net_profit']:+,.2f} "
            f"({stats['return_pct']:+.2f}%), "
            f"PF {stats['profit_factor']:.2f}, "
            f"max DD {stats['max_drawdown_pct']:.1f}%"
        )

    # --------------------------------------------------------- indicators

    def apply_indicators(self) -> None:
        """Draw the app-wide indicator selection on the replay chart."""
        errors = self.chart.set_indicators(self._indicators)
        if errors:
            self.setup_note.setText("Indicator errors:\n" + "\n".join(errors))

    def set_indicators(self, indicators: list) -> None:
        self._indicators = list(indicators)
        self.apply_indicators()

    # ---------------------------------------------------------- trade log

    def _logging_enabled(self) -> bool:
        # Manual sessions log nothing: the decisions were yours, not a
        # strategy's, and there are no indicator series behind them.
        return self.log_check.isChecked() and not self.is_manual

    def _on_trade_log_toggled(self, checked: bool) -> None:
        self._log_settings.enabled = checked
        self._log_settings.save()
        if checked:
            self.log_note.setText("")

    def _edit_trade_log_settings(self) -> None:
        result = TradeLogDialog.edit(self, self._log_settings)
        if result is None:
            return
        self._log_settings = result
        self._log_settings.save()

    def _write_trade_log(self, result) -> None:
        """Post-run pass: bars + indicator values per trade moment.

        See ``engine/trade_log.py`` — the writing is Qt-free; this only supplies
        the folder and a cancellable progress dialog.
        """
        if not self._logging_enabled() or self._df is None:
            return
        if self._backtester is None:
            return
        settings = self._log_settings
        spec = settings.spec
        events = getattr(result, "events", [])
        planned = count_moments(events, spec)
        if planned == 0:
            self.log_note.setText(
                "Trade log: nothing to log (no trades, or no moments selected)."
            )
            return
        if spec.max_moments > 0:
            planned = min(planned, spec.max_moments)

        folder = settings.directory() / run_folder_name(
            self._loaded_key or "run", self.strategy_combo.currentText()
        )
        dialog = QProgressDialog(
            f"Logging {planned:,} trade moments…", "Cancel", 0, planned, self
        )
        dialog.setWindowTitle("Trade log")
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        dialog.setMinimumDuration(0)
        dialog.setValue(0)
        try:
            report = log_run(
                self._df,
                result,
                self._backtester.strategy,
                folder,
                spec,
                progress=lambda done, _total: dialog.setValue(done),
                should_cancel=dialog.wasCanceled,
            )
        except (OSError, ValueError) as exc:
            self.log_note.setText("Trade log: failed.")
            QMessageBox.warning(self, "Trade log", str(exc))
            return
        finally:
            dialog.close()
        self.log_note.setText(report.message())
        self.log_note.setToolTip(str(report.folder))

    def apply_external_params(self, strategy_name: str, params: dict) -> None:
        """Adopt a strategy + parameter set (from the Optimizer tab)."""
        if self.strategy_combo.findText(strategy_name) < 0:
            return
        self.strategy_combo.setCurrentText(strategy_name)
        for name, value in params.items():
            widget = self._param_widgets.get(name)
            if isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.setValue(value)

    def focus_trade(self, trade) -> None:
        """Zoom the chart to a trade's entry→exit region (Results tab jump)."""
        if self._df is None:
            return
        self.follow_check.setChecked(False)
        n = len(self._df)
        span = max(trade.exit_index - trade.entry_index, 5)
        margin = max(10, span)
        self.chart.plot.setXRange(
            max(0, trade.entry_index - margin),
            min(n, trade.exit_index + margin),
            padding=0.05,
        )

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

    def _on_speed_changed(self, value: int) -> None:
        self.speed_label.setText(f"{value} bars/s")
        if self._controller is not None:
            self._controller.set_speed(float(value))

    def _on_follow_toggled(self, checked: bool) -> None:
        self.chart.set_follow(checked)

    def _on_shift_toggled(self, checked: bool) -> None:
        self.chart.set_shift(checked)

    def _reset(self) -> None:
        self._stop_controller()
        self.manual.detach()
        self._clear_run_visuals()
        if self._df is not None:
            self.chart.set_data(self._df, title=(self._loaded_key or "").replace("_", " "))
            self.apply_indicators()
            self.progress_label.setText(f"{len(self._df):,} bars loaded")

    # ------------------------------------------------------------ settings

    def _save_settings(self) -> None:
        settings = app_settings()
        settings.setValue("backtest/dataset", self.dataset_combo.currentText())
        settings.setValue("backtest/strategy", self.strategy_combo.currentText())
        settings.setValue("backtest/balance", self.balance_spin.value())
        settings.setValue(
            "backtest/spread_from_data", self.spread_data_check.isChecked()
        )
        settings.setValue("backtest/spread", self.spread_spin.value())
        settings.setValue("backtest/commission", self.commission_spin.value())
        settings.setValue("backtest/speed", self.speed_slider.value())
        settings.setValue("backtest/mode", self.mode_combo.currentText())
        settings.setValue("backtest/shift", self.shift_check.isChecked())
        strategy = self.strategy_combo.currentText()
        for name, value in self._collect_params().items():
            settings.setValue(f"params/{strategy}/{name}", value)

    def _restore_settings(self) -> None:
        settings = app_settings()
        dataset = str(settings.value("backtest/dataset", "") or "")
        if dataset and self.dataset_combo.findText(dataset) >= 0:
            self.dataset_combo.setCurrentText(dataset)
        strategy = str(settings.value("backtest/strategy", "") or "")
        if strategy and self.strategy_combo.findText(strategy) >= 0:
            self.strategy_combo.setCurrentText(strategy)
        self._rebuild_param_form(self.strategy_combo.currentText())
        self.balance_spin.setValue(
            cast_like(settings.value("backtest/balance"), 10_000.0)
        )
        self.spread_data_check.setChecked(
            cast_like(settings.value("backtest/spread_from_data"), True)
        )
        self.spread_spin.setValue(cast_like(settings.value("backtest/spread"), 10))
        self.commission_spin.setValue(
            cast_like(settings.value("backtest/commission"), 0.0)
        )
        speed = cast_like(settings.value("backtest/speed"), 10)
        if self.speed_slider.minimum() <= speed <= self.speed_slider.maximum():
            self.speed_slider.setValue(speed)
        mode = str(settings.value("backtest/mode", "") or "")
        if mode and self.mode_combo.findText(mode) >= 0:
            self.mode_combo.setCurrentText(mode)
        self.shift_check.setChecked(cast_like(settings.value("backtest/shift"), False))

    # ----------------------------------------------------------- lifecycle

    def shutdown(self) -> None:
        self._stop_controller()
        if self._fast_worker is not None and self._fast_worker.isRunning():
            self._fast_worker.wait(5_000)

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
