"""Integer's "IncOnArray" maths — the MQL5 library behind the ``Test_*OnArray``
indicators, converted forward-indexed (bar 0 = oldest).

The library computes every indicator on plain arrays, so one indicator can be
run on another's output. Its moving average (``CMAOnArray``) differs from the
terminal's ``iMA`` in two ways that matter for matching values:

- EMA and SMMA are seeded with the first valid value rather than an SMA, and
  SMMA is simply an EMA with ``alpha = 1/period``.
- Every calculation starts at the first valid (finite, non-zero) input rather
  than at bar 0, so chained indicators line up behind their inputs.

``bars_required`` mirrors the library's ``BarsRequired()`` — what the source
passes to ``PLOT_DRAW_BEGIN`` to keep the unsettled warm-up off the chart.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from . import mql5
from .base import Choice

EMPTY = np.nan

#: ENUM_MA_METHOD as the library offers it.
MA_CHOICE_OPTIONS = {
    "sma": "Simple",
    "ema": "Exponential",
    "smma": "Smoothed",
    "lwma": "Linear weighted",
}


def ma_choice(default: str = "sma") -> Choice:
    return Choice(MA_CHOICE_OPTIONS, default=default)


#: MT5's "Apply to" list for indicators drawn on a single price series.
PRICE_OPTIONS = {
    "close": "Close", "open": "Open", "high": "High", "low": "Low",
    "median": "Median (HL/2)", "typical": "Typical (HLC/3)",
    "weighted": "Weighted (HLCC/4)",
}


def price_choice(default: str = "close") -> Choice:
    return Choice(PRICE_OPTIONS, default=default)


def first_valid(values: np.ndarray) -> int | None:
    """Index of the first finite, non-zero value — the library's start test."""
    ok = np.nonzero(np.isfinite(values) & (values != 0))[0]
    return int(ok[0]) if len(ok) else None


def bars_required(period: int, method: str) -> int:
    return period * 10 if method in ("ema", "smma") else period


def hide_before(values: np.ndarray, begin: int) -> np.ndarray:
    """``PLOT_DRAW_BEGIN``: blank the first ``begin`` bars."""
    out = np.asarray(values, dtype=float).copy()
    out[: max(0, min(begin, len(out)))] = EMPTY
    return out


def ma(values: np.ndarray, period: int, method: str = "sma") -> np.ndarray:
    """``CMAOnArray.Solve``."""
    values = np.asarray(values, dtype=float)
    n = len(values)
    out = np.full(n, EMPTY)
    period = max(int(period), 1)
    start = first_valid(values)
    if start is None:
        return out
    tail = pd.Series(values[start:])
    if method in ("ema", "smma"):
        alpha = 2.0 / (period + 1.0) if method == "ema" else 1.0 / period
        out[start:] = tail.ewm(alpha=alpha, adjust=False).mean().to_numpy()
    elif method == "lwma":
        out[start:] = mql5.lwma(values[start:], period)
    else:
        out[start:] = tail.rolling(period).mean().to_numpy()
    return out


def window_max(values: np.ndarray, period: int) -> np.ndarray:
    """``values[ArrayMaximum(values, i-period+1, period)]`` at every bar."""
    return pd.Series(values).rolling(max(int(period), 1)).max().to_numpy()


def window_min(values: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(values).rolling(max(int(period), 1)).min().to_numpy()


def window_sum(values: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(values).rolling(max(int(period), 1)).sum().to_numpy()


def abs_change(values: np.ndarray) -> np.ndarray:
    """|x[i] - x[i-1]|, NaN on the first bar."""
    out = np.full(len(values), EMPTY)
    out[1:] = np.abs(np.diff(values))
    return out


def hold_previous(values: np.ndarray, invalid: np.ndarray) -> np.ndarray:
    """``else out[i] = out[i-1]`` — carry the last value over invalid bars."""
    out = np.where(invalid, np.nan, values)
    return pd.Series(out).ffill().to_numpy()


def from_start(values: np.ndarray, start: int | None) -> np.ndarray:
    """Blank everything before a computed start bar."""
    out = np.asarray(values, dtype=float).copy()
    if start is None:
        out[:] = EMPTY
    else:
        out[: max(0, min(start, len(out)))] = EMPTY
    return out
