"""Thin wrapper around the MetaTrader5 package.

The MetaTrader5 package is imported lazily so the rest of the app still works
on machines without it — data can always be brought in via CSV import.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from .models import Timeframe
from .store import normalize_bars


class MT5Error(RuntimeError):
    """Raised when the MetaTrader5 package or terminal reports a failure."""


def _mt5():
    try:
        import MetaTrader5 as mt5
    except ImportError as exc:
        raise MT5Error(
            "The 'MetaTrader5' package is not installed or not supported on this "
            "Python version. Install it on Windows with: pip install MetaTrader5\n"
            "CSV import still works without it."
        ) from exc
    return mt5


def _timeframe_constant(mt5, timeframe: Timeframe) -> int:
    return {
        Timeframe.M1: mt5.TIMEFRAME_M1,
        Timeframe.M5: mt5.TIMEFRAME_M5,
        Timeframe.M15: mt5.TIMEFRAME_M15,
        Timeframe.M30: mt5.TIMEFRAME_M30,
        Timeframe.H1: mt5.TIMEFRAME_H1,
        Timeframe.H4: mt5.TIMEFRAME_H4,
        Timeframe.D1: mt5.TIMEFRAME_D1,
        Timeframe.W1: mt5.TIMEFRAME_W1,
        Timeframe.MN1: mt5.TIMEFRAME_MN1,
    }[timeframe]


class MT5Client:
    """Connection to a locally installed, logged-in MetaTrader 5 terminal."""

    def __init__(self) -> None:
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self, terminal_path: str | None = None) -> dict[str, Any]:
        """Attach to the MT5 terminal and return a connection summary."""
        mt5 = _mt5()
        ok = mt5.initialize(terminal_path) if terminal_path else mt5.initialize()
        if not ok:
            raise MT5Error(
                f"Could not attach to the MT5 terminal: {mt5.last_error()}\n"
                "Make sure MetaTrader 5 is installed and logged in to a broker."
            )
        self._connected = True
        return self.summary()

    def shutdown(self) -> None:
        if self._connected:
            _mt5().shutdown()
            self._connected = False

    def summary(self) -> dict[str, Any]:
        mt5 = _mt5()
        terminal = mt5.terminal_info()
        account = mt5.account_info()
        return {
            "terminal": getattr(terminal, "name", "?"),
            "company": getattr(terminal, "company", "?"),
            "login": getattr(account, "login", "?"),
            "server": getattr(account, "server", "?"),
            "currency": getattr(account, "currency", "?"),
            "balance": getattr(account, "balance", "?"),
        }

    def list_symbols(self) -> list[str]:
        symbols = _mt5().symbols_get()
        return sorted(s.name for s in symbols or [])

    def download_bars(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
    ) -> pd.DataFrame:
        """Fetch bars for ``symbol`` in ``[start, end]`` as a normalized frame.

        Bar times are MT5 server time. The terminal's "Max bars in chart"
        setting caps how much history one request can return.
        """
        mt5 = _mt5()
        tf = Timeframe(timeframe)
        if not mt5.symbol_select(symbol, True):
            raise MT5Error(f"Symbol {symbol!r} not found: {mt5.last_error()}")

        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
        if end.tzinfo is None:
            end = end.replace(tzinfo=timezone.utc)

        rates = mt5.copy_rates_range(symbol, _timeframe_constant(mt5, tf), start, end)
        if rates is None:
            raise MT5Error(f"Download failed for {symbol} {tf.value}: {mt5.last_error()}")
        if len(rates) == 0:
            raise MT5Error(
                f"MT5 returned no {symbol} {tf.value} bars for that range. "
                "Check the broker's history depth and the terminal's "
                "'Max bars in chart' setting (Tools > Options > Charts)."
            )
        return normalize_bars(pd.DataFrame(rates))
