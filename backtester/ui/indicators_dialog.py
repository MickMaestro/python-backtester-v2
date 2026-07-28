"""Pick which indicators are on the charts, and with what parameters.

Indicators are discovered from the ``indicators/`` folder on every open, so
editing a file and reopening this dialog picks up the change. The chosen set is
persisted (name + parameter values) and applied to every chart in the app, and
can be saved as a named **template** — see ``indicator_templates.py``.
"""

from __future__ import annotations

import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from backtester.indicators import loader
from backtester.indicators.base import Indicator
from backtester.ui import indicator_templates as templates
from backtester.ui.param_form import build_form, clear_form, collect_form
from backtester.ui.settings import app_settings

#: Placeholder row in the template picker — selecting it loads nothing.
NO_TEMPLATE = "(none)"


def load_selection() -> list[Indicator]:
    """Rebuild the saved indicator set. Unknown or broken entries are skipped."""
    raw = str(app_settings().value("indicators/selection", "") or "")
    if not raw:
        return []
    try:
        saved = json.loads(raw)
    except ValueError:
        return []
    chosen, _skipped = templates.build(saved)
    return chosen


def save_selection(indicators: list[Indicator]) -> None:
    app_settings().setValue(
        "indicators/selection", json.dumps(templates.to_spec(indicators))
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
        layout.addLayout(self._build_template_row())
        layout.addLayout(columns, stretch=1)
        layout.addWidget(self.error_label)
        layout.addWidget(buttons)

        self.reload()
        self.refresh_templates()
        self._refresh_attached()

    # ----------------------------------------------------------- templates

    def _build_template_row(self) -> QHBoxLayout:
        self.template_combo = QComboBox()
        self.template_combo.setMinimumWidth(180)
        self.template_combo.setToolTip("Saved indicator sets")
        load_button = QPushButton("Load")
        load_button.clicked.connect(self._load_template)
        save_button = QPushButton("Save as…")
        save_button.setToolTip("Save what's on the chart as a named template")
        save_button.clicked.connect(self._save_template)
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self._delete_template)

        row = QHBoxLayout()
        row.addWidget(QLabel("Template:"))
        row.addWidget(self.template_combo)
        row.addWidget(load_button)
        row.addWidget(save_button)
        row.addWidget(delete_button)
        row.addStretch()
        return row

    def refresh_templates(self, select: str = "") -> None:
        current = select or self.template_combo.currentText()
        self.template_combo.blockSignals(True)
        self.template_combo.clear()
        self.template_combo.addItem(NO_TEMPLATE)
        self.template_combo.addItems(templates.list_templates())
        index = self.template_combo.findText(current)
        self.template_combo.setCurrentIndex(max(index, 0))
        self.template_combo.blockSignals(False)

    def _selected_template(self) -> str:
        name = self.template_combo.currentText()
        return "" if name == NO_TEMPLATE else name

    def _load_template(self) -> None:
        name = self._selected_template()
        if not name:
            return
        chosen, skipped = templates.load_template(name)
        self._chosen = chosen
        self._refresh_attached()
        self.error_label.setText(
            "" if not skipped else f"{name} — skipped:\n" + "\n".join(skipped)
        )

    def _save_template(self) -> None:
        name, accepted = QInputDialog.getText(
            self, "Save template", "Template name:", text=self._selected_template()
        )
        name = name.strip()
        if not accepted or not name:
            return
        if templates.exists(name):
            confirm = QMessageBox.question(
                self, "Save template", f"Replace the existing template {name!r}?"
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return
        templates.save_template(name, self._chosen)
        self.refresh_templates(select=name)
        self.error_label.setText("")

    def _delete_template(self) -> None:
        name = self._selected_template()
        if not name:
            return
        confirm = QMessageBox.question(
            self, "Delete template", f"Delete the template {name!r}?"
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        templates.delete_template(name)
        self.refresh_templates(select=NO_TEMPLATE)

    # ------------------------------------------------------------ contents

    def reload(self) -> None:
        current = self.available.currentItem()
        name = current.text() if current else ""
        self._registry, errors = loader.discover()
        self.available.clear()
        self.available.addItems(sorted(self._registry))
        matches = (
            self.available.findItems(name, Qt.MatchFlag.MatchExactly) if name else []
        )
        if matches:
            self.available.setCurrentItem(matches[0])
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
