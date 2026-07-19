"""Vectorized indicators. All return numpy arrays aligned to the input,
with NaN where the indicator is not yet defined."""

from __future__ import annotations

import numpy as np
import pandas as pd


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


class IndicatorFactory:
    """Bound to a bar DataFrame; used by strategies as ``self.ind.sma(20)``."""

    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    def _source(self, name: str) -> np.ndarray:
        return self._df[name].to_numpy(dtype=float)

    def sma(self, period: int, source: str = "close") -> np.ndarray:
        return sma(self._source(source), period)

    def ema(self, period: int, source: str = "close") -> np.ndarray:
        return ema(self._source(source), period)

    def rsi(self, period: int = 14, source: str = "close") -> np.ndarray:
        return rsi(self._source(source), period)

    def atr(self, period: int = 14) -> np.ndarray:
        return atr(self._source("high"), self._source("low"), self._source("close"), period)

    def highest(self, period: int, source: str = "high") -> np.ndarray:
        return highest(self._source(source), period)

    def lowest(self, period: int, source: str = "low") -> np.ndarray:
        return lowest(self._source(source), period)
