"""Builds an editable form from a ``params`` declaration.

Indicators (and strategies) declare parameters as name → default value; this
turns that into the right widget per type and reads the values back. Choice
parameters become a dropdown, bools a checkbox, numbers a spin box.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QSpinBox,
    QWidget,
)

from backtester.indicators.base import Choice, default_value


def clear_form(form: QFormLayout) -> None:
    while form.rowCount():
        form.removeRow(0)


def build_form(
    form: QFormLayout, params: dict, values: dict | None = None
) -> dict[str, QWidget]:
    """Fill ``form`` with a widget per parameter; returns them by name."""
    clear_form(form)
    values = values or {}
    widgets: dict[str, QWidget] = {}

    for name, spec in params.items():
        current = values.get(name, default_value(spec))
        if isinstance(spec, Choice):
            widget = QComboBox()
            for option in spec.values:
                widget.addItem(spec.label_for(option), option)
            index = widget.findData(current)
            widget.setCurrentIndex(index if index >= 0 else 0)
        elif isinstance(spec, bool):
            widget = QCheckBox()
            widget.setChecked(bool(current))
        elif isinstance(spec, int):
            widget = QSpinBox()
            widget.setRange(-1_000_000, 1_000_000)
            widget.setValue(int(current))
        elif isinstance(spec, float):
            widget = QDoubleSpinBox()
            widget.setRange(-1e9, 1e9)
            widget.setDecimals(2)
            widget.setSingleStep(0.1 if abs(spec) < 10 else 1.0)
            widget.setValue(float(current))
        else:
            continue  # only numeric, bool, and choice parameters are editable
        form.addRow(f"{name.replace('_', ' ')}:", widget)
        widgets[name] = widget
    return widgets


def collect_form(widgets: dict[str, QWidget]) -> dict:
    values: dict = {}
    for name, widget in widgets.items():
        if isinstance(widget, QComboBox):
            values[name] = widget.currentData()
        elif isinstance(widget, QCheckBox):
            values[name] = widget.isChecked()
        elif isinstance(widget, QSpinBox):
            values[name] = widget.value()
        elif isinstance(widget, QDoubleSpinBox):
            values[name] = float(widget.value())
    return values
