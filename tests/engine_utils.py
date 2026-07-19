"""Shared helpers for engine tests."""

from __future__ import annotations

import numpy as np
import pandas as pd

from backtester.strategy.base import Strategy


def make_df(
    bars: list[tuple[float, float, float, float]],
    start: str = "2024-01-01",
    freq: str = "1h",
    spread: int = 0,
) -> pd.DataFrame:
    """Build a bar frame from (open, high, low, close) tuples."""
    opens, highs, lows, closes = zip(*bars)
    return pd.DataFrame(
        {
            "time": pd.date_range(start, periods=len(bars), freq=freq),
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "spread": spread,
        }
    )


def make_wave(
    n: int = 400, period: int = 50, amplitude: float = 0.01, base: float = 1.10
) -> pd.DataFrame:
    """Sine-wave closes — guarantees MA crossovers for integration tests."""
    xs = np.arange(n)
    closes = base + amplitude * np.sin(2 * np.pi * xs / period)
    opens = np.roll(closes, 1)
    opens[0] = closes[0]
    highs = np.maximum(opens, closes) + 0.0005
    lows = np.minimum(opens, closes) - 0.0005
    return pd.DataFrame(
        {
            "time": pd.date_range("2024-01-01", periods=n, freq="1h"),
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "spread": 10,
        }
    )


class Scripted(Strategy):
    """Executes canned actions at given bar indices: ``{index: [fn(strategy)]}``."""

    def __init__(self, script: dict | None = None):
        super().__init__()
        self._script = script or {}

    def on_bar(self, bar):
        for action in self._script.get(self.i, []):
            action(self)


def events_of(events: list, event_type: type) -> list:
    return [e for e in events if isinstance(e, event_type)]
