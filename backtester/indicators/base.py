"""The indicator plugin API — what a chart indicator declares and computes.

An indicator declares its **parameters**, the **plots** it draws, and which
pane it lives in, then computes a dict of numpy arrays aligned to the bar
frame (NaN where the value is undefined). That is all the chart needs to draw
it, and all the loader needs to build a settings form for it.

    class Ssl(Indicator):
        name = "SSL Channel"
        pane = Pane.PRICE
        params = {"period": 13, "nrtr": True}
        plots = [
            Plot("up",   "Upper SSL", color="#2962ff", width=2, dash=True),
            Plot("down", "Lower SSL", color="#ff1493", width=2, dash=True),
        ]

        def calculate(self, df):
            ...
            return {"up": up, "down": down}

Parameters follow the ``Strategy.params`` convention (ints, floats, bools),
plus :class:`Choice` for a fixed set of options — the form builder renders each
as the right widget.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import SimpleNamespace

import numpy as np
import pandas as pd


class Pane(Enum):
    """Where an indicator draws: over the candles, or in its own sub-window."""

    PRICE = "price"
    SEPARATE = "separate"


class DrawStyle(Enum):
    LINE = "line"
    ARROW = "arrow"              # a marker per non-NaN value
    HISTOGRAM = "histogram"      # vertical bars from zero
    FILL = "fill"                # shaded band between this plot and ``fill_with``
    CANDLE_COLOR = "candle_color"  # per-bar colour index applied to the candles
    NONE = "none"                # computed but not drawn


@dataclass
class Plot:
    """One drawable series produced by :meth:`Indicator.calculate`."""

    key: str                       # the key in the returned dict
    label: str = ""
    style: DrawStyle = DrawStyle.LINE
    color: str = "#f0a732"
    width: float = 1.5
    dash: bool = False
    symbol: str = "o"              # ARROW: pyqtgraph symbol ("o", "t", "t1", "d")
    size: int = 8                  # ARROW: marker size
    fill_with: str = ""            # FILL: key of the band's other edge
    colors: tuple[str, ...] = ()   # CANDLE_COLOR: colour per index value
    pane: Pane | None = None       # override the indicator's pane

    def __post_init__(self) -> None:
        if not self.label:
            self.label = self.key.replace("_", " ").title()


@dataclass
class Level:
    """A horizontal reference line (MT5's ``indicator_levelN``)."""

    value: float
    color: str = "#787b86"
    dash: bool = True


@dataclass
class Choice:
    """A parameter with a fixed set of options, rendered as a dropdown.

    ``options`` maps the stored value to its label; a plain list is taken as
    both. The default is the first option unless ``default`` says otherwise.
    """

    options: list | dict
    default: object = None

    def __post_init__(self) -> None:
        if isinstance(self.options, dict):
            self.labels = dict(self.options)
            self.values = list(self.options)
        else:
            self.values = list(self.options)
            self.labels = {v: str(v).replace("_", " ").title() for v in self.values}
        if self.default is None:
            self.default = self.values[0]

    def label_for(self, value) -> str:
        return self.labels.get(value, str(value))


def default_value(spec):
    """The value a parameter spec starts at (``Choice`` → its default)."""
    return spec.default if isinstance(spec, Choice) else spec


class Indicator:
    #: Display name in the indicator list. Defaults to the class name.
    name: str = ""
    #: Where it draws. Individual plots may override via ``Plot.pane``.
    pane: Pane = Pane.PRICE
    #: Parameter name → default value (or :class:`Choice`).
    params: dict = {}
    #: Plots to draw. Set in :meth:`setup` for parameter-dependent plots.
    plots: list[Plot] = []
    #: Horizontal reference lines (separate panes).
    levels: list[Level] = []
    #: Fixed y-range for a separate pane, e.g. ``(0, 100)`` for an oscillator.
    y_range: tuple[float, float] | None = None

    def __init__(self, **overrides):
        unknown = set(overrides) - set(self.params)
        if unknown:
            raise ValueError(
                f"Unknown parameter(s) for {type(self).__name__}: "
                f"{', '.join(sorted(unknown))}"
            )
        values = {name: default_value(spec) for name, spec in self.params.items()}
        values.update(overrides)
        self.p = SimpleNamespace(**values)
        self.setup()

    # ------------------------------------------------------ user overrides

    def setup(self) -> None:
        """Called after parameters are bound; build parameter-dependent plots."""

    def calculate(self, df: pd.DataFrame) -> dict[str, np.ndarray]:
        """Arrays aligned to ``df``, keyed by plot key. NaN = undefined."""
        raise NotImplementedError

    # ------------------------------------------------------------ display

    @property
    def display_name(self) -> str:
        return self.name or type(self).__name__

    @property
    def label(self) -> str:
        """Name with the parameters that differ from the defaults."""
        changed = [
            f"{name}={_short(getattr(self.p, name))}"
            for name, spec in self.params.items()
            if getattr(self.p, name) != default_value(spec)
        ]
        return f"{self.display_name}({', '.join(changed)})" if changed else self.display_name

    def values(self) -> dict:
        return {name: getattr(self.p, name) for name in self.params}

    # ------------------------------------------------------------- helpers

    def series(self, df: pd.DataFrame, name: str) -> np.ndarray:
        return df[name].to_numpy(dtype=float)

    @staticmethod
    def empty(n: int) -> np.ndarray:
        """A NaN-filled buffer — MT5's EMPTY_VALUE, which is how an unset
        indicator value is represented everywhere in this app."""
        return np.full(n, np.nan)


def _short(value) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)
