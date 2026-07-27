"""Trade log settings and their dialog.

The writer itself is Qt-free and lives in ``engine/trade_log.py``; this module
only holds what the GUI adds — where the folder goes, whether the option is on,
and a dialog to edit it. Settings persist via QSettings like ChartSettings.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

from PySide6.QtCore import QStandardPaths, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from backtester.engine.trade_log import ContextMode, TradeLogSpec
from backtester.ui.settings import app_settings, cast_like


def default_trade_log_dir() -> Path:
    """``trade_logs/`` next to the app (or next to the .exe when frozen)."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "trade_logs"
    return Path(__file__).resolve().parents[2] / "trade_logs"


@dataclass
class TradeLogSettings:
    """The GUI's view of trade logging: on/off, where, and what to log."""

    enabled: bool = False
    folder: str = ""                  # empty → default_trade_log_dir()
    spec: TradeLogSpec = field(default_factory=TradeLogSpec)

    def directory(self) -> Path:
        return Path(self.folder) if self.folder else default_trade_log_dir()

    @classmethod
    def load(cls) -> "TradeLogSettings":
        s = app_settings()
        d = cls()
        try:
            mode = ContextMode(str(s.value("tradelog/mode", d.spec.mode.value)))
        except ValueError:
            mode = d.spec.mode
        return cls(
            enabled=cast_like(s.value("tradelog/enabled"), d.enabled),
            folder=str(s.value("tradelog/folder", d.folder) or ""),
            spec=TradeLogSpec(
                entries=cast_like(s.value("tradelog/entries"), d.spec.entries),
                modifications=cast_like(
                    s.value("tradelog/modifications"), d.spec.modifications
                ),
                exits=cast_like(s.value("tradelog/exits"), d.spec.exits),
                mode=mode,
                context_bars=cast_like(
                    s.value("tradelog/context_bars"), d.spec.context_bars
                ),
                max_moments=cast_like(
                    s.value("tradelog/max_moments"), d.spec.max_moments
                ),
            ),
        )

    def save(self) -> None:
        s = app_settings()
        s.setValue("tradelog/enabled", self.enabled)
        s.setValue("tradelog/folder", self.folder)
        s.setValue("tradelog/entries", self.spec.entries)
        s.setValue("tradelog/modifications", self.spec.modifications)
        s.setValue("tradelog/exits", self.spec.exits)
        s.setValue("tradelog/mode", self.spec.mode.value)
        s.setValue("tradelog/context_bars", self.spec.context_bars)
        s.setValue("tradelog/max_moments", self.spec.max_moments)


class TradeLogDialog(QDialog):
    """Choose which trade moments to log, how much context, and where."""

    def __init__(self, settings: TradeLogSettings, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Trade Log")
        spec = settings.spec

        self.entry_check = QCheckBox("Entries")
        self.entry_check.setChecked(spec.entries)
        self.modify_check = QCheckBox("Modifications (SL/TP changes)")
        self.modify_check.setChecked(spec.modifications)
        self.exit_check = QCheckBox("Exits")
        self.exit_check.setChecked(spec.exits)

        self.mode_combo = QComboBox()
        # Item data is the enum's *value*: ContextMode subclasses str, and Qt
        # marshals that to a plain string, so a stored member comes back out
        # as "bars" and identity checks on it would quietly fail.
        for mode in ContextMode:
            self.mode_combo.addItem(mode.label, mode.value)
        self.mode_combo.setCurrentIndex(self.mode_combo.findData(spec.mode.value))
        self.mode_combo.currentIndexChanged.connect(self._sync_mode)
        self.mode_combo.setToolTip(
            "Last N bars: the history the strategy had, nothing after.\n"
            "Whole day: every bar of that calendar day, including what "
            "followed the moment."
        )
        self.context_spin = QSpinBox()
        self.context_spin.setRange(2, 100_000)
        self.context_spin.setValue(spec.context_bars)
        self.context_spin.setSuffix(" bars")

        self.max_spin = QSpinBox()
        self.max_spin.setRange(0, 1_000_000)
        self.max_spin.setValue(spec.max_moments)
        self.max_spin.setSpecialValueText("No limit")
        self.max_spin.setToolTip(
            "A trailing-stop strategy modifies its SL on most bars, so logging "
            "modifications can run to thousands of windows."
        )

        self.folder_edit = QLineEdit(settings.folder)
        self.folder_edit.setPlaceholderText(str(default_trade_log_dir()))
        browse = QPushButton("Browse…")
        browse.clicked.connect(self._browse)
        open_button = QPushButton("Open")
        open_button.setToolTip("Open the trade log folder")
        open_button.clicked.connect(self._open_folder)
        folder_row = QHBoxLayout()
        folder_row.addWidget(self.folder_edit, stretch=1)
        folder_row.addWidget(browse)
        folder_row.addWidget(open_button)

        form = QFormLayout()
        form.addRow("Log:", self.entry_check)
        form.addRow("", self.modify_check)
        form.addRow("", self.exit_check)
        form.addRow("Context:", self.mode_combo)
        form.addRow("Bars:", self.context_spin)
        form.addRow("Max moments/run:", self.max_spin)
        form.addRow("Folder:", folder_row)

        note = QLabel(
            "One folder per run holding context.parquet (every window, stacked "
            "and tagged by moment), manifest.csv (what happened at each), and "
            "indicators.csv (what each indicator column was computed from)."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: gray;")

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.RestoreDefaults
            | QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(
            self._restore_defaults
        )

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(note)
        layout.addWidget(buttons)
        self._sync_mode()

    def _mode(self) -> ContextMode:
        return ContextMode(self.mode_combo.currentData())

    def _sync_mode(self) -> None:
        # The bar count only means something for the "last N bars" window.
        self.context_spin.setEnabled(self._mode() is ContextMode.BARS)

    def _browse(self) -> None:
        start = self.folder_edit.text() or str(default_trade_log_dir())
        if not Path(start).exists():
            start = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
        chosen = QFileDialog.getExistingDirectory(self, "Trade log folder", start)
        if chosen:
            self.folder_edit.setText(chosen)

    def _open_folder(self) -> None:
        folder = Path(self.folder_edit.text() or default_trade_log_dir())
        folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))

    def _restore_defaults(self) -> None:
        d = TradeLogSettings()
        self.entry_check.setChecked(d.spec.entries)
        self.modify_check.setChecked(d.spec.modifications)
        self.exit_check.setChecked(d.spec.exits)
        self.mode_combo.setCurrentIndex(self.mode_combo.findData(d.spec.mode.value))
        self.context_spin.setValue(d.spec.context_bars)
        self.max_spin.setValue(d.spec.max_moments)
        self.folder_edit.setText(d.folder)

    def result_settings(self, enabled: bool) -> TradeLogSettings:
        return TradeLogSettings(
            enabled=enabled,
            folder=self.folder_edit.text().strip(),
            spec=TradeLogSpec(
                entries=self.entry_check.isChecked(),
                modifications=self.modify_check.isChecked(),
                exits=self.exit_check.isChecked(),
                mode=self._mode(),
                context_bars=self.context_spin.value(),
                max_moments=self.max_spin.value(),
            ),
        )

    @staticmethod
    def edit(
        parent: QWidget, settings: TradeLogSettings
    ) -> "TradeLogSettings | None":
        dialog = TradeLogDialog(settings, parent)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        return dialog.result_settings(settings.enabled)
