"""``AIV/Resources.mqh`` and ``AIV/Matrices.mqh`` (the "AIV" multi-symbol
synthetics library behind *PCA Synthetics* and *Relation*) — port.

The library loads several symbols' bars, aligns them on a common time grid
(``synchronize``), and turns them into return / equity / log / percentage
matrices for portfolio maths; it also has a small infix-expression evaluator
(``CExpression``) and a few trading helpers.

Bars come from :mod:`.terminal`: add one :class:`~.terminal.Rates` per symbol
(same timeframe) to the current :class:`~.terminal.Terminal`. A symbol the
terminal does not have is "not selectable", exactly as ``SymbolSelect``
fails in MT5 for an unknown name. Contract data the bars do not carry
(``SYMBOL_TRADE_TICK_VALUE``, ``SYMBOL_VOLUME_MIN``) is read from the
``Rates`` spec (``Rates(df, "EURUSD", PERIOD_H1, tick_value=1.0)``) and is 0
when absent — the value MT5 returns for an unknown property.

Not portable and kept as clearly failing stubs: ``getMargin`` (needs the
account's leverage/currency), ``getDeals`` (the account's deal history) and
``logData`` (writes ``debug.log`` in the terminal's sandbox; here it appends
to a file path you pass). ``AIV/Charts.mqh`` only draws chart objects.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from . import terminal as T
from .mql_runtime import MathLog, MathPow, NormalizeDouble, idiv


# ================================================================ structs


@dataclass
class SPoint:
    mAsk: float = 0.0
    mBid: float = 0.0
    mLow: float = 0.0
    mHigh: float = 0.0
    mOpen: float = 0.0
    mClose: float = 0.0
    mPoint: float = 0.0
    mSpread: float = 0.0
    mVolume: float = 0.0
    mTime: int = 0


@dataclass
class SSymbol:
    mName: str = ""
    mMean: float = 0.0
    mUnit: float = 0.0
    mOrder: float = 0.0


@dataclass
class SSeries:
    mSymbol: SSymbol = field(default_factory=SSymbol)
    mPoints: list = field(default_factory=list)


@dataclass
class SGroup:
    mName: str = ""
    mMessage: str = ""
    mPrice: float = 0.0
    mMean: float = 0.0


@dataclass
class SDeal:
    mEntry: int = 0
    mDirection: int = 0
    mTicket: int = 0
    mName: str = ""
    mPrice: float = 0.0
    mVolume: float = 0.0
    mSummary: float = 0.0
    mTime: int = 0


@dataclass
class SBet:
    mCount: float = 0.0
    mMinus: float = 0.0
    mPlus: float = 0.0


def _rates(symbol, period=T.PERIOD_CURRENT):
    return T.rates_for(symbol, period)


def _resize_points(points: list, n: int) -> None:
    while len(points) < n:
        points.append(SPoint())
    del points[n:]


# ============================================================ Resources


def pipsToMoney(symbol, volume, pips) -> float:
    r = _rates(symbol)
    if r is None:
        return 0.0
    step = r.SymbolInfoDouble(T.SYMBOL_TRADE_TICK_SIZE)
    value = float(r.spec.get("tick_value", 0.0))
    return pips * value * volume / step if step else 0.0


def maxPrecision() -> int:
    chart = T.current().chart
    v = float(chart.spec.get("volume_min", 0.01)) if chart is not None else 0.01
    digits = 0
    k = 1
    while k < 100 and int(v * k) == 0:
        k *= 10
        digits += 1
    return digits


def getMargin(symbol, volume, end=""):
    raise NotImplementedError("getMargin needs the trading account (leverage, currency)")


def isTradingTime(shours: str = "0:30-23:30", sdays: str = "0-6") -> bool:
    days = sdays.split("-")
    hours = shours.split("-")
    chart = T.current().chart
    now = int(chart.time[-1]) if chart is not None and len(chart) else 0
    o = T.TimeToStruct(now)

    def at(y, m, d, hm):
        hh, mm = (int(x) for x in hm.split(":"))
        import datetime as _dt
        base = _dt.datetime(y, m, 1) + _dt.timedelta(days=d - 1, hours=hh, minutes=mm)
        return int((base - _dt.datetime(1970, 1, 1)).total_seconds())

    H1 = at(o.year, o.mon, o.day, hours[0])
    day = o.day + 1 if hours[0] > hours[1] else o.day
    H2 = at(o.year, o.mon, day, hours[1])
    D1 = int(days[0])
    D2 = int(days[len(hours) - 1])
    return H1 <= now <= H2 and D1 <= o.day_of_week <= D2


def getTickCost(symbol, check: bool = False) -> float:
    r = _rates(symbol)
    if r is None:
        return 0.0
    cost = float(r.spec.get("tick_value", 0.0))
    if cost == 0:
        alt = _rates(symbol[3:] + "USD")
        if alt is not None:
            point = r.SymbolInfoDouble(T.SYMBOL_POINT)
            contract = r.SymbolInfoDouble(T.SYMBOL_TRADE_CONTRACT_SIZE)
            cross = float(alt.spec.get("tick_value", 0.0))
            cost = 0 if (cross == 0 and check) else (point * contract / cross if cross else 0.0)
    return cost


def getLastSymbolTime(symbol, period=T.PERIOD_CURRENT, start: int = 0) -> int:
    r = _rates(symbol, period)
    return r.iTime(start) if r is not None else 0


def getLastTime(series, period, start) -> int:
    startTime = 0
    for s in series:
        startTime = max(startTime, getLastSymbolTime(s.mSymbol.mName, period, start))
    return startTime


def EMA(current: float, previous: float, period: int) -> float:
    if period > 0:
        pr = 2.0 / (period + 1.0)
        return current * pr + previous * (1 - pr)
    return 0.0


def getTrades(deals, results: list, symbol=None, mode: int = 0) -> str:
    """Win/loss (or direction) runs as a text grid; fills ``results``."""
    results.clear()
    results.append(SSeries())
    index = position = 0
    for d in deals:
        if d.mName == symbol or d.mName is None:
            item = 0
            if mode == 0:
                item = 1 if d.mSummary > 0 else 0
            elif mode == 1:
                item = 1 if d.mDirection > 0 else 0
            _resize_points(results[index].mPoints, position + 1)
            results[index].mPoints[position].mPoint = item
            position += 1
            if item == 1:
                position = 0
                results.append(SSeries())
                index += 1
    longest = max((len(r.mPoints) for r in results), default=0)
    for r in results:
        while len(r.mPoints) < longest:
            r.mPoints.append(SPoint(mPoint=2))
    lines = []
    for r in results:
        lines.append(":".join(f"{p.mPoint:.0f}" for p in r.mPoints))
    return "\n".join(lines) + ("\n" if lines else "")


def getDeals(deals, symbol=None, entry=-1, direction=-1) -> int:
    raise NotImplementedError("getDeals reads the account's deal history (not available offline)")


def getNextSize(oppositeSize: float, index: float = 0) -> float:
    return NormalizeDouble(oppositeSize * max(index, 0), maxPrecision())


def logData(data: str, path: str = "debug.log") -> None:
    with open(path, "a", encoding="ascii", errors="replace") as fh:
        fh.write(data + "\r\n")


def getChain(codes: list, order: int) -> int:
    """Binary counter over ``codes`` in *series* order (index 0 = last
    element): add one; returns 0 after wrapping to all zeros."""
    n = len(codes)
    for k in range(order):
        i = n - 1 - k
        if codes[i] == 0:
            codes[i] = 1
            return 1
        codes[i] = 0
    return 0


_last_period_time = None


def isNewPeriod(bars: int = 0, period=T.PERIOD_CURRENT) -> int:
    global _last_period_time
    chart = T.current().chart
    if _last_period_time is None:
        _last_period_time = getLastSymbolTime(chart.symbol, chart.period)
    if getLastSymbolTime(chart.symbol, period) - _last_period_time > T.PeriodSeconds(period) * bars:
        _last_period_time = getLastSymbolTime(chart.symbol, period)
        return 1
    return 0


def getRandom(binary: bool, size: int = 0, rng=random) -> int:
    if size <= 0 or size >= 32768:
        size = 32768
    number = 1 + idiv(size * rng.randint(0, 32767), 32768)
    if binary:
        return 1 if number % 2 == 0 else -1
    return number


class CExpression:
    """Infix → postfix (shunting-yard) and evaluation with named variables;
    ``a / 0`` evaluates to 0 as in the source."""

    def __init__(self):
        self.separators = ["^", "/", "*", "+", "-", "(", ")"]
        self.separatorsCount = len(self.separators)

    def isOperator(self, v: str) -> bool:
        return v in self.separators

    @staticmethod
    def order(v: str) -> int:
        return {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}.get(v[:1], 0)

    @staticmethod
    def operation(a: float, b: float, op: str) -> float:
        x = op[:1]
        if x == "+":
            return a + b
        if x == "-":
            return a - b
        if x == "*":
            return a * b
        if x == "/":
            return 0 if b == 0 else a / b
        if x == "^":
            return MathPow(a, b)
        return 0

    def isHigher(self, a: str, b: str) -> bool:
        return self.order(a) >= self.order(b)

    def splitExpression(self, source: str) -> list:
        for s in self.separators:
            source = source.replace(s, " " + s + " ")
        while "  " in source:
            source = source.replace("  ", " ")
        return source.split(" ")

    def getExpression(self, source: str):
        """→ ``(queue_string, postfix_tokens)``."""
        parts = self.splitExpression(source)
        queue = ""
        stack = []
        for token in parts:
            if self.isOperator(token):
                if token == "(":
                    stack.append(token)
                elif token == ")":
                    while stack[-1] != "(":
                        queue += stack.pop() + " "
                    stack.pop()
                else:
                    o2 = stack[-1] if stack else ""
                    while self.isHigher(o2, token):
                        queue += stack.pop() + " "
                        o2 = stack[-1] if stack else ""
                    stack.append(token)
            else:
                queue += token + " "
        while stack:
            queue += stack.pop() + " "
        while "  " in queue:
            queue = queue.replace("  ", " ")
        return queue, queue.split(" ")

    def getResult(self, variables, names, values) -> float:
        items = list(variables)
        for k in range(len(names)):
            items = [values[k] if it == names[k] else it for it in items]
        stack = []
        for it in items:
            if self.isOperator(it):
                b = stack.pop() if stack else 0.0
                a = stack.pop() if stack else 0.0
                stack.append(self.operation(a, b, it))
            elif it != "":
                try:
                    stack.append(float(it))
                except ValueError:
                    stack.append(0.0)          # StringToDouble of a non-number
        return stack[0] if stack else 0.0


# ============================================================ Matrices


def copySeries(source, destination) -> None:
    for k in range(len(source)):
        d, s = destination[k], source[k]
        d.mSymbol.mName = s.mSymbol.mName
        d.mSymbol.mMean = s.mSymbol.mMean
        d.mSymbol.mUnit = s.mSymbol.mUnit
        d.mSymbol.mOrder = s.mSymbol.mOrder
        d.mPoints = [SPoint(**vars(p)) for p in s.mPoints]


def setupSeries(series: list, rows: int, cols: int) -> None:
    while len(series) < rows:
        series.append(SSeries())
    del series[rows:]
    for s in series:
        s.mSymbol.mMean = s.mSymbol.mUnit = s.mSymbol.mOrder = 0
        _resize_points(s.mPoints, cols)


def getBars(series, period, order) -> int:
    bars = 1000000
    for k in range(order):
        r = _rates(series[k].mSymbol.mName, period)
        bars = min(bars, len(r) if r is not None else 0)
        if bars < 1:
            return 0
    return bars


def seriesByName(series, order, name) -> int:
    for k in range(order):
        if series[k].mSymbol.mName == name:
            return k
    return -1


def _selectable(name: str) -> bool:
    return _rates(name) is not None


def listCombinations(series: list, names: str, end: str = "") -> int:
    syms = names.split(",")
    index = 0
    for a in syms:
        for b in syms:
            s1, s2 = a + b, b + a
            c1, c2 = _selectable(s1 + end), _selectable(s2 + end)
            c3 = seriesByName(series, index, s1 + end) < 0
            c4 = seriesByName(series, index, s2 + end) < 0
            if (c1 and c3) or (c2 and c4):
                if len(series) <= index:
                    series.append(SSeries())
                series[index].mSymbol.mName = (s1 if c1 else s2) + end
                index += 1
    del series[index:]
    return index


def listPairs(series: list, names: str, validate: bool = True) -> int:
    syms = names.split(",")
    index = 0
    for s in syms:
        inverse = s[3:6] + s[0:3] + s[6:]
        A = _selectable(s)
        B = _selectable(inverse)
        if A or not validate:
            name, order = s, 0
        elif B or not validate:
            name, order = inverse, 1
        else:
            continue
        if len(series) <= index:
            series.append(SSeries())
        series[index].mSymbol.mName = name
        series[index].mSymbol.mOrder = order
        index += 1
    del series[index:]
    return index


def isChannel(name: str, symbol=None) -> bool:
    Tq = Bq = ""
    L = len(name)
    E = 1
    k = 0
    while k < L:
        sT = name[k:k + 3]
        sB = name[k + 3:k + 6]
        D1 = Tq.find(sB)
        D2 = Bq.find(sT)
        if D1 > -1:
            Tq = Tq[:D1] + Tq[D1 + 3:]
        else:
            Bq += sB
        if D2 > -1:
            Bq = Bq[:D2] + Bq[D2 + 3:]
        else:
            Tq += sT
        k += E + 6
    return ((symbol is None and len(Tq) == 0 and len(Bq) == 0)
            or (len(Bq) == 0 and symbol is not None and Tq.find(symbol) > -1)
            or (len(Tq) == 0 and symbol is not None and Bq.find(symbol) > -1))


def getGroups(series, groups: list, symbol=None) -> int:
    K = len(series)
    codes = [0] * K
    while getChain(codes, K):
        name = "".join(series[k].mSymbol.mName + ":" if codes[K - 1 - k] else ""
                       for k in range(K))
        # (the source indexes codes[] after ArraySetAsSeries; k maps to K-1-k)
        if symbol is None or isChannel(name, symbol):
            groups.append(SGroup(mName=name[:-1]))
    return len(groups)


def logRange(series, results: list) -> str:
    lines = []
    results.clear()
    if series:
        N = len(series[0].mPoints)
        for n in range(N):
            C = W = 0
            for s in series:
                v = s.mPoints[n].mPoint
                if v < 2:
                    C += 1
                    if v == 1:
                        W += int(v)
            results.append(SBet(mCount=C, mMinus=C - W, mPlus=W))
            lines.append(f"{n} : {C} : {W} : {C - W}")
    return "\n".join(lines)


def getQuotes(series, period, order, depth, position) -> int:
    bars = min(getBars(series, period, order), depth)
    for k in range(order):
        r = _rates(series[k].mSymbol.mName, period)
        idx = None if r is None else (len(r) - position - bars, len(r) - position)
        if r is None or idx[1] <= 0:
            return 0
        lo, hi = max(0, idx[0]), idx[1]
        counted = hi - lo
        if counted < 1:
            return 0
        _resize_points(series[k].mPoints, max(len(series[k].mPoints), counted))
        for n in range(counted - 1, -1, -1):
            i = lo + n
            p = series[k].mPoints[n]
            p.mLow, p.mHigh, p.mOpen, p.mClose = r.low[i], r.high[i], r.open[i], r.close[i]
            p.mPoint = r.close[i]
            p.mSpread = float(r.spread[i])
            p.mVolume = float(r.tick_volume[i])
            p.mTime = int(r.time[i])
    return bars


def synchronize(series, period, order, depth, position, closes: bool = True) -> int:
    """Align ``order`` symbols on one time grid of ``depth`` bars ending at
    the latest bar among them (``position`` bars back), forward-filling a
    symbol's missing bars and skipping weekends."""
    bars = min(getBars(series, period, order), depth)
    lastTime = getLastTime(series, period, position)
    sec = T.PeriodSeconds(period)
    weekend = 2 * T.PeriodSeconds(T.PERIOD_D1)
    for k in range(order):
        r = _rates(series[k].mSymbol.mName, period)
        if r is None:
            return 0
        points = r.SymbolInfoDouble(T.SYMBOL_POINT)
        hi = len(r) - position
        lo = max(0, hi - bars)
        counted = hi - lo
        if counted < 1:
            return 0
        _resize_points(series[k].mPoints, max(len(series[k].mPoints), depth))
        P = series[k].mPoints
        index = counted - 1
        currentTime = lastTime
        series[k].mSymbol.mMean = 0
        last = P[depth - 1]
        i = lo + index
        last.mLow, last.mHigh, last.mOpen, last.mClose = r.low[i], r.high[i], r.open[i], r.close[i]
        last.mPoint = r.close[i] if closes else r.open[i]
        last.mSpread = r.spread[i] * points
        last.mTime = int(r.time[i])
        for n in range(depth - 1, -1, -1):
            if weekend >= sec:
                if T.TimeToStruct(currentTime).day_of_week == 0:
                    currentTime -= weekend
            i = lo + index
            if currentTime == int(r.time[i]):
                P[n].mSpread = r.spread[i] * points
                P[n].mPoint = r.close[i] if closes else r.open[i]
                P[n].mClose, P[n].mOpen = r.close[i], r.open[i]
                P[n].mHigh, P[n].mLow = r.high[i], r.low[i]
                index = index - 1 if index > 0 else index
            elif n < depth - 1:
                q = P[n + 1]
                P[n].mSpread, P[n].mPoint, P[n].mClose = q.mSpread, q.mPoint, q.mClose
                P[n].mOpen, P[n].mHigh, P[n].mLow = q.mOpen, q.mHigh, q.mLow
            P[n].mTime = currentTime
            series[k].mSymbol.mMean += P[n].mPoint
            currentTime -= sec
        series[k].mSymbol.mMean /= depth
    return bars


def getMinIndex(series, order) -> int:
    minIndex = 0
    mx, mn = 0.0, 1000000.0
    for k in range(order):
        cur_min = cur_max = series[k].mPoints[0].mPoint
        if abs(mn) > abs(cur_min) and abs(mx) > abs(cur_max):
            mn, mx = cur_min, cur_max
            minIndex = k
    return minIndex


def getReturnsMatrix(series, equity, order, depth, range_: int = 1) -> None:
    for k in range(order):
        equity[k].mSymbol.mName = series[k].mSymbol.mName
        S, E = series[k].mPoints, equity[k].mPoints
        for n in range(range_):
            E[n].mPoint = S[n].mPoint - S[0].mPoint
        for n in range(range_, depth):
            E[n].mPoint = S[n].mPoint - S[n - range_].mPoint


def getEquityMatrix(series, equity, order, depth, mean: bool = True) -> None:
    for k in range(order):
        cost = getTickCost(series[k].mSymbol.mName)
        equity[k].mSymbol.mMean = 0
        equity[k].mSymbol.mName = series[k].mSymbol.mName
        if series[k].mSymbol.mUnit == 0:
            series[k].mSymbol.mUnit = series[k].mPoints[0].mPoint
        for n in range(1, depth):
            equity[k].mPoints[n].mPoint = (series[k].mPoints[n].mPoint - series[k].mSymbol.mUnit) * cost
            equity[k].mSymbol.mMean += equity[k].mPoints[n].mPoint
        equity[k].mSymbol.mMean /= depth
    if mean:
        for k in range(order):
            for n in range(depth):
                equity[k].mPoints[n].mPoint -= equity[k].mSymbol.mMean


def getLogMatrix(series, equity, order, depth) -> None:
    for k in range(order):
        equity[k].mSymbol.mMean = 0
        equity[k].mSymbol.mName = series[k].mSymbol.mName
        for n in range(depth):
            equity[k].mPoints[n].mPoint = MathLog(series[k].mPoints[n].mPoint)
            equity[k].mSymbol.mMean += equity[k].mPoints[n].mPoint
        equity[k].mSymbol.mMean /= depth
    for k in range(order):
        for n in range(depth):
            equity[k].mPoints[n].mPoint -= equity[k].mSymbol.mMean


def getLimitMatrix(series, equity, order, depth) -> None:
    for k in range(order):
        equity[k].mSymbol.mMean = 0
        equity[k].mSymbol.mName = series[k].mSymbol.mName
        equity[k].mPoints[0].mPoint = series[k].mPoints[0].mPoint
        if series[k].mSymbol.mUnit == 0:
            series[k].mSymbol.mUnit = series[k].mPoints[0].mPoint
        for n in range(depth):
            equity[k].mPoints[n].mPoint = (series[k].mPoints[n].mPoint / series[k].mSymbol.mUnit - 1) * 100
