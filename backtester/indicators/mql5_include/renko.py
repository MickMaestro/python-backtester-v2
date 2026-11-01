"""``RenkoCharts.mqh`` (Guilherme Santos, 2018, v2.0) — port of the brick engine.

The MQL5 class builds Renko bricks from M1 bars (each bar fed as
open → low/high → close) or from ticks, and publishes them as a *custom
symbol* with its own chart. Custom symbols, chart opening and tick events
are terminal features with no equivalent here (``Symbol.mqh``, which clones
symbol properties into the custom symbol, goes with them); the brick
building itself — ``Setup``, ``LoadPrice``, ``LoadPriceOHLC``, ``LoadFrom``,
``AddOne``/``CloseUp``/``CloseDown``, ``GetValue``/``GetValueAsSeries`` — is
transcribed line by line, and :meth:`RenkoCharts.to_frame` returns the
bricks as a bar DataFrame (``time, open, high, low, close, tick_volume,
spread, real_volume``) that can be saved as a dataset and charted.

Bars are read from :mod:`.terminal` (``PERIOD_M1`` of the symbol, as the
source does; set ``source_period`` to build from another timeframe).
Function-level ``static``\\ s of ``LoadPrice``/``UpdateRates`` are instance
attributes here (one RenkoCharts per symbol, as the indicators use it).
"""

from __future__ import annotations

import math

import pandas as pd

from . import terminal as T
from .mql_runtime import EMPTY_VALUE, NormalizeDouble

# enum ENUM_RENKO_TYPE / ENUM_RENKO_WINDOW
RENKO_TYPE_TICKS, RENKO_TYPE_PIPS, RENKO_TYPE_POINTS, RENKO_TYPE_R = 0, 1, 2, 3
RENKO_NO_WINDOW, RENKO_CURRENT_WINDOW, RENKO_NEW_WINDOW, RENKO_MINI_CHART = 0, 1, 2, 3


class _Rate:
    __slots__ = ("time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume")

    def __init__(self):
        self.time = 0
        self.open = self.high = self.low = self.close = 0.0
        self.tick_volume = self.real_volume = 0
        self.spread = 0


class RenkoCharts:
    def __init__(self, source_period: int = T.PERIOD_M1):
        self.renko_buffer: list[_Rate] = []
        self.renko_symbol = ""
        self.custom_symbol = ""
        self.renko_size = self.brick_size = 0.0
        self.up_wick = self.down_wick = 0.0
        self.tick_volumes = self.volumes = 0
        self.show_wicks = True
        self.open_time = True
        self.asymetric_reversal = False
        self.renko_type = RENKO_TYPE_TICKS
        self.digits = 5
        self.source_period = source_period
        self._last_time = 0
        self._last_tick_volume = self._last_volume = 0
        self._last_update = 0

    def _now(self) -> int:
        r = T.rates_for(self.renko_symbol, self.source_period)
        return int(r.time[-1]) if r is not None and len(r) else 0

    def Setup(self, symbol, type_=RENKO_TYPE_TICKS, size=20, wicks=True, times=True,
              asymetric=False) -> bool:
        if not symbol:
            return False
        r = T.rates_for(symbol, self.source_period) or T.rates_for(symbol)
        if r is None:
            return False                                 # SymbolSelect failed
        self.renko_symbol = symbol
        self.renko_type = type_
        self.renko_size = size
        self.show_wicks = wicks
        self.open_time = times
        self.asymetric_reversal = asymetric
        digits = r.SymbolInfoInteger(T.SYMBOL_DIGITS)
        points = r.SymbolInfoDouble(T.SYMBOL_POINT)
        tick_size = r.SymbolInfoDouble(T.SYMBOL_TRADE_TICK_SIZE)
        self.digits = digits
        pip_size = points * 10 if digits in (5, 3) else points
        if type_ == RENKO_TYPE_TICKS:
            self.brick_size = size * tick_size
        elif type_ == RENKO_TYPE_PIPS:
            self.brick_size = size * pip_size
        elif type_ == RENKO_TYPE_R:
            self.brick_size = size * tick_size - tick_size
        else:
            self.brick_size = size
        if self.brick_size <= 0:
            return False
        if self.brick_size < tick_size:
            self.brick_size = tick_size
        self.brick_size = NormalizeDouble(self.brick_size, digits)
        return True

    # ------------------------------------------------------------ bricks

    def AddOne(self, time: int = 0) -> int:
        buf = self.renko_buffer
        buf.append(_Rate())
        index = len(buf) - 1
        if index <= 0:
            return 0
        if time == 0:
            time = self._now()
        if not self.open_time:
            time = time - time % 86400
        prev = buf[index - 1]
        cur = buf[index]
        cur.time = prev.time + 60 if time <= prev.time else time
        cur.open = cur.high = cur.low = cur.close = prev.close
        cur.tick_volume = cur.real_volume = 0
        cur.spread = 0
        return index

    def CloseUp(self, points: float, time: int = 0, spread: int = 0) -> int:
        buf = self.renko_buffer
        index = len(buf) - 1
        cur, prev = buf[index], buf[index - 1]
        cur.open = prev.close if self.asymetric_reversal else prev.close + points - self.brick_size
        cur.high = prev.close + points
        cur.close = prev.close + points
        cur.low = self.down_wick if self.show_wicks else cur.open
        self.up_wick = self.down_wick = cur.close
        cur.tick_volume = self.tick_volumes
        cur.real_volume = self.volumes
        cur.spread = spread
        self.tick_volumes = self.volumes = 0
        return self.AddOne(time)

    def CloseDown(self, points: float, time: int = 0, spread: int = 0) -> int:
        buf = self.renko_buffer
        index = len(buf) - 1
        cur, prev = buf[index], buf[index - 1]
        cur.open = prev.close if self.asymetric_reversal else prev.close - points + self.brick_size
        cur.low = prev.close - points
        cur.close = prev.close - points
        cur.high = self.up_wick if self.show_wicks else cur.open
        self.up_wick = self.down_wick = cur.close
        cur.tick_volume = self.tick_volumes
        cur.real_volume = self.volumes
        cur.spread = spread
        self.tick_volumes = self.volumes = 0
        return self.AddOne(time)

    def LoadPrice(self, price: float, time: int = 0, tick_volume: int = 0, volume: int = 0,
                  spread: int = 0) -> int:
        if time == 0:
            time = self._now()
        buf = self.renko_buffer
        bs = self.brick_size
        index = len(buf) - 1
        if not buf:
            b0, b1 = _Rate(), _Rate()
            buf.extend([b0, b1])
            b1.time = time - 60
            b1.close = b1.high = NormalizeDouble(math.floor(price / bs) * bs, self.digits)
            b1.open = b1.low = b1.close - bs
            b0.time = time - 120
            b0.open = b0.low = b1.open - bs
            b0.high = b0.close = b1.open
            index = self.AddOne(time)
        if time != self._last_time:
            self._last_time = time
            self.tick_volumes += self._last_tick_volume
            self.volumes += self._last_volume
        self._last_tick_volume = tick_volume
        self._last_volume = volume
        self.up_wick = max(self.up_wick, price)
        self.down_wick = min(self.down_wick, price)
        if self.down_wick <= 0:
            self.down_wick = price

        def c(i):
            return self.renko_buffer[i].close

        if self.renko_type == RENKO_TYPE_R:
            if c(index - 1) > c(index - 2):
                if price > c(index - 1) + bs:
                    while price > c(index - 1) + bs:
                        index = self.CloseUp(bs, time, spread)
                elif price < c(index - 1) - bs * 2.0:
                    index = self.CloseDown(bs * 2.0, time, spread)
                    while price < c(index - 1) - bs:
                        index = self.CloseDown(bs, time, spread)
            if c(index - 1) < c(index - 2):
                if price < c(index - 1) - bs:
                    while price < c(index - 1) - bs:
                        index = self.CloseDown(bs, time, spread)
                elif price > c(index - 1) + bs * 2.0:
                    index = self.CloseUp(bs * 2.0, time, spread)
                    while price > c(index - 1) + bs:
                        index = self.CloseUp(bs, time, spread)
        else:
            if c(index - 1) >= c(index - 2):
                if price >= c(index - 1) + bs:
                    while price >= c(index - 1) + bs:
                        index = self.CloseUp(bs, time, spread)
                elif price <= c(index - 1) - bs * 2.0:
                    index = self.CloseDown(bs * 2.0, time, spread)
                    while price <= c(index - 1) - bs:
                        index = self.CloseDown(bs, time, spread)
            if c(index - 1) <= c(index - 2):
                if price <= c(index - 1) - bs:
                    while price <= c(index - 1) - bs:
                        index = self.CloseDown(bs, time, spread)
                elif price >= c(index - 1) + bs * 2.0:
                    index = self.CloseUp(bs * 2.0, time, spread)
                    while price >= c(index - 1) + bs:
                        index = self.CloseUp(bs, time, spread)
        cur = self.renko_buffer[index]
        cur.open = self.renko_buffer[index - 1].close
        cur.high = self.up_wick
        cur.low = self.down_wick
        cur.close = price
        cur.tick_volume = self.tick_volumes + tick_volume
        cur.real_volume = self.volumes + volume
        cur.spread = spread
        return index + 1

    def LoadPriceOHLC(self, t, o, h, l, cl, tick_volume=0, real_volume=0, spread=0) -> int:
        self.LoadPrice(o, t, 0, 0, spread)
        if cl > o:
            self.LoadPrice(l, t, 0, 0, spread)
            self.LoadPrice(h, t, 0, 0, spread)
        else:
            self.LoadPrice(h, t, 0, 0, spread)
            self.LoadPrice(l, t, 0, 0, spread)
        return self.LoadPrice(cl, t, tick_volume, real_volume, spread)

    def LoadFrom(self, start: int = 0) -> int:
        r = T.rates_for(self.renko_symbol, self.source_period)
        if r is None or not len(r):
            return 0
        if not self.renko_buffer:
            rows = range(max(0, len(r) - 1000000), len(r))
        else:
            rows = [i for i in range(len(r)) if r.time[i] >= start - 59]
        rows = list(rows)
        size = len(self.renko_buffer)
        if not rows:
            return 0
        if len(rows) == 1:
            i = rows[0]
            return self.LoadPrice(r.close[i], int(r.time[i]), int(r.tick_volume[i]),
                                  int(r.real_volume[i]), int(r.spread[i]))
        for i in rows:
            size = self.LoadPriceOHLC(int(r.time[i]), r.open[i], r.high[i], r.low[i], r.close[i],
                                      int(r.tick_volume[i]), int(r.real_volume[i]), int(r.spread[i]))
        return size

    def UpdateRates(self) -> int:
        size = self.LoadFrom(self._last_update)
        self._last_update = self._now()
        return size

    def ClearRates(self) -> int:
        self.renko_buffer = []
        return 0

    # ------------------------------------------------------------ access

    def _field(self, index: int, buffer: int) -> float:
        b = self.renko_buffer[index]
        if buffer == 0:
            return float(b.time)
        if buffer == 1:
            return b.open
        if buffer == 2:
            return b.high
        if buffer == 3:
            return b.low
        if buffer == 4:
            return b.close
        if buffer == 5:
            return float(b.tick_volume)
        if buffer == 6:
            return float(b.real_volume)
        if buffer == 7:
            return float(b.spread)
        if buffer == 8:
            return 1.0 if b.open < b.close else (0.0 if b.open == b.close else -1.0)
        return EMPTY_VALUE

    def GetValue(self, buffer: int = 0, index: int = -1) -> float:
        index = len(self.renko_buffer) - 1 if index < 0 else index
        if index < 0:
            return EMPTY_VALUE
        return self._field(index, buffer)

    def GetValueAsSeries(self, buffer: int = 0, index: int = -1) -> float:
        index = len(self.renko_buffer) - index
        index = len(self.renko_buffer) - 1 if index <= 0 else index - 1
        if index < 0:
            return EMPTY_VALUE
        return self._field(index, buffer)

    def GetSymbolName(self) -> str:
        return self.custom_symbol

    def to_frame(self) -> pd.DataFrame:
        """The bricks as this app's bar DataFrame."""
        b = self.renko_buffer
        return pd.DataFrame({
            "time": pd.to_datetime([x.time for x in b], unit="s"),
            "open": [x.open for x in b], "high": [x.high for x in b],
            "low": [x.low for x in b], "close": [x.close for x in b],
            "tick_volume": [x.tick_volume for x in b], "spread": [x.spread for x in b],
            "real_volume": [x.real_volume for x in b],
        })
