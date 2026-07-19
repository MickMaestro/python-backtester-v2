"""Data Manager tab: MT5 connection, bar download, and the local data library."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QDate, Qt, QThread, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QCompleter,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from backtester.data.models import DatasetInfo, Timeframe
from backtester.data.mt5_client import MT5Client, MT5Error
from backtester.data.store import DataStore, StoreError


class DownloadWorker(QThread):
    """Runs an MT5 download + store save off the UI thread."""

    done = Signal(object)  # DatasetInfo
    failed = Signal(str)

    def __init__(
        self,
        client: MT5Client,
        store: DataStore,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._client = client
        self._store = store
        self._symbol = symbol
        self._timeframe = timeframe
        self._start = start
        self._end = end

    def run(self) -> None:
        try:
            df = self._client.download_bars(
                self._symbol, self._timeframe, self._start, self._end
            )
            spec = self._client.symbol_spec(self._symbol)
            info = self._store.save_bars(
                self._symbol, self._timeframe, df, source="MT5", spec=spec
            )
        except (MT5Error, StoreError) as exc:
            self.failed.emit(str(exc))
        except Exception as exc:  # keep the UI alive on unexpected errors
            self.failed.emit(f"Unexpected error: {exc!r}")
        else:
            self.done.emit(info)


class ImportDialog(QDialog):
    """Asks which symbol/timeframe an imported CSV belongs to."""

    def __init__(self, default_symbol: str, default_tf: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Import CSV")

        self.symbol_edit = QLineEdit(default_symbol)
        self.tf_combo = QComboBox()
        self.tf_combo.addItems([tf.value for tf in Timeframe])
        self.tf_combo.setCurrentText(default_tf)

        form = QFormLayout()
        form.addRow("Symbol:", self.symbol_edit)
        form.addRow("Timeframe:", self.tf_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    @staticmethod
    def get(parent: QWidget, filename: str) -> tuple[str, str] | None:
        symbol, tf = _guess_from_filename(filename)
        dialog = ImportDialog(symbol, tf, parent)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        return dialog.symbol_edit.text().strip().upper(), dialog.tf_combo.currentText()


def _guess_from_filename(filename: str) -> tuple[str, str]:
    """Guess symbol/timeframe from names like ``EURUSD_H1.csv``."""
    tokens = Path(filename).stem.replace("-", "_").split("_")
    tf_names = {tf.value for tf in Timeframe}
    timeframe = next((t.upper() for t in tokens if t.upper() in tf_names), "H1")
    symbol = tokens[0].upper() if tokens and tokens[0] else ""
    return symbol, timeframe


class DataTab(QWidget):
    #: Emitted whenever the local library contents change (download/import/delete).
    datasets_changed = Signal()

    def __init__(self, store: DataStore | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.client = MT5Client()
        self.store = store if store is not None else DataStore()
        self._worker: DownloadWorker | None = None

        layout = QHBoxLayout(self)
        layout.addWidget(self._build_left_panel())
        layout.addWidget(self._build_library_panel(), stretch=1)

        self._refresh_table()

    # ------------------------------------------------------------ UI build

    def _build_left_panel(self) -> QWidget:
        panel = QWidget()
        panel.setFixedWidth(340)
        column = QVBoxLayout(panel)

        # --- connection group
        self.connect_button = QPushButton("Connect to MT5")
        self.connect_button.clicked.connect(self._toggle_connection)
        self.connection_label = QLabel("Not connected.")
        self.connection_label.setWordWrap(True)

        conn_group = QGroupBox("MT5 Connection")
        conn_layout = QVBoxLayout(conn_group)
        conn_layout.addWidget(self.connect_button)
        conn_layout.addWidget(self.connection_label)

        # --- download group
        self.symbol_combo = QComboBox()
        self.symbol_combo.setEditable(True)
        self.symbol_combo.lineEdit().setPlaceholderText("e.g. EURUSD")

        self.tf_combo = QComboBox()
        self.tf_combo.addItems([tf.value for tf in Timeframe])
        self.tf_combo.setCurrentText(Timeframe.H1.value)

        today = QDate.currentDate()
        self.start_edit = QDateEdit(today.addYears(-1))
        self.end_edit = QDateEdit(today)
        for editor in (self.start_edit, self.end_edit):
            editor.setCalendarPopup(True)
            editor.setDisplayFormat("yyyy-MM-dd")

        self.download_button = QPushButton("Download")
        self.download_button.setEnabled(False)
        self.download_button.clicked.connect(self._start_download)
        self.download_status = QLabel("Connect to MT5 to download.")
        self.download_status.setWordWrap(True)

        form = QFormLayout()
        form.addRow("Symbol:", self.symbol_combo)
        form.addRow("Timeframe:", self.tf_combo)
        form.addRow("From:", self.start_edit)
        form.addRow("To:", self.end_edit)

        dl_group = QGroupBox("Download Bars")
        dl_layout = QVBoxLayout(dl_group)
        dl_layout.addLayout(form)
        dl_layout.addWidget(self.download_button)
        dl_layout.addWidget(self.download_status)

        column.addWidget(conn_group)
        column.addWidget(dl_group)
        column.addStretch()
        return panel

    def _build_library_panel(self) -> QWidget:
        group = QGroupBox("Local Data Library")
        layout = QVBoxLayout(group)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(
            ["Symbol", "TF", "From", "To", "Bars", "Size"]
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.verticalHeader().setVisible(False)

        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self._refresh_table)
        import_button = QPushButton("Import CSV…")
        import_button.clicked.connect(self._import_csv)
        export_button = QPushButton("Export CSV…")
        export_button.clicked.connect(self._export_csv)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self._delete_dataset)

        buttons = QHBoxLayout()
        for button in (refresh_button, import_button, export_button, delete_button):
            buttons.addWidget(button)
        buttons.addStretch()

        layout.addWidget(self.table)
        layout.addLayout(buttons)
        return group

    # ---------------------------------------------------------- connection

    def _toggle_connection(self) -> None:
        if self.client.connected:
            self.client.shutdown()
            self.connect_button.setText("Connect to MT5")
            self.connection_label.setText("Not connected.")
            self.download_button.setEnabled(False)
            self.download_status.setText("Connect to MT5 to download.")
            return

        try:
            summary = self.client.connect()
        except MT5Error as exc:
            QMessageBox.warning(self, "MT5 Connection", str(exc))
            return

        self.connect_button.setText("Disconnect")
        self.connection_label.setText(
            f"{summary['terminal']} — {summary['company']}\n"
            f"Account {summary['login']} @ {summary['server']}\n"
            f"Balance: {summary['balance']} {summary['currency']}"
        )
        self.download_button.setEnabled(True)
        self.download_status.setText("Ready to download.")
        self._populate_symbols()

    def _populate_symbols(self) -> None:
        try:
            symbols = self.client.list_symbols()
        except MT5Error:
            symbols = []
        current = self.symbol_combo.currentText()
        self.symbol_combo.clear()
        self.symbol_combo.addItems(symbols)
        completer = QCompleter(symbols, self.symbol_combo)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.symbol_combo.setCompleter(completer)
        if current:
            self.symbol_combo.setCurrentText(current)

    # ------------------------------------------------------------ download

    def _start_download(self) -> None:
        symbol = self.symbol_combo.currentText().strip().upper()
        if not symbol:
            QMessageBox.warning(self, "Download", "Enter a symbol first.")
            return
        start = self.start_edit.date().toPython()
        end = self.end_edit.date().toPython()
        if start >= end:
            QMessageBox.warning(self, "Download", "'From' must be before 'To'.")
            return

        self.download_button.setEnabled(False)
        self.download_status.setText(f"Downloading {symbol} {self.tf_combo.currentText()}…")

        self._worker = DownloadWorker(
            self.client,
            self.store,
            symbol,
            self.tf_combo.currentText(),
            datetime(start.year, start.month, start.day),
            datetime(end.year, end.month, end.day, 23, 59, 59),
            parent=self,
        )
        self._worker.done.connect(self._download_done)
        self._worker.failed.connect(self._download_failed)
        self._worker.start()

    def _download_done(self, info: DatasetInfo) -> None:
        self.download_button.setEnabled(True)
        self.download_status.setText(
            f"Saved {info.bars:,} bars of {info.symbol} {info.timeframe}."
        )
        self._refresh_table()
        self.datasets_changed.emit()

    def _download_failed(self, message: str) -> None:
        self.download_button.setEnabled(True)
        self.download_status.setText("Download failed.")
        QMessageBox.warning(self, "Download failed", message)

    # ------------------------------------------------------------- library

    def _refresh_table(self) -> None:
        datasets = self.store.datasets()
        self.table.setRowCount(len(datasets))
        for row, info in enumerate(datasets):
            size_mb = self.store.size_bytes(info) / (1024 * 1024)
            values = [
                info.symbol,
                info.timeframe,
                info.start,
                info.end,
                f"{info.bars:,}",
                f"{size_mb:.2f} MB",
            ]
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.ItemDataRole.UserRole, info)
                self.table.setItem(row, column, item)

    def _selected_dataset(self) -> DatasetInfo | None:
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def _import_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Import CSV", "", "CSV files (*.csv *.txt);;All files (*)"
        )
        if not path:
            return
        answer = ImportDialog.get(self, path)
        if answer is None:
            return
        symbol, timeframe = answer
        try:
            info = self.store.import_csv(path, symbol, timeframe)
        except (StoreError, ValueError) as exc:
            QMessageBox.warning(self, "Import failed", str(exc))
            return
        self._refresh_table()
        self.datasets_changed.emit()
        self.download_status.setText(
            f"Imported {info.bars:,} bars as {info.symbol} {info.timeframe}."
        )

    def _export_csv(self) -> None:
        info = self._selected_dataset()
        if info is None:
            QMessageBox.information(self, "Export CSV", "Select a dataset first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", f"{info.key}.csv", "CSV files (*.csv)"
        )
        if not path:
            return
        try:
            self.store.export_csv(info.symbol, info.timeframe, path)
        except StoreError as exc:
            QMessageBox.warning(self, "Export failed", str(exc))

    def _delete_dataset(self) -> None:
        info = self._selected_dataset()
        if info is None:
            QMessageBox.information(self, "Delete", "Select a dataset first.")
            return
        answer = QMessageBox.question(
            self,
            "Delete dataset",
            f"Delete {info.symbol} {info.timeframe} ({info.bars:,} bars) from the library?",
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            self.store.delete(info.symbol, info.timeframe)
        except StoreError as exc:
            QMessageBox.warning(self, "Delete failed", str(exc))
        self._refresh_table()
        self.datasets_changed.emit()

    # ------------------------------------------------------------ lifecycle

    def shutdown(self) -> None:
        if self._worker is not None and self._worker.isRunning():
            self._worker.wait(5_000)
        self.client.shutdown()
