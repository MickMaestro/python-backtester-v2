"""Chart tab: pick a dataset from the library, browse it, load indicators."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from backtester.data.store import DataStore, StoreError
from backtester.ui import indicator_templates as templates
from backtester.ui.chart.chart_widget import ChartWidget
from backtester.ui.indicators_dialog import (
    NO_TEMPLATE,
    IndicatorsDialog,
    load_selection,
    save_selection,
)


class ChartTab(QWidget):
    #: Emitted with the new indicator list when the user changes it, so every
    #: chart in the app can show the same set.
    indicators_changed = Signal(list)

    def __init__(self, store: DataStore, parent: QWidget | None = None):
        super().__init__(parent)
        self.store = store
        self._loaded_key: str | None = None
        self._indicators = load_selection()

        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumWidth(160)
        self.dataset_combo.currentTextChanged.connect(self._load_dataset)

        indicators_button = QPushButton("Indicators…")
        indicators_button.setToolTip(
            "Load indicators from the indicators/ folder onto the charts"
        )
        indicators_button.clicked.connect(self._edit_indicators)

        self.template_combo = QComboBox()
        self.template_combo.setMinimumWidth(150)
        self.template_combo.setToolTip(
            "Apply a saved indicator template (manage them in Indicators…)"
        )
        self.template_combo.currentTextChanged.connect(self._apply_template)

        self.indicator_label = QLabel("")
        self.indicator_label.setStyleSheet("color: gray;")

        top = QHBoxLayout()
        top.addWidget(QLabel("Dataset:"))
        top.addWidget(self.dataset_combo)
        top.addSpacing(24)
        top.addWidget(indicators_button)
        top.addWidget(QLabel("Template:"))
        top.addWidget(self.template_combo)
        top.addWidget(self.indicator_label, stretch=1)

        self.chart = ChartWidget()

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self.chart)

        self.refresh_templates()
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
        self.apply_indicators()

    # ---------------------------------------------------------- indicators

    @property
    def indicators(self) -> list:
        return list(self._indicators)

    def apply_indicators(self) -> None:
        """Recompute and draw the current selection on this chart."""
        errors = self.chart.set_indicators(self._indicators)
        names = ", ".join(i.label for i in self._indicators)
        self.indicator_label.setText(names)
        if errors:
            self.indicator_label.setText(f"{names}   —   {len(errors)} failed")
            QMessageBox.warning(self, "Indicators", "\n".join(errors))

    def set_indicators(self, indicators: list) -> None:
        self._indicators = list(indicators)
        self.apply_indicators()

    def _edit_indicators(self) -> None:
        result = IndicatorsDialog.edit(self, self._indicators)
        # The dialog can add or delete templates whether or not it was accepted.
        self.refresh_templates()
        if result is None:
            return
        self._indicators = result
        save_selection(result)
        self.apply_indicators()
        self.indicators_changed.emit(result)

    # ----------------------------------------------------------- templates

    def refresh_templates(self, select: str = "") -> None:
        current = select or self.template_combo.currentText()
        self.template_combo.blockSignals(True)
        self.template_combo.clear()
        self.template_combo.addItem(NO_TEMPLATE)
        self.template_combo.addItems(templates.list_templates())
        index = self.template_combo.findText(current)
        self.template_combo.setCurrentIndex(max(index, 0))
        self.template_combo.blockSignals(False)

    def _apply_template(self, name: str) -> None:
        """Switch the whole indicator set to a saved template."""
        if not name or name == NO_TEMPLATE:
            return
        chosen, skipped = templates.load_template(name)
        self._indicators = chosen
        save_selection(chosen)
        self.apply_indicators()
        self.indicators_changed.emit(chosen)
        if skipped:
            QMessageBox.warning(
                self, "Template", f"{name} — skipped:\n" + "\n".join(skipped)
            )
