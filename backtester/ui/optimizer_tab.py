"""Optimizer tab: grid-search a strategy's parameters across CPU cores.

Check the parameters to sweep and give each a From/To/Step; unchecked
parameters stay fixed at their shown value. Results land in a sortable
table; double-click a row to send those parameters to the Backtest tab.
Account settings (balance/spread/commission) are taken from the Backtest
tab's last-used values.
"""

from __future__ import annotations

import os

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from backtester.data.store import DataStore, StoreError
from backtester.engine.backtester import BacktestConfig
from backtester.engine.instrument import InstrumentSpec
from backtester.engine.optimizer import build_grid, optimize, steps
from backtester.strategy import loader
from backtester.ui.results_tab import NumericItem
from backtester.ui.settings import app_settings, cast_like

METRICS = {
    "Net profit": "net_profit",
    "Profit factor": "profit_factor",
    "Expectancy": "expectancy",
    "Win rate": "win_rate",
    "Sharpe": "sharpe",
    "Max drawdown %": "max_drawdown_pct",  # lower is better; sort ascending
}
STAT_COLUMNS = [
    ("Net", "net_profit", "{:+,.2f}"),
    ("PF", "profit_factor", "{:.2f}"),
    ("Trades", "trades", "{:d}"),
    ("Win %", "win_rate", "{:.1%}"),
    ("Max DD %", "max_drawdown_pct", "{:.1f}"),
    ("Sharpe", "sharpe", "{:.2f}"),
]
MAX_COMBINATIONS = 5_000


class OptimizeWorker(QThread):
    progress = Signal(int, int)
    finished_results = Signal(list)
    failed = Signal(str)

    def __init__(self, df, strategy_spec, grid, config, workers, intrabar_df, parent=None):
        super().__init__(parent)
        self._args = (df, strategy_spec, grid, config, workers, intrabar_df)
        self._stop = False

    def stop(self) -> None:
        self._stop = True

    def run(self) -> None:
        df, spec, grid, config, workers, intrabar_df = self._args
        try:
            results = optimize(
                df, spec, grid, config,
                workers=workers, intrabar_df=intrabar_df,
                progress=lambda done, total: self.progress.emit(done, total),
                should_stop=lambda: self._stop,
            )
            self.finished_results.emit(results)
        except Exception as exc:
            self.failed.emit(f"{type(exc).__name__}: {exc}")


class ParamRow:
    """One sweep row: enable-checkbox + from/to/step spin boxes."""

    def __init__(self, name: str, default, grid: QGridLayout, row: int):
        self.name = name
        self.default = default
        self.is_int = isinstance(default, int) and not isinstance(default, bool)
        self.check = QCheckBox(name)

        def make_spin(value):
            if self.is_int:
                spin = QSpinBox()
                spin.setRange(1, 100_000)
                spin.setValue(int(value))
            else:
                spin = QDoubleSpinBox()
                spin.setRange(0.0, 1e9)
                spin.setDecimals(2)
                spin.setSingleStep(0.01 if default < 1 else 1.0)
                spin.setValue(float(value))
            return spin

        self.from_spin = make_spin(default)
        self.to_spin = make_spin(default)
        self.step_spin = make_spin(1 if self.is_int else max(default / 4, 0.01))
        for widget in (self.from_spin, self.to_spin, self.step_spin):
            widget.setEnabled(False)
        self.check.toggled.connect(
            lambda on: [w.setEnabled(on) for w in
                        (self.from_spin, self.to_spin, self.step_spin)]
        )
        grid.addWidget(self.check, row, 0)
        grid.addWidget(self.from_spin, row, 1)
        grid.addWidget(self.to_spin, row, 2)
        grid.addWidget(self.step_spin, row, 3)

    def values(self) -> list:
        if not self.check.isChecked():
            return [self.default if not self.is_int else int(self.default)]
        return steps(
            self.from_spin.value(), self.to_spin.value(),
            max(self.step_spin.value(), 1e-9), as_int=self.is_int,
        )


class OptimizerTab(QWidget):
    #: (strategy_name, params) — user picked a result to run in Backtest.
    params_chosen = Signal(str, dict)

    def __init__(self, store: DataStore, parent: QWidget | None = None):
        super().__init__(parent)
        self.store = store
        self._strategies: dict[str, loader.StrategyEntry] = {}
        self._param_rows: list[ParamRow] = []
        self._worker: OptimizeWorker | None = None
        self._results: list = []

        self.dataset_combo = QComboBox()
        self.strategy_combo = QComboBox()
        self.strategy_combo.currentTextChanged.connect(self._rebuild_param_rows)
        self.metric_combo = QComboBox()
        self.metric_combo.addItems(list(METRICS))
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(0, 64)
        self.workers_spin.setValue(max(1, (os.cpu_count() or 2) - 1))
        self.workers_spin.setToolTip("Parallel processes; 0 = run in-process")

        top_form = QGridLayout()
        top_form.addWidget(QLabel("Dataset:"), 0, 0)
        top_form.addWidget(self.dataset_combo, 0, 1)
        top_form.addWidget(QLabel("Strategy:"), 0, 2)
        top_form.addWidget(self.strategy_combo, 0, 3)
        top_form.addWidget(QLabel("Rank by:"), 1, 0)
        top_form.addWidget(self.metric_combo, 1, 1)
        top_form.addWidget(QLabel("Workers:"), 1, 2)
        top_form.addWidget(self.workers_spin, 1, 3)

        self.params_group = QGroupBox("Parameter sweep (checked = sweep From→To by Step)")
        self.params_grid = QGridLayout(self.params_group)

        self.run_button = QPushButton("Run Optimization")
        self.run_button.clicked.connect(self._run)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self._stop)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_label = QLabel("")

        controls = QHBoxLayout()
        controls.addWidget(self.run_button)
        controls.addWidget(self.stop_button)
        controls.addWidget(self.progress_bar)
        controls.addWidget(self.status_label)
        controls.addStretch()

        self.table = QTableWidget(0, 0)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemDoubleClicked.connect(self._on_double_clicked)

        hint = QLabel("Double-click a row to load its parameters into the Backtest tab.")
        hint.setStyleSheet("color: gray;")

        layout = QVBoxLayout(self)
        layout.addLayout(top_form)
        layout.addWidget(self.params_group)
        layout.addLayout(controls)
        layout.addWidget(self.table, stretch=1)
        layout.addWidget(hint)

        self.reload_strategies()
        self.refresh_datasets()

    # ----------------------------------------------------------- populate

    def reload_strategies(self) -> None:
        current = self.strategy_combo.currentText()
        self._strategies, _ = loader.discover()
        self.strategy_combo.blockSignals(True)
        self.strategy_combo.clear()
        self.strategy_combo.addItems(sorted(self._strategies))
        if current in self._strategies:
            self.strategy_combo.setCurrentText(current)
        self.strategy_combo.blockSignals(False)
        self._rebuild_param_rows(self.strategy_combo.currentText())

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

    def _rebuild_param_rows(self, strategy_name: str) -> None:
        while self.params_grid.count():
            item = self.params_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._param_rows.clear()
        entry = self._strategies.get(strategy_name)
        if entry is None:
            return
        self.params_grid.addWidget(QLabel("Sweep"), 0, 0)
        self.params_grid.addWidget(QLabel("From"), 0, 1)
        self.params_grid.addWidget(QLabel("To"), 0, 2)
        self.params_grid.addWidget(QLabel("Step"), 0, 3)
        for row, (name, default) in enumerate(entry[0].params.items(), start=1):
            if isinstance(default, bool) or not isinstance(default, (int, float)):
                continue
            self._param_rows.append(ParamRow(name, default, self.params_grid, row))

    # ---------------------------------------------------------------- run

    def _run(self) -> None:
        key = self.dataset_combo.currentText()
        entry = self._strategies.get(self.strategy_combo.currentText())
        if not key or entry is None:
            QMessageBox.information(self, "Optimizer", "Pick a dataset and strategy.")
            return
        symbol, _, timeframe = key.rpartition("_")
        try:
            df = self.store.load_bars(symbol, timeframe)
        except (StoreError, ValueError) as exc:
            QMessageBox.warning(self, "Optimizer", str(exc))
            return

        ranges = {row.name: row.values() for row in self._param_rows}
        grid = build_grid(ranges)
        if len(grid) < 2:
            QMessageBox.information(
                self, "Optimizer", "Check at least one parameter to sweep."
            )
            return
        if len(grid) > MAX_COMBINATIONS:
            QMessageBox.warning(
                self, "Optimizer",
                f"{len(grid):,} combinations exceeds the limit of "
                f"{MAX_COMBINATIONS:,}. Increase the steps.",
            )
            return

        settings = app_settings()
        config = BacktestConfig(
            initial_balance=cast_like(settings.value("backtest/balance"), 10_000.0),
            spread_points=(
                None
                if cast_like(settings.value("backtest/spread_from_data"), True)
                else cast_like(settings.value("backtest/spread"), 10)
            ),
            commission_per_lot=cast_like(settings.value("backtest/commission"), 0.0),
            instrument=self._instrument(symbol, timeframe),
        )

        self._results = []
        self.table.setRowCount(0)
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setRange(0, len(grid))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_label.setText(f"{len(grid):,} combinations…")

        # No parent: owned via self._worker and released with deleteLater()
        # (see the note in BacktestTab._run_fast).
        self._worker = OptimizeWorker(
            df, entry[1], grid, config, self.workers_spin.value(), None
        )
        self._worker.progress.connect(
            lambda done, total: self.progress_bar.setValue(done)
        )
        self._worker.finished_results.connect(self._on_finished)
        self._worker.failed.connect(self._on_failed)
        self._worker.start()

    def _instrument(self, symbol: str, timeframe: str) -> InstrumentSpec:
        info = self.store.get(symbol, timeframe)
        if info is not None and info.point and info.contract_size:
            return InstrumentSpec.from_meta(
                symbol, info.point, info.digits or 5, info.contract_size
            )
        return InstrumentSpec.forex_major(symbol)

    def _stop(self) -> None:
        if self._worker is not None:
            self._worker.stop()
            self.status_label.setText("Stopping…")

    def _on_failed(self, message: str) -> None:
        self._finish_ui()
        QMessageBox.warning(self, "Optimization failed", message)

    def _on_finished(self, results: list) -> None:
        self._finish_ui()
        self._results = results
        errors = [r for r in results if r.error]
        metric = METRICS[self.metric_combo.currentText()]
        ranked = sorted(
            (r for r in results if not r.error),
            key=lambda r: r.stats.get(metric, 0.0),
            reverse=metric != "max_drawdown_pct",
        )
        self._populate_table(ranked)
        message = f"{len(ranked):,} results"
        if errors:
            message += f", {len(errors)} failed ({errors[0].error})"
        self.status_label.setText(message)

    def _finish_ui(self) -> None:
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress_bar.setVisible(False)
        if self._worker is not None:
            # Join the thread before releasing it — deleting a QThread whose
            # run() hasn't fully returned aborts the process ("QThread:
            # Destroyed while thread is still running").
            self._worker.wait()
            self._worker.deleteLater()
            self._worker = None

    # -------------------------------------------------------------- table

    def _populate_table(self, ranked: list) -> None:
        if not ranked:
            self.table.setRowCount(0)
            return
        param_names = list(ranked[0].params)
        headers = param_names + [name for name, _, _ in STAT_COLUMNS]
        self.table.setSortingEnabled(False)
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(ranked))
        for row, result in enumerate(ranked):
            items = []
            for name in param_names:
                value = result.params[name]
                items.append(NumericItem(f"{value:g}", value))
            for _, stat_key, fmt in STAT_COLUMNS:
                value = result.stats.get(stat_key, 0.0)
                if value in (float("inf"), float("-inf")):
                    items.append(NumericItem("∞", 1e18))
                else:
                    items.append(NumericItem(fmt.format(value), float(value)))
            items[0].setData(Qt.ItemDataRole.UserRole, result)
            for column, item in enumerate(items):
                self.table.setItem(row, column, item)
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()

    def _on_double_clicked(self, item: QTableWidgetItem) -> None:
        anchor = self.table.item(item.row(), 0)
        result = anchor.data(Qt.ItemDataRole.UserRole) if anchor else None
        if result is not None:
            self.params_chosen.emit(self.strategy_combo.currentText(), result.params)

    # ----------------------------------------------------------- lifecycle

    def shutdown(self) -> None:
        if self._worker is not None:
            self._worker.stop()
            self._worker.wait(10_000)
