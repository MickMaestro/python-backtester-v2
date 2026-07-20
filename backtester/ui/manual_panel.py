"""Manual order-entry panel: order type, risk sizing, and trade management.

Pure UI — it reports what the user wants; :class:`~backtester.ui.manual_tab.ManualTab`
does the sizing math and talks to the broker.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from backtester.engine.sizing import RiskMode

MARKET = "Market"
PENDING = "Pending"

_RISK_MODES = (
    (RiskMode.PERCENT_BALANCE, "% of balance", 1.0, 0.01, 100.0, 2),
    (RiskMode.CASH, "Cash amount", 100.0, 0.01, 1e9, 2),
    (RiskMode.LOTS, "Fixed lots", 0.10, 0.01, 1000.0, 2),
)


class ManualPanel(QWidget):
    buy_clicked = Signal()
    sell_clicked = Signal()
    close_clicked = Signal()
    cancel_clicked = Signal()
    #: anything that changes the resolved order (type, risk, TP/SL toggles)
    settings_changed = Signal()
    lines_toggled = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        # --- order type
        self.type_combo = QComboBox()
        self.type_combo.addItems([MARKET, PENDING])
        self.type_combo.currentTextChanged.connect(self._on_settings_changed)
        self.type_combo.setToolTip(
            "Market fills at the next bar's open.\n"
            "Pending places a stop/limit order at the entry line."
        )

        self.sl_check = QCheckBox("Use stop loss")
        self.sl_check.setChecked(True)
        self.tp_check = QCheckBox("Use take profit")
        self.tp_check.setChecked(True)
        for check in (self.sl_check, self.tp_check):
            check.toggled.connect(self._on_lines_toggled)

        type_group = QGroupBox("Order")
        type_layout = QVBoxLayout(type_group)
        type_layout.addWidget(self.type_combo)
        type_layout.addWidget(self.sl_check)
        type_layout.addWidget(self.tp_check)

        # --- risk sizing
        self.risk_group = QGroupBox("Position size")
        risk_layout = QVBoxLayout(self.risk_group)
        self._radios: dict[RiskMode, QRadioButton] = {}
        self._spins: dict[RiskMode, QDoubleSpinBox] = {}
        self._button_group = QButtonGroup(self)
        for mode, label, default, low, high, decimals in _RISK_MODES:
            radio = QRadioButton(label)
            spin = QDoubleSpinBox()
            spin.setRange(low, high)
            spin.setDecimals(decimals)
            spin.setValue(default)
            spin.valueChanged.connect(self._on_settings_changed)
            radio.toggled.connect(self._on_settings_changed)
            self._button_group.addButton(radio)
            self._radios[mode] = radio
            self._spins[mode] = spin
            row = QHBoxLayout()
            row.addWidget(radio)
            row.addWidget(spin)
            risk_layout.addLayout(row)
        self._radios[RiskMode.PERCENT_BALANCE].setChecked(True)

        # --- actions
        self.buy_button = QPushButton("Buy")
        self.buy_button.setStyleSheet("background-color: #26a69a; color: white;")
        self.buy_button.clicked.connect(self.buy_clicked)
        self.sell_button = QPushButton("Sell")
        self.sell_button.setStyleSheet("background-color: #ef5350; color: white;")
        self.sell_button.clicked.connect(self.sell_clicked)
        action_row = QHBoxLayout()
        action_row.addWidget(self.buy_button)
        action_row.addWidget(self.sell_button)

        self.close_button = QPushButton("Close position")
        self.close_button.clicked.connect(self.close_clicked)
        self.cancel_button = QPushButton("Cancel pending")
        self.cancel_button.clicked.connect(self.cancel_clicked)

        self.preview_label = QLabel("—")
        self.preview_label.setWordWrap(True)
        self.preview_label.setStyleSheet(
            "font-family: Consolas, monospace; font-size: 11px;"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(type_group)
        layout.addWidget(self.risk_group)
        layout.addLayout(action_row)
        layout.addWidget(self.close_button)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.preview_label)

        self.set_enabled(False)

    # ------------------------------------------------------------- reading

    @property
    def order_type(self) -> str:
        return self.type_combo.currentText()

    @property
    def is_pending(self) -> bool:
        return self.order_type == PENDING

    @property
    def risk_mode(self) -> RiskMode:
        for mode, radio in self._radios.items():
            if radio.isChecked():
                return mode
        return RiskMode.LOTS

    @property
    def risk_value(self) -> float:
        return float(self._spins[self.risk_mode].value())

    @property
    def use_sl(self) -> bool:
        return self.sl_check.isChecked()

    @property
    def use_tp(self) -> bool:
        return self.tp_check.isChecked()

    # ------------------------------------------------------------- writing

    def set_preview(self, text: str) -> None:
        self.preview_label.setText(text)

    def set_enabled(self, enabled: bool) -> None:
        for widget in (
            self.type_combo, self.sl_check, self.tp_check, self.risk_group,
            self.buy_button, self.sell_button,
        ):
            widget.setEnabled(enabled)
        if not enabled:
            self.close_button.setEnabled(False)
            self.cancel_button.setEnabled(False)

    def set_position_open(self, open_: bool) -> None:
        self.close_button.setEnabled(open_)

    def set_pending_open(self, open_: bool) -> None:
        self.cancel_button.setEnabled(open_)

    # ------------------------------------------------------------- signals

    def _on_settings_changed(self, *_args) -> None:
        self.settings_changed.emit()

    def _on_lines_toggled(self, *_args) -> None:
        self.lines_toggled.emit()
        self.settings_changed.emit()
