"""Results tab: performance summary, sortable trade list, and exports.

Double-clicking a trade emits ``trade_selected`` so the main window can jump
the Backtest chart to that trade.
"""

from __future__ import annotations

import pandas as pd
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from backtester.engine.backtester import BacktestResult
from backtester.engine.stats import format_stats

WIN_COLOR = QColor("#26a69a")
LOSS_COLOR = QColor("#ef5350")

COLUMNS = [
    "#", "Dir", "Lots", "Entry time", "Entry", "Exit time", "Exit",
    "Duration", "Pips", "Net", "Comm", "Swap", "Reason",
]


class NumericItem(QTableWidgetItem):
    """Table item that sorts by a numeric key instead of its display text."""

    def __init__(self, text: str, value: float):
        super().__init__(text)
        # float(): numpy scalars would make __lt__ return numpy.bool, which
        # PySide6's C++ override glue cannot convert back to a C++ bool.
        self.sort_value = float(value)

    def __lt__(self, other):
        if isinstance(other, NumericItem):
            return bool(self.sort_value < other.sort_value)
        return super().__lt__(other)


class ResultsTab(QWidget):
    trade_selected = Signal(object)  # Trade

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._result: BacktestResult | None = None
        self._title = ""

        self.context_label = QLabel("Run a backtest to see results here.")
        self.context_label.setWordWrap(True)
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 12px;"
        )
        self.stats_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        export_trades_button = QPushButton("Export trades CSV…")
        export_trades_button.clicked.connect(self._export_trades_dialog)
        export_summary_button = QPushButton("Export summary…")
        export_summary_button.clicked.connect(self._export_summary_dialog)

        summary_group = QGroupBox("Summary")
        summary_layout = QVBoxLayout(summary_group)
        summary_layout.addWidget(self.context_label)
        summary_layout.addWidget(self.stats_label)
        summary_layout.addWidget(export_trades_button)
        summary_layout.addWidget(export_summary_button)
        summary_layout.addStretch()

        left = QWidget()
        left.setFixedWidth(320)
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(summary_group)

        self.table = QTableWidget(0, len(COLUMNS))
        self.table.setHorizontalHeaderLabels(COLUMNS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.itemDoubleClicked.connect(self._on_double_clicked)

        hint = QLabel("Double-click a trade to see it on the chart.")
        hint.setStyleSheet("color: gray;")
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.table)
        right_layout.addWidget(hint)

        layout = QHBoxLayout(self)
        layout.addWidget(left)
        layout.addLayout(right_layout, stretch=1)

    # ------------------------------------------------------------- populate

    def show_result(self, result: BacktestResult, title: str) -> None:
        self._result = result
        self._title = title
        self.context_label.setText(title)
        self.stats_label.setText(format_stats(result.stats))

        pip = None
        if result.config is not None:
            pip = result.config.instrument.pip

        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(result.trades))
        for row, trade in enumerate(result.trades):
            entry_time = pd.Timestamp(trade.entry_time)
            exit_time = pd.Timestamp(trade.exit_time)
            duration = exit_time - entry_time
            pips = (
                trade.direction * (trade.exit_price - trade.entry_price) / pip
                if pip else 0.0
            )
            direction = "buy" if trade.direction > 0 else "sell"

            items = [
                NumericItem(str(trade.id), trade.id),
                QTableWidgetItem(direction),
                NumericItem(f"{trade.lots:g}", trade.lots),
                NumericItem(f"{entry_time:%Y-%m-%d %H:%M}", entry_time.value),
                NumericItem(f"{trade.entry_price:g}", trade.entry_price),
                NumericItem(f"{exit_time:%Y-%m-%d %H:%M}", exit_time.value),
                NumericItem(f"{trade.exit_price:g}", trade.exit_price),
                NumericItem(_fmt_duration(duration), duration.value),
                NumericItem(f"{pips:+.1f}" if pip else "-", pips),
                NumericItem(f"{trade.net:+,.2f}", trade.net),
                NumericItem(f"{trade.commission:,.2f}", trade.commission),
                NumericItem(f"{trade.swap:,.2f}", trade.swap),
                QTableWidgetItem(trade.reason.value),
            ]
            direction_brush = QBrush(WIN_COLOR if trade.direction > 0 else LOSS_COLOR)
            items[1].setForeground(direction_brush)
            items[9].setForeground(QBrush(WIN_COLOR if trade.net > 0 else LOSS_COLOR))
            items[0].setData(Qt.ItemDataRole.UserRole, trade)
            for column, item in enumerate(items):
                self.table.setItem(row, column, item)
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()

    # -------------------------------------------------------------- export

    def export_trades_csv(self, path: str) -> None:
        if self._result is None:
            return
        frame = pd.DataFrame(
            [
                {
                    "id": t.id,
                    "direction": "buy" if t.direction > 0 else "sell",
                    "lots": t.lots,
                    "entry_time": t.entry_time,
                    "entry_price": t.entry_price,
                    "exit_time": t.exit_time,
                    "exit_price": t.exit_price,
                    "profit": t.profit,
                    "commission": t.commission,
                    "swap": t.swap,
                    "net": t.net,
                    "reason": t.reason.value,
                    "comment": t.comment,
                }
                for t in self._result.trades
            ]
        )
        frame.to_csv(path, index=False)

    def export_summary(self, path: str) -> None:
        if self._result is None:
            return
        text = f"{self._title}\n\n{format_stats(self._result.stats)}\n"
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(text)

    def _export_trades_dialog(self) -> None:
        if self._result is None:
            QMessageBox.information(self, "Export", "No results to export yet.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export trades", "trades.csv", "CSV files (*.csv)"
        )
        if path:
            self.export_trades_csv(path)

    def _export_summary_dialog(self) -> None:
        if self._result is None:
            QMessageBox.information(self, "Export", "No results to export yet.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export summary", "summary.txt", "Text files (*.txt)"
        )
        if path:
            self.export_summary(path)

    # ------------------------------------------------------------ jumping

    def _on_double_clicked(self, item: QTableWidgetItem) -> None:
        anchor = self.table.item(item.row(), 0)
        trade = anchor.data(Qt.ItemDataRole.UserRole) if anchor else None
        if trade is not None:
            self.trade_selected.emit(trade)


def _fmt_duration(delta: pd.Timedelta) -> str:
    parts = delta.components
    if parts.days:
        return f"{parts.days}d {parts.hours:02}:{parts.minutes:02}"
    return f"{parts.hours:02}:{parts.minutes:02}"
