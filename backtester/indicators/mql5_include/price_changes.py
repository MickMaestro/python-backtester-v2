"""``fxsaber/PriceChanges/PriceChange.mqh`` + ``PriceChanges.mqh`` (fxsaber) —
port. ``fxsaber/PriceChanges/Error.mqh`` is just error-printing macros.

For every visible symbol, the relative price change between two times (on
M1 bars, price = (open+close)/2) and the largest swing inside the interval,
sorted by size. Symbols and bars come from :mod:`.terminal`: add an M1
:class:`~.terminal.Rates` per symbol (the source always reads
``PERIOD_M1``); a symbol without M1 data contributes no bars and a zero
change, as ``CopyRates`` failing does in MT5. ``SymbolInfoString``
description / profit currency for the ``SymbBase`` filter come from the
``Rates`` spec (``description=``, ``currency_profit=``).

``Chart.mqh`` (hides/restores chart decorations) and ``TwoVLines.mqh``
(reads the two vertical-line objects the user drags) are chart-UI and not
ported; pass the two times to :meth:`PRICECHANGES.Calc` directly.
"""

from __future__ import annotations

from . import terminal as T
from .mql_runtime import DBL_MAX


class PRICECHANGE:
    def __init__(self):
        self.Value = 0.0
        self.MinMax = 0.0
        self.Name = ""

    @staticmethod
    def NumToString(num, digits: int = 1) -> str:
        sign = "+" if num > 0 else ""
        return sign + (f"{num:.{digits}f}" if isinstance(num, float) else str(num))

    @staticmethod
    def _price(o, c):
        return (o + c) / 2

    def _rates(self, symb, t1, t2):
        r = T.rates_for(symb, T.PERIOD_M1)
        if r is None:
            return []
        lo, hi = sorted((int(t1), int(t2)))
        return [(r.open[i], r.close[i]) for i in range(len(r)) if lo <= r.time[i] <= hi]

    def CalcMinMax(self, rates) -> float:
        MaxLast = True
        mn, mx = DBL_MAX, -DBL_MAX
        for o, c in reversed(rates):
            p = self._price(o, c)
            if p > mx:
                mx = p
                MaxLast = False
            if p < mn:
                mn = p
                MaxLast = True
        return ((mx / mn if MaxLast else mn / mx) - 1) if mn != DBL_MAX else 0

    def Calc(self, Symb, Time1, Time2) -> None:
        rates = self._rates(Symb, Time1, Time2)
        p1 = self._price(*rates[0]) if rates else 1
        p2 = self._price(*rates[-1]) if rates else p1
        self.Value = p2 / p1 - 1
        self.MinMax = self.CalcMinMax(rates)
        self.Name = Symb

    def ToString(self, MaxValue: float = 0, current_symbol: str = "") -> str:
        s = f"{self.Name}: {self.NumToString(self.Value * 1e4)}%%"
        if MaxValue > 0:
            s += f" ({100 * abs(self.Value / MaxValue):.1f}%)"
        s += f", MinMax = {self.NumToString(self.MinMax * 1e4)}%%"
        if MaxValue < 0:
            s += f" ({100 * abs(self.MinMax / MaxValue):.1f}%)"
        if self.Name == current_symbol:
            s += " - current symbol."
        return s


class PRICECHANGES:
    def __init__(self):
        self.Changes: list[PRICECHANGE] = []
        self.Current = -1
        self.MaxValue = 0.0

    def _symbols(self):
        term = T.current()
        return sorted({sym for (sym, _per) in term._rates})

    @staticmethod
    def StringBetween(s, begin, end=None):
        if s is None:
            return None, None
        pos = s.find(begin) if begin is not None else 0
        if pos >= 0 or begin is None:
            pos = pos + len(begin) if begin is not None and pos >= 0 else 0
            pend = s.find(end, pos) if end is not None else -1
            res = s[pos: pend if pend >= 0 else None] if pend != pos else None
            rest = s[pend + len(end):] if pend >= 0 else None
            return (res or None), (rest or None)
        return None, s

    def _names(self, symb):
        r = T.rates_for(symb)
        spec = r.spec if r is not None else {}
        desc = spec.get("description", "")
        first, rest = self.StringBetween(desc, None, " vs ")
        return [first, rest, spec.get("currency_profit")]

    def IsIntersection(self, Symb1, Symb2) -> bool:
        n1, n2 = self._names(Symb1), self._names(Symb2)
        return any(a is not None and a == b for a in n1 for b in n2)

    def _sort(self, SortByMinMax: bool) -> int:
        self.MaxValue = -DBL_MAX
        self.Current = -1
        keyed = []
        for i, ch in enumerate(self.Changes):
            v = abs(ch.MinMax if SortByMinMax else ch.Value)
            keyed.append((v, i))
            if v > self.MaxValue:
                self.MaxValue = v
        keyed.sort()                       # ArraySort on [value, index] rows
        chart = T.current().chart
        current = chart.symbol if chart is not None else ""
        self.Changes = [self.Changes[i] for _, i in keyed]
        for i in range(len(self.Changes) - 1, -1, -1):
            if self.Current == -1 and self.Changes[i].Name == current:
                self.Current = i
        if SortByMinMax:
            self.MaxValue = -self.MaxValue
        return len(self.Changes)

    def Calc(self, Time1, Time2, SortByMinMax: bool = False, SymbBase=None) -> int:
        self.Changes = []
        for symb in reversed(self._symbols()):
            if SymbBase is None or self.IsIntersection(symb, SymbBase):
                ch = PRICECHANGE()
                ch.Calc(symb, Time1, Time2)
                self.Changes.append(ch)
        return self._sort(SortByMinMax)

    def _correct_index(self, index: int) -> int:
        size = len(self.Changes)
        return ((index % size) + size) % size

    def _line(self, index: int) -> str:
        chart = T.current().chart
        current = chart.symbol if chart is not None else ""
        return f"\n{len(self.Changes) - index:02d}: " + self.Changes[index].ToString(self.MaxValue, current)

    def ToString(self) -> str:
        s = self._line(self.Current) + "\n" if self.Current != -1 else ""
        for i in range(len(self.Changes) - 1, -1, -1):
            s += self._line(i)
        return s

    def GetNextSymbol(self) -> str:
        return self.Changes[self._correct_index(self.Current - 1)].Name

    def GetPrevSymbol(self) -> str:
        return self.Changes[self._correct_index(self.Current + 1)].Name

    def GetFirstSymbol(self) -> str:
        return self.Changes[-1].Name

    def IsCalc(self) -> bool:
        return bool(self.Changes)
