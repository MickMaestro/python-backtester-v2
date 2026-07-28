"""Pick which indicators are on the charts, and with what parameters.

Indicators are discovered from the ``indicators/`` folder on every open, so
editing a file and reopening this dialog picks up the change. The chosen set is
persisted (name + parameter values) and applied to every chart in the app.
"""

from __future__ import annotations

import json

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from backtester.indicators import loader
from backtester.indicators.base import Indicator
from backtester.ui.param_form import build_form, clear_form, collect_form
from backtester.ui.settings import app_settings


def load_selection() -> list[Indicator]:
    """Rebuild the saved indicator set. Unknown or broken entries are skipped."""
    raw = str(app_settings().value("indicators/selection", "") or "")
    if not raw:
        return []
    try:
        saved = json.loads(raw)
    except ValueError:
        return []

    registry, _errors = loader.discover()
    chosen: list[Indicator] = []
    for entry in saved:
        item = registry.get(entry.get("name", ""))
        if item is None:
            continue
        try:
            chosen.append(item[0](**entry.get("params", {})))
        except (ValueError, TypeError):
            continue  # the file's parameters changed under a saved selection
    return chosen


def save_selection(indicators: list[Indicator]) -> None:
    app_settings().setValue(
        "indicators/selection",
        json.dumps(
            [{"name": i.display_name, "params": i.values()} for i in indicators]
        ),
    )


class IndicatorsDialog(QDialog):
    """Available indicators on the left, the ones on the chart on the right."""

    def __init__(self, chosen: list[Indicator], parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Chart Indicators")
        self.resize(700, 460)
        self._registry: dict = {}
        self._widgets: dict = {}
        self._chosen: list[Indicator] = list(chosen)

        self.available = QListWidget()
        self.available.currentTextChanged.connect(self._show_params)
        reload_button = QPushButton("Reload")
        reload_button.setToolTip("Re-read the indicators/ folder")
        reload_button.clicked.connect(self.reload)
        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet("color: #ef5350;")

        self.params_group = QGroupBox("Parameters")
        self.params_form = QFormLayout(self.params_group)

        add_button = QPushButton("Add to chart  →")
        add_button.clicked.connect(self._add)

        self.attached = QListWidget()
        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self._remove)
        clear_button = QPushButton("Remove all")
        clear_button.clicked.connect(self._clear)

        left = QVBoxLayout()
        left.addWidget(QLabel("Available"))
        left.addWidget(self.available, stretch=1)
        left.addWidget(reload_button)

        middle = QVBoxLayout()
        middle.addWidget(self.params_group, stretch=1)
        middle.addWidget(add_button)

        right = QVBoxLayout()
        right.addWidget(QLabel("On the chart"))
        right.addWidget(self.attached, stretch=1)
        buttons_row = QHBoxLayout()
        buttons_row.addWidget(remove_button)
        buttons_row.addWidget(clear_button)
        right.addLayout(buttons_row)

        columns = QHBoxLayout()
        columns.addLayout(left, stretch=2)
        columns.addLayout(middle, stretch=3)
        columns.addLayout(right, stretch=3)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(columns, stretch=1)
        layout.addWidget(self.error_label)
        layout.addWidget(buttons)

        self.reload()
        self._refresh_attached()

    # ------------------------------------------------------------ contents

    def reload(self) -> None:
        current = self.available.currentItem()
        name = current.text() if current else ""
        self._registry, errors = loader.discover()
        self.available.clear()
        self.available.addItems(sorted(self._registry))
        if name and self.available.findItems(name, 0):
            self.available.setCurrentItem(self.available.findItems(name, 0)[0])
        elif self.available.count():
            self.available.setCurrentRow(0)
        self.error_label.setText("\n".join(errors))

    def _show_params(self, name: str) -> None:
        entry = self._registry.get(name)
        if entry is None:
            clear_form(self.params_form)
            self._widgets = {}
            return
        self._widgets = build_form(self.params_form, entry[0].params)

    def _add(self) -> None:
        item = self.available.currentItem()
        if item is None:
            return
        entry = self._registry.get(item.text())
        if entry is None:
            return
        try:
            self._chosen.append(entry[0](**collect_form(self._widgets)))
        except (ValueError, TypeError) as exc:
            self.error_label.setText(f"{item.text()}: {exc}")
            return
        self._refresh_attached()

    def _remove(self) -> None:
        row = self.attached.currentRow()
        if 0 <= row < len(self._chosen):
            del self._chosen[row]
            self._refresh_attached()

    def _clear(self) -> None:
        self._chosen.clear()
        self._refresh_attached()

    def _refresh_attached(self) -> None:
        self.attached.clear()
        for indicator in self._chosen:
            QListWidgetItem(indicator.label, self.attached)

    # -------------------------------------------------------------- result

    def result_indicators(self) -> list[Indicator]:
        return list(self._chosen)

    @staticmethod
    def edit(parent: QWidget, chosen: list[Indicator]) -> "list[Indicator] | None":
        dialog = IndicatorsDialog(chosen, parent)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        return dialog.result_indicators()
