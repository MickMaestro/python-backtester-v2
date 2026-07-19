"""Chart tab: pick a dataset from the library, browse it, overlay indicators."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from backtester.data.store import DataStore, StoreError
from backtester.strategy import indicators
from backtester.ui.chart.chart_widget import ChartWidget

_INDICATORS = {"SMA": indicators.sma, "EMA": indicators.ema}


class ChartTab(QWidget):
    def __init__(self, store: DataStore, parent: QWidget | None = None):
        super().__init__(parent)
        self.store = store
        self._loaded_key: str | None = None

        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumWidth(160)
        self.dataset_combo.currentTextChanged.connect(self._load_dataset)

        self.indicator_combo = QComboBox()
        self.indicator_combo.addItems(list(_INDICATORS))
        self.period_spin = QSpinBox()
        self.period_spin.setRange(2, 500)
        self.period_spin.setValue(20)
        add_button = QPushButton("Add")
        add_button.clicked.connect(self._add_indicator)
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self._clear_indicators)
        self.overlay_label = QLabel("")
        self.overlay_label.setStyleSheet("color: gray;")

        top = QHBoxLayout()
        top.addWidget(QLabel("Dataset:"))
        top.addWidget(self.dataset_combo)
        top.addSpacing(24)
        top.addWidget(QLabel("Indicator:"))
        top.addWidget(self.indicator_combo)
        top.addWidget(self.period_spin)
        top.addWidget(add_button)
        top.addWidget(clear_button)
        top.addWidget(self.overlay_label)
        top.addStretch()

        self.chart = ChartWidget()

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.chart)

        self.refresh_datasets()

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
        # Load the first dataset automatically on first show.
        if self._loaded_key is None and keys:
            self._load_dataset(self.dataset_combo.currentText())

    def showEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        self.refresh_datasets()
        super().showEvent(event)

    def _load_dataset(self, key: str) -> None:
        if not key or key == self._loaded_key:
            return
        symbol, _, timeframe = key.rpartition("_")
        try:
            df = self.store.load_bars(symbol, timeframe)
        except (StoreError, ValueError) as exc:
            QMessageBox.warning(self, "Load dataset", str(exc))
            return
        self._loaded_key = key
        self.chart.set_data(df, title=f"{symbol} {timeframe}")
        self.overlay_label.setText("")

    # ---------------------------------------------------------- indicators

    def _add_indicator(self) -> None:
        if self.chart.df is None:
            return
        kind = self.indicator_combo.currentText()
        period = self.period_spin.value()
        name = f"{kind}({period})"
        values = _INDICATORS[kind](
            self.chart.df["close"].to_numpy(dtype=float), period
        )
        self.chart.add_overlay(name, values)
        self.overlay_label.setText(", ".join(self.chart.overlay_names))

    def _clear_indicators(self) -> None:
        self.chart.clear_overlays()
        self.overlay_label.setText("")
