"""Chart display settings — colours, grid, and period separators.

Persisted globally via QSettings so the look is consistent across every chart
and remembered between sessions.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields

import pyqtgraph as pg
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
    QWidget,
)

from backtester.ui.settings import app_settings, cast_like


@dataclass
class ChartSettings:
    up_color: str = "#26a69a"          # bullish candle
    down_color: str = "#ef5350"        # bearish candle
    background: str = "#131722"
    grid_visible: bool = False         # default: no grid
    grid_color: str = "#2a2e39"
    separators_visible: bool = True     # default: period separators on
    separator_color: str = "#3a4a5a"

    @classmethod
    def load(cls) -> "ChartSettings":
        s = app_settings()
        d = cls()
        return cls(
            up_color=str(s.value("chart/up_color", d.up_color)),
            down_color=str(s.value("chart/down_color", d.down_color)),
            background=str(s.value("chart/background", d.background)),
            grid_visible=cast_like(s.value("chart/grid_visible"), d.grid_visible),
            grid_color=str(s.value("chart/grid_color", d.grid_color)),
            separators_visible=cast_like(
                s.value("chart/separators_visible"), d.separators_visible
            ),
            separator_color=str(s.value("chart/separator_color", d.separator_color)),
        )

    def save(self) -> None:
        s = app_settings()
        for key, value in asdict(self).items():
            s.setValue(f"chart/{key}", value)


class ChartSettingsDialog(QDialog):
    """Edit chart colours, grid, and period separators."""

    def __init__(self, settings: ChartSettings, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Chart Display Settings")

        self.up_btn = pg.ColorButton(color=settings.up_color)
        self.down_btn = pg.ColorButton(color=settings.down_color)
        self.bg_btn = pg.ColorButton(color=settings.background)
        self.grid_check = QCheckBox()
        self.grid_check.setChecked(settings.grid_visible)
        self.grid_btn = pg.ColorButton(color=settings.grid_color)
        self.sep_check = QCheckBox()
        self.sep_check.setChecked(settings.separators_visible)
        self.sep_btn = pg.ColorButton(color=settings.separator_color)

        form = QFormLayout()
        form.addRow("Bullish candle:", self.up_btn)
        form.addRow("Bearish candle:", self.down_btn)
        form.addRow("Background:", self.bg_btn)
        form.addRow("Show grid:", self.grid_check)
        form.addRow("Grid colour:", self.grid_btn)
        form.addRow("Show period separators:", self.sep_check)
        form.addRow("Separator colour:", self.sep_btn)

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
        layout.addWidget(buttons)

    def _restore_defaults(self) -> None:
        d = ChartSettings()
        self.up_btn.setColor(d.up_color)
        self.down_btn.setColor(d.down_color)
        self.bg_btn.setColor(d.background)
        self.grid_check.setChecked(d.grid_visible)
        self.grid_btn.setColor(d.grid_color)
        self.sep_check.setChecked(d.separators_visible)
        self.sep_btn.setColor(d.separator_color)

    def result_settings(self) -> ChartSettings:
        return ChartSettings(
            up_color=self.up_btn.color().name(),
            down_color=self.down_btn.color().name(),
            background=self.bg_btn.color().name(),
            grid_visible=self.grid_check.isChecked(),
            grid_color=self.grid_btn.color().name(),
            separators_visible=self.sep_check.isChecked(),
            separator_color=self.sep_btn.color().name(),
        )

    @staticmethod
    def edit(parent: QWidget, settings: ChartSettings) -> "ChartSettings | None":
        dialog = ChartSettingsDialog(settings, parent)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None
        return dialog.result_settings()


# Keep for symmetry / potential external use.
SETTINGS_FIELDS = [f.name for f in fields(ChartSettings)]
