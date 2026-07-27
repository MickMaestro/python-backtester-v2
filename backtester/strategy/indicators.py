"""Vectorized indicators. All return numpy arrays aligned to the input,
with NaN where the indicator is not yet defined."""

from __future__ import annotations

from enum import Enum

import numpy as np
import pandas as pd


class AppliedPrice(Enum):
    """Price an indicator is computed on (MT5's applied-price conventions)."""

    CLOSE = "close"
    OPEN = "open"
    HIGH = "high"
    LOW = "low"
    MEDIAN = "median"      # (High + Low) / 2
    TYPICAL = "typical"    # (High + Low + Close) / 3
    WEIGHTED = "weighted"  # (High + Low + 2*Close) / 4

    @property
    def label(self) -> str:
        return _APPLIED_LABELS[self]

    @property
    def short(self) -> str:
        return self.name.title()


_APPLIED_LABELS = {
    AppliedPrice.CLOSE: "Close",
    AppliedPrice.OPEN: "Open",
    AppliedPrice.HIGH: "High",
    AppliedPrice.LOW: "Low",
    AppliedPrice.MEDIAN: "Median (HL/2)",
    AppliedPrice.TYPICAL: "Typical (HLC/3)",
    AppliedPrice.WEIGHTED: "Weighted (HLCC/4)",
}


def price_series(df: pd.DataFrame, applied: AppliedPrice | str = AppliedPrice.CLOSE) -> np.ndarray:
    """The chosen applied-price series from a bar DataFrame."""
    applied = AppliedPrice(applied) if not isinstance(applied, AppliedPrice) else applied
    o = df["open"].to_numpy(dtype=float)
    h = df["high"].to_numpy(dtype=float)
    l = df["low"].to_numpy(dtype=float)
    c = df["close"].to_numpy(dtype=float)
    return {
        AppliedPrice.CLOSE: c,
        AppliedPrice.OPEN: o,
        AppliedPrice.HIGH: h,
        AppliedPrice.LOW: l,
        AppliedPrice.MEDIAN: (h + l) / 2.0,
        AppliedPrice.TYPICAL: (h + l + c) / 3.0,
        AppliedPrice.WEIGHTED: (h + l + 2.0 * c) / 4.0,
    }[applied]


def sma(values: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(values).rolling(period).mean().to_numpy()


def ema(values: np.ndarray, period: int) -> np.ndarray:
    # .copy(): pandas 3 returns read-only views from to_numpy(), and the
    # warm-up region is overwritten with NaN below.
    out = pd.Series(values).ewm(span=period, adjust=False).mean().to_numpy().copy()
    out[: period - 1] = np.nan  # treat the spin-up region as undefined
    return out


def rsi(values: np.ndarray, period: int = 14) -> np.ndarray:
    """Wilder's RSI."""
    series = pd.Series(values)
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    out = (100 - 100 / (1 + rs)).fillna(100.0).to_numpy().copy()
    out[:period] = np.nan
    return out


def atr(
    high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14
) -> np.ndarray:
    """Wilder's Average True Range."""
    h, l = pd.Series(high), pd.Series(low)
    prev_close = pd.Series(close).shift(1)
    tr = pd.concat(
        [h - l, (h - prev_close).abs(), (l - prev_close).abs()], axis=1
    ).max(axis=1)
    out = tr.ewm(alpha=1 / period, adjust=False).mean().to_numpy().copy()
    out[:period] = np.nan
    return out


def highest(values: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(values).rolling(period).max().to_numpy()


def lowest(values: np.ndarray, period: int) -> np.ndarray:
    return pd.Series(values).rolling(period).min().to_numpy()


def applied_name(applied) -> str:
    """Display name of an applied price, for indicator recipes and labels."""
    return applied.short if isinstance(applied, AppliedPrice) else str(applied).title()


class IndicatorFactory:
    """Bound to a bar DataFrame; used by strategies as ``self.ind.sma(20)``.

    Price-based indicators take an ``applied`` price (an :class:`AppliedPrice`,
    or its string value / a raw column name for back-compat), e.g.
    ``self.ind.ema(20, applied=AppliedPrice.TYPICAL)``.

    Every series handed out is remembered in ``registry`` along with the call
    that produced it ("ema(50, Typical)"), so a post-run pass can say what a
    strategy actually computed — see ``engine/trade_log.py``.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df
        #: id(array) -> (array, recipe). The array is kept so a lookup can
        #: confirm identity: ids are reused once an array is collected.
        self.registry: dict[int, tuple[np.ndarray, str]] = {}

    def _record(self, values: np.ndarray, recipe: str) -> np.ndarray:
        self.registry[id(values)] = (values, recipe)
        return values

    def recipe_for(self, values) -> str:
        """The call that produced ``values``, or "" if it wasn't built here."""
        entry = self.registry.get(id(values))
        return entry[1] if entry is not None and entry[0] is values else ""

    def _source(self, name: str) -> np.ndarray:
        return self._df[name].to_numpy(dtype=float)

    def _series(self, applied) -> np.ndarray:
        if isinstance(applied, AppliedPrice):
            return price_series(self._df, applied)
        key = str(applied).lower()
        try:
            return price_series(self._df, AppliedPrice(key))
        except ValueError:
            return self._source(applied)  # raw column name

    def sma(self, period: int, applied=AppliedPrice.CLOSE) -> np.ndarray:
        return self._record(
            sma(self._series(applied), period), f"sma({period}, {applied_name(applied)})"
        )

    def ema(self, period: int, applied=AppliedPrice.CLOSE) -> np.ndarray:
        return self._record(
            ema(self._series(applied), period), f"ema({period}, {applied_name(applied)})"
        )

    def rsi(self, period: int = 14, applied=AppliedPrice.CLOSE) -> np.ndarray:
        return self._record(
            rsi(self._series(applied), period), f"rsi({period}, {applied_name(applied)})"
        )

    def atr(self, period: int = 14) -> np.ndarray:
        # ATR is intrinsically High/Low/Close-based; applied price does not apply.
        return self._record(
            atr(self._source("high"), self._source("low"), self._source("close"), period),
            f"atr({period})",
        )

    def highest(self, period: int, applied=AppliedPrice.HIGH) -> np.ndarray:
        return self._record(
            highest(self._series(applied), period),
            f"highest({period}, {applied_name(applied)})",
        )

    def lowest(self, period: int, applied=AppliedPrice.LOW) -> np.ndarray:
        return self._record(
            lowest(self._series(applied), period),
            f"lowest({period}, {applied_name(applied)})",
        )
