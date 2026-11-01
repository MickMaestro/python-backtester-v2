"""``Candlestick.mqh`` (MetaQuotes, 2019) — line-by-line port.

``cCandlestick.mvGetCandleStickCharateristics(symbol, i)`` reads bar ``i``
(0 = newest) of the chart timeframe through :mod:`.mql4_compat` and measures
its range, body and wicks in points (``NormalizeDouble(..., _Digits)``), then
classifies it as doji / bull / bear.

Note from the source: a bar with ``open == close`` that is not a doji (its
body is ≤ 1 point but a wick is not longer than the body) leaves the three
flags as they were from the previous call.
"""

from __future__ import annotations

from . import terminal as T
from .mql4_compat import MODE_POINT, MarketInfoMQL4, iCloseMQL4, iHighMQL4, iLowMQL4, iOpenMQL4
from .mql_runtime import MathAbs, NormalizeDouble, fdiv


class cCandlestick:
    def __init__(self):
        self.dOpenPrice = self.dHighPrice = self.dLowPrice = self.dClosePrice = 0.0
        self.dRangeCandle = self.dBodyCandle = 0.0
        self.dUpperWickCandle = self.dLowerWickCandle = 0.0
        self.bBullCandle = self.bBearCandle = self.bDojiCandle = False

    def mvGetCandleStickCharateristics(self, s, i) -> None:
        self.dOpenPrice = iOpenMQL4(s, T.PERIOD_CURRENT, i)
        self.dHighPrice = iHighMQL4(s, T.PERIOD_CURRENT, i)
        self.dLowPrice = iLowMQL4(s, T.PERIOD_CURRENT, i)
        self.dClosePrice = iCloseMQL4(s, T.PERIOD_CURRENT, i)
        point = MarketInfoMQL4(s, MODE_POINT)
        r = T.rates_for(s)
        digits = r.SymbolInfoInteger(T.SYMBOL_DIGITS) if r is not None else 5
        self.dRangeCandle = NormalizeDouble(fdiv(MathAbs(self.dHighPrice - self.dLowPrice), point), digits)
        self.dBodyCandle = NormalizeDouble(fdiv(MathAbs(self.dOpenPrice - self.dClosePrice), point), digits)
        self.dUpperWickCandle = NormalizeDouble(
            fdiv(MathAbs(self.dHighPrice - max(self.dClosePrice, self.dOpenPrice)), point), digits)
        self.dLowerWickCandle = NormalizeDouble(
            fdiv(MathAbs(min(self.dClosePrice, self.dOpenPrice) - self.dLowPrice), point), digits)
        if (self.dBodyCandle <= 1.0 and self.dUpperWickCandle > self.dBodyCandle
                and self.dLowerWickCandle > self.dBodyCandle):
            self.bDojiCandle, self.bBullCandle, self.bBearCandle = True, False, False
        elif self.dOpenPrice < self.dClosePrice:
            self.bDojiCandle, self.bBullCandle, self.bBearCandle = False, True, False
        elif self.dOpenPrice > self.dClosePrice:
            self.bDojiCandle, self.bBullCandle, self.bBearCandle = False, False, True
