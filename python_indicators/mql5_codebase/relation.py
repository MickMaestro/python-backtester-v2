"""Relation — converted from MQL5: MQL5 Indicators/Relation - Chart Builder Legacy/Relation.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Relation', 'source': 'MQL5 Indicators/Relation - Chart Builder Legacy/Relation.mq5', 'folder': 'Relation - Chart Builder Legacy', 'inputs': [{'mql': 'InpDepth', 'py': 'InpDepth', 'param': 'InpDepth', 'type': 'int', 'default': 1500, 'label': '', 'sinput': False}, {'mql': 'InpAlign', 'py': 'InpAlign', 'param': 'InpAlign', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'InpTimePeriod', 'py': 'InpTimePeriod', 'param': 'InpTimePeriod', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'InpExpression', 'py': 'InpExpression', 'param': None, 'type': 'string', 'default': '2 ^ (1 + EURUSD.m) + EURUSD.m / 3.5 * GBPUSD.m', 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpDepth = _input('InpDepth', 1500)
InpAlign = _input('InpAlign', True)
InpTimePeriod = _input('InpTimePeriod', PERIOD_CURRENT)
InpExpression = _input('InpExpression', '2 ^ (1 + EURUSD.m) + EURUSD.m / 3.5 * GBPUSD.m')
iSize = 0
iDepth = 0
iLoader = 0
S0 = Arr(0, 0.0)
iNames = Arr(0, "")
iValues = Arr(0, "")
iTokens = Arr(0, "")
iExpression = None

class SPoint(MqlObject):
    _q_fields = ('mAsk', 'mBid', 'mLow', 'mHigh', 'mOpen', 'mClose', 'mPoint', 'mSpread', 'mVolume', 'mTime')
    def __init__(self, *args):
        self.mAsk = 0.0
        self.mBid = 0.0
        self.mLow = 0.0
        self.mHigh = 0.0
        self.mOpen = 0.0
        self.mClose = 0.0
        self.mPoint = 0.0
        self.mSpread = 0.0
        self.mVolume = 0.0
        self.mTime = 0

class SSymbol(MqlObject):
    _q_fields = ('mName', 'mMean', 'mUnit', 'mOrder')
    def __init__(self, *args):
        self.mName = ""
        self.mMean = 0.0
        self.mUnit = 0.0
        self.mOrder = 0.0

class SSeries(MqlObject):
    _q_fields = ('mSymbol', 'mPoints')
    def __init__(self, *args):
        self.mSymbol = SSymbol()
        self.mPoints = Arr(0, 0, factory=SPoint)

class SMatrix(MqlObject):
    _q_fields = ('mSymbol', 'mAsk', 'mBid', 'mLow', 'mHigh', 'mOpen', 'mClose', 'mPoint', 'mSpread', 'mVolume', 'mTime')
    def __init__(self, *args):
        self.mSymbol = SSymbol()
        self.mAsk = Arr(0, 0.0)
        self.mBid = Arr(0, 0.0)
        self.mLow = Arr(0, 0.0)
        self.mHigh = Arr(0, 0.0)
        self.mOpen = Arr(0, 0.0)
        self.mClose = Arr(0, 0.0)
        self.mPoint = Arr(0, 0.0)
        self.mSpread = Arr(0, 0.0)
        self.mVolume = Arr(0, 0.0)
        self.mTime = Arr(0, 0)

class SGroup(MqlObject):
    _q_fields = ('mName', 'mMessage', 'mPrice', 'mMean')
    def __init__(self, *args):
        self.mName = ""
        self.mMessage = ""
        self.mPrice = 0.0
        self.mMean = 0.0

class SDeal(MqlObject):
    _q_fields = ('mEntry', 'mDirection', 'mTicket', 'mName', 'mPrice', 'mVolume', 'mSummary', 'mTime')
    def __init__(self, *args):
        self.mEntry = 0
        self.mDirection = 0
        self.mTicket = 0
        self.mName = ""
        self.mPrice = 0.0
        self.mVolume = 0.0
        self.mSummary = 0.0
        self.mTime = 0

class SBet(MqlObject):
    _q_fields = ('mCount', 'mMinus', 'mPlus')
    def __init__(self, *args):
        self.mCount = 0.0
        self.mMinus = 0.0
        self.mPlus = 0.0

class CExpression(MqlObject):
    _q_fields = ('separators', 'separatorsCount')
    def __init__(self):
        self.separators = Arr(0, "")
        self.separatorsCount = 0
        operators = Arr.of(['^', '/', '*', '+', '-', '(', ')'], fill="")
        ArrayCopy(self.separators, operators)
        self.separatorsCount = ArraySize(self.separators)
    def isOperator(self, v):
        op = False
        k = 0
        while k < self.separatorsCount:
            if self.separators[k] == v:
                op = True
            k += 1
        return op
    def order(self, v):
        x = _char(StringGetCharacter(v, 0))
        _sw1 = x
        if _sw1 == 43:
            return 1
        elif _sw1 == 45:
            return 1
        elif _sw1 == 42:
            return 2
        elif _sw1 == 47:
            return 2
        elif _sw1 == 94:
            return 3
        return 0
    def operation(self, a, b, op):
        x = _char(StringGetCharacter(op, 0))
        _sw2 = x
        if _sw2 == 43:
            return a + b
        elif _sw2 == 45:
            return a - b
        elif _sw2 == 42:
            return a * b
        elif _sw2 == 47:
            return (0 if (b == 0) else _fdiv(a, b))
        elif _sw2 == 94:
            return MathPow(a, b)
        return 0.0
    def isHigher(self, a, b):
        return self.order(a) >= self.order(b)
    def splitExpression(self, source, expression):
        source = Box(source)
        k = 0
        while k < self.separatorsCount:
            StringReplace(source, self.separators[k], ' ' + self.separators[k] + ' ')
            k += 1
        while StringReplace(source, '  ', ' ') > 0:
            pass
        return StringSplit(source.v, 32, expression)
    def getExpression(self, source, expression):
        parts = Arr(0, "")
        self.splitExpression(source, parts)
        queue = Box('')
        operatorIndex = -1
        operatorStack = Arr.of([_str(0)], fill="", dyn=False, size=100)
        size = ArraySize(parts)
        for i in range(0, size):
            token = parts[i]
            if self.isOperator(token):
                if token == '(':
                    operatorIndex += 1
                    operatorStack[operatorIndex] = token
                elif token == ')':
                    while operatorStack[operatorIndex] != '(':
                        queue.v += operatorStack[operatorIndex] + ' '
                        operatorIndex -= 1
                    operatorIndex -= 1
                else:
                    o1 = token
                    o2 = (operatorStack[operatorIndex] if (operatorIndex >= 0) else '')
                    while self.isHigher(o2, o1):
                        queue.v += operatorStack[operatorIndex] + ' '
                        operatorIndex -= 1
                        o2 = (operatorStack[operatorIndex] if (operatorIndex >= 0) else '')
                    operatorIndex += 1
                    operatorStack[operatorIndex] = o1
            else:
                queue.v += token + ' '
        while operatorIndex >= 0:
            queue.v += operatorStack[operatorIndex] + ' '
            operatorIndex -= 1
        while StringReplace(queue, '  ', ' ') > 0:
            pass
        StringSplit(queue.v, 32, expression)
        return queue.v
    def getResult(self, variables, names, values):
        items = Arr(0, "")
        stackIndex = -1
        stack = Arr.of([0.0], fill=0.0, dyn=False, size=100)
        ArrayCopy(items, variables)
        count = ArraySize(items)
        evaluations = ArraySize(names)
        for k in range(0, evaluations):
            for n in range(0, count):
                if items[n] == names[k]:
                    items[n] = values[k]
        for k in range(0, count):
            if self.isOperator(items[k]):
                b = stack[stackIndex]
                stackIndex -= 1
                a = stack[stackIndex]
                stackIndex -= 1
                stackIndex += 1
                stack[stackIndex] = self.operation(a, b, items[k])
            elif items[k] != '':
                stackIndex += 1
                stack[stackIndex] = StringToDouble(items[k])
        return stack[0]

def pipsToMoney(symbol, volume, pips):
    step = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_SIZE)
    value = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
    return _fdiv(pips * value * volume, step)

def maxPrecision():
    digits = 0
    v = SymbolInfoDouble(Symbol(), SYMBOL_VOLUME_MIN)
    k = 1
    while k < 100 and MathFloor(v * k) == 0:
        pass
        k *= 10
        digits += 1
    return digits

def getMargin(symbol, volume, end=''):
    leverage = AccountInfoInteger(ACCOUNT_LEVERAGE)
    contract = SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE) * volume
    currency = StringSubstr(symbol, 0, 3) + AccountInfoString(ACCOUNT_CURRENCY) + end
    return _fdiv(SymbolInfoDouble(currency, SYMBOL_LAST) * contract, leverage)

def isTradingTime(shours='0:30-23:30', sdays='0-6'):
    days = Arr(0, "")
    hours = Arr(0, "")
    StringSplit(sdays, 45, days)
    StringSplit(shours, 45, hours)
    o = _struct_init(MqlDateTime(), [0])
    now = TimeCurrent(o)
    day = _str(o.year) + '.' + _str(o.mon) + '.' + _str(o.day)
    H1 = StringToTime(day + ' ' + hours[0])
    if hours[0] > hours[1]:
        day = _str(o.year) + '.' + _str(o.mon) + '.' + _str(o.day + 1)
    H2 = StringToTime(day + ' ' + hours[1])
    D1 = StringToInteger(days[0])
    D2 = StringToInteger(days[ArraySize(hours) - 1])
    if ((now >= H1 and now <= H2) and o.day_of_week >= D1) and o.day_of_week <= D2:
        return True
    return False

def getTickCost(symbol, check=False):
    cost = SymbolInfoDouble(symbol, SYMBOL_TRADE_TICK_VALUE)
    if cost == 0:
        altSymbol = StringSubstr(symbol, 3) + 'USD'
        if SymbolSelect(altSymbol, True):
            point = SymbolInfoDouble(symbol, SYMBOL_POINT)
            contract = SymbolInfoDouble(symbol, SYMBOL_TRADE_CONTRACT_SIZE)
            crossCost = SymbolInfoDouble(altSymbol, SYMBOL_TRADE_TICK_VALUE)
            cost = (0 if (crossCost == 0 and check) else _fdiv(point * contract, crossCost))
    return cost

def getLastSymbolTime(symbol, period=PERIOD_CURRENT, start=0):
    moment = Arr(0, 0)
    CopyTime(symbol, period, start, 1, moment)
    return moment[0]

def getLastTime(series, period, start):
    startTime = 0
    count = ArraySize(series)
    for k in range(0, count):
        startTime = MathMax(startTime, getLastSymbolTime(series[k].mSymbol.mName, period, start))
    return startTime

def EMA(current, previous, period):
    result = 0.0
    if period > 0:
        pr = _fdiv(2.0, period + 1.0)
        result = (current * pr) + (previous * (1 - pr))
    return result

def getTrades(deals, results, symbol=None, mode=0):
    result = ''
    index = 0
    position = 0
    K = ArraySize(deals)
    ArrayResize(results, index + 1)
    for k in range(0, K):
        if deals[k].mName == symbol or deals[k].mName == "":
            item = 0
            _sw3 = mode
            if _sw3 == 0:
                item = (1 if (deals[k].mSummary > 0) else 0)
            elif _sw3 == 1:
                item = (1 if (deals[k].mDirection > 0) else 0)
            ArrayResize(results[index].mPoints, position + 1)
            results[index].mPoints[position].mPoint = item
            position += 1
            if item == 1:
                position = 0
                ArrayResize(results, index + 2)
                ZeroMemory(results[index + 1])
                index += 1
    max_ = 0
    N = ArraySize(results)
    for k in range(0, N):
        M = ArraySize(results[k].mPoints)
        max_ = (M if (M > max_) else max_)
    for k in range(0, N):
        M = ArraySize(results[k].mPoints)
        for n in range(M, max_):
            ArrayResize(results[k].mPoints, n + 1)
            results[k].mPoints[n].mPoint = 2.0
    for k in range(0, N):
        M = ArraySize(results[k].mPoints)
        for n in range(0, M):
            result += DoubleToString(results[k].mPoints[n].mPoint, 0) + (':' if (n < (M - 1)) else '')
        result += '\n'
    return result

def getDeals(deals, symbol=None, entry=-1, direction=-1):
    ArrayResize(deals, 0)
    if HistorySelect(0, TimeCurrent()):
        index = 0
        count = HistoryDealsTotal()
        for k in range(0, count):
            ticket = HistoryDealGetTicket(k)
            route = HistoryDealGetInteger(ticket, DEAL_TYPE)
            deal = HistoryDealGetInteger(ticket, DEAL_ENTRY)
            A = entry == -1 or entry == deal
            B = direction == -1 or direction == route
            if A and B:
                ArrayResize(deals, index + 1)
                deals[index].mEntry = deal
                deals[index].mTicket = ticket
                deals[index].mName = HistoryDealGetString(ticket, DEAL_SYMBOL)
                deals[index].mPrice = HistoryDealGetDouble(ticket, DEAL_PRICE)
                deals[index].mSummary = HistoryDealGetDouble(ticket, DEAL_PROFIT)
                deals[index].mTime = HistoryDealGetInteger(ticket, DEAL_TIME)
                deals[index].mVolume = HistoryDealGetDouble(ticket, DEAL_VOLUME)
                deals[index].mDirection = (1 if (HistoryDealGetInteger(ticket, DEAL_TYPE) == DEAL_TYPE_BUY) else -1)
                index += 1
    return ArraySize(deals)

def getNextSize(oppositeSize, index=0.0):
    size = oppositeSize * MathMax(index, 0)
    return NormalizeDouble(size, maxPrecision())

def logData(data):
    FH = FileOpen('debug.log', ((FILE_WRITE | FILE_READ) | FILE_SHARE_READ) | FILE_ANSI)
    FileSeek(FH, 0, SEEK_END)
    FileWrite(FH, data)
    FileFlush(FH)
    FileClose(FH)

def getChain(codes, order):
    ArraySetAsSeries(codes, True)
    for k in range(0, order):
        if codes[k] == 0:
            codes[k] = 1
            return 1
        else:
            codes[k] = 0
    return 0

def isNewPeriod(bars=0, period=PERIOD_CURRENT):
    global _s_isNewPeriod_last
    if _s_isNewPeriod_last is _UNSET:
        _s_isNewPeriod_last = getLastSymbolTime(Symbol(), Period())
    if (_int(getLastSymbolTime(Symbol(), period)) - _int(_s_isNewPeriod_last)) > (PeriodSeconds(period) * bars):
        _s_isNewPeriod_last = getLastSymbolTime(Symbol(), period)
        return 1
    return 0

def getRandom(binary, size=0):
    if size <= 0 or size >= 32768:
        size = 32768
    number = 1 + _idiv(size * MathRand(), 32768)
    if binary:
        return (1 if (_imod(number, 2) == 0) else -1)
    return number

def copySeries(source, destination):
    N = ArraySize(source)
    for k in range(0, N):
        destination[k].mSymbol.mName = source[k].mSymbol.mName
        destination[k].mSymbol.mMean = source[k].mSymbol.mMean
        destination[k].mSymbol.mUnit = source[k].mSymbol.mUnit
        destination[k].mSymbol.mOrder = source[k].mSymbol.mOrder
        ArrayCopy(destination[k].mPoints, source[k].mPoints)

def setupSeries(series, rows, cols):
    ArrayResize(series, rows)
    for k in range(0, rows):
        series[k].mSymbol.mMean = 0.0
        series[k].mSymbol.mUnit = 0.0
        series[k].mSymbol.mOrder = 0.0
        ArrayResize(series[k].mPoints, cols)

def setupMatrix(series, rows, cols):
    ArrayResize(series, rows)
    for k in range(0, rows):
        series[k].mSymbol.mMean = 0.0
        series[k].mSymbol.mUnit = 0.0
        series[k].mSymbol.mOrder = 0.0
        ArrayResize(series[k].mAsk, cols)
        ArrayResize(series[k].mBid, cols)
        ArrayResize(series[k].mLow, cols)
        ArrayResize(series[k].mHigh, cols)
        ArrayResize(series[k].mOpen, cols)
        ArrayResize(series[k].mClose, cols)
        ArrayResize(series[k].mPoint, cols)
        ArrayResize(series[k].mSpread, cols)
        ArrayResize(series[k].mVolume, cols)
        ArrayResize(series[k].mTime, cols)

def getBars(series, period, order):
    bars = 1000000
    for k in range(0, order):
        rates = Arr(0, 0, factory=MqlRates)
        bars = MathMin(bars, Bars(series[k].mSymbol.mName, period))
        if bars < 1:
            Print('Synchronization : ' + (series[k].mSymbol.mName) + ', ' + 'Bars : ' + IntegerToString(bars))
            return 0
    return bars

def listCombinations(series, names, end=''):
    syms = Arr(0, "")
    index = 0
    count = StringSplit(names, 44, syms)
    for k in range(0, count):
        for n in range(0, count):
            s1 = syms[k] + syms[n]
            s2 = syms[n] + syms[k]
            c1 = SymbolSelect(s1 + end, True)
            c2 = SymbolSelect(s2 + end, True)
            c3 = seriesByName(series, index, s1 + end) < 0
            c4 = seriesByName(series, index, s2 + end) < 0
            c5 = SymbolInfoInteger(s1 + end, SYMBOL_TRADE_MODE) == SYMBOL_TRADE_MODE_FULL
            c6 = SymbolInfoInteger(s2 + end, SYMBOL_TRADE_MODE) == SYMBOL_TRADE_MODE_FULL
            if ((c1 and c3) and c5) or ((c2 and c4) and c6):
                ArrayResize(series, index + 1)
                series[index].mSymbol.mName = (s1 if c1 else s2) + end
                index += 1
    return index

def listPairs(series, names, validate=True):
    syms = Arr(0, "")
    index = 0
    count = StringSplit(names, 44, syms)
    for k in range(0, count):
        inverse = StringSubstr(syms[k], 3, 3) + StringSubstr(syms[k], 0, 3) + StringSubstr(syms[k], 6)
        A = SymbolSelect(syms[k], True) and SymbolInfoInteger(syms[k], SYMBOL_TRADE_MODE) == SYMBOL_TRADE_MODE_FULL
        B = SymbolSelect(inverse, True) and SymbolInfoInteger(inverse, SYMBOL_TRADE_MODE) == SYMBOL_TRADE_MODE_FULL
        if A or validate == False:
            ArrayResize(series, index + 1)
            series[index].mSymbol.mName = syms[k]
            series[index].mSymbol.mOrder = 0.0
            index += 1
        elif B or validate == False:
            ArrayResize(series, index + 1)
            series[index].mSymbol.mName = inverse
            series[index].mSymbol.mOrder = 1.0
            index += 1
    return index

def getGroups(series, groups, symbol=None):
    n = 0
    codes = Arr(0, 0)
    K = ArraySize(series)
    ArrayResize(codes, K)
    ArrayFill(codes, 0, K, 0)
    while getChain(codes, K):
        name = ""
        for k in range(0, K):
            name += (((series[k].mSymbol.mName) + ':') if codes[k] else '')
        if symbol == "" or isChannel(name, symbol):
            ArrayResize(groups, n + 1)
            groups[((n := n + 1) - 1)].mName = StringSubstr(name, 0, StringLen(name) - 1)
    return ArraySize(groups)

def isChannel(name, symbol=None):
    T_ = Box("")
    B = Box("")
    sT = ""
    sB = ""
    ZeroMemory(T_)
    ZeroMemory(B)
    L = StringLen(name)
    E = StringLen(':')
    k = 0
    while k < L:
        sT = StringSubstr(name, k, 3)
        sB = StringSubstr(name, k + 3, 3)
        D1 = StringFind(T_.v, sB)
        D2 = StringFind(B.v, sT)
        if D1 > -1:
            T_.v = StringSubstr(T_.v, 0, D1) + StringSubstr(T_.v, D1 + 3, StringLen(T_.v))
        else:
            B.v += sB
        if D2 > -1:
            B.v = StringSubstr(B.v, 0, D2) + StringSubstr(B.v, D2 + 3, StringLen(B.v))
        else:
            T_.v += sT
        k += E + 6
    return (((symbol == "" and StringLen(T_.v) == 0) and StringLen(B.v) == 0) or (StringLen(B.v) == 0 and StringFind(T_.v, symbol) > -1)) or (StringLen(T_.v) == 0 and StringFind(B.v, symbol) > -1)

def logRange(series, results):
    bets = ''
    K = ArraySize(series)
    if K > 0:
        N = ArraySize(series[0].mPoints)
        ArrayResize(results, N)
        for n in range(0, N):
            C = 0
            W = 0
            for k in range(0, K):
                if series[k].mPoints[n].mPoint < 2:
                    C += 1
                    if series[k].mPoints[n].mPoint == 1:
                        W += _int(series[k].mPoints[n].mPoint)
            results[n].mPlus = W
            results[n].mCount = C
            results[n].mMinus = C - W
            bets += IntegerToString(n) + ' : ' + IntegerToString(C) + ' : ' + IntegerToString(W) + ' : ' + IntegerToString(C - W) + ('\n' if (n < (N - 1)) else '')
    return bets

def getQuotes(series, period, order, depth, position):
    bars = MathMin(getBars(series, period, order), depth)
    for k in range(0, order):
        rates = Arr(0, 0, factory=MqlRates)
        counted = CopyRates(series[k].mSymbol.mName, period, position, bars, rates)
        if counted < 1:
            Print('Synchronization : ' + (series[k].mSymbol.mName) + ', ' + 'Position : ' + IntegerToString(position) + ', ' + 'Depth : ' + IntegerToString(depth) + ', ' + 'Bars : ' + IntegerToString(bars))
            return 0
        index = counted - 1
        for n in range(index, -1, -1):
            series[k].mPoints[n].mLow = rates[n].low
            series[k].mPoints[n].mHigh = rates[n].high
            series[k].mPoints[n].mOpen = rates[n].open
            series[k].mPoints[n].mClose = rates[n].close
            series[k].mPoints[n].mPoint = rates[n].close
            series[k].mPoints[n].mSpread = rates[n].spread
            series[k].mPoints[n].mVolume = float(rates[n].tick_volume)
            series[k].mPoints[n].mTime = rates[n].time
    return bars

def synchronize(series, period, order, depth, position, closes=True):
    bars = MathMin(getBars(series, period, order), depth)
    lastTime = getLastTime(series, period, position)
    for k in range(0, order):
        rates = Arr(0, 0, factory=MqlRates)
        currentTime = lastTime
        points = SymbolInfoDouble(series[k].mSymbol.mName, SYMBOL_POINT)
        counted = CopyRates(series[k].mSymbol.mName, period, position, bars, rates)
        if counted < 1:
            Print('Synchronization : ' + (series[k].mSymbol.mName) + ', ' + 'Position : ' + IntegerToString(position) + ', ' + 'Depth : ' + IntegerToString(depth) + ', ' + 'Bars : ' + IntegerToString(bars))
            return 0
        index = counted - 1
        series[k].mSymbol.mMean = 0.0
        series[k].mPoints[depth - 1].mLow = rates[index].low
        series[k].mPoints[depth - 1].mHigh = rates[index].high
        series[k].mPoints[depth - 1].mOpen = rates[index].open
        series[k].mPoints[depth - 1].mClose = rates[index].close
        series[k].mPoints[depth - 1].mPoint = (rates[index].close if closes else rates[index].open)
        series[k].mPoints[depth - 1].mSpread = rates[index].spread * points
        series[k].mPoints[depth - 1].mTime = rates[index].time
        dates = _struct_init(MqlDateTime(), [0])
        secondsInPeriod = PeriodSeconds(period)
        secondsInWeekend = 2 * PeriodSeconds(PERIOD_D1)
        for n in range(depth - 1, 0 - 1, -1):
            if secondsInWeekend >= secondsInPeriod:
                TimeToStruct(currentTime, dates)
                if dates.day_of_week == 0:
                    currentTime -= secondsInWeekend
            if currentTime == rates[index].time:
                series[k].mPoints[n].mSpread = rates[index].spread * points
                series[k].mPoints[n].mPoint = (rates[index].close if closes else rates[index].open)
                series[k].mPoints[n].mClose = rates[index].close
                series[k].mPoints[n].mOpen = rates[index].open
                series[k].mPoints[n].mHigh = rates[index].high
                series[k].mPoints[n].mLow = rates[index].low
                index = ((index - 1) if (index > 0) else index)
            elif n < (depth - 1):
                series[k].mPoints[n].mSpread = series[k].mPoints[n + 1].mSpread
                series[k].mPoints[n].mPoint = series[k].mPoints[n + 1].mPoint
                series[k].mPoints[n].mClose = series[k].mPoints[n + 1].mClose
                series[k].mPoints[n].mOpen = series[k].mPoints[n + 1].mOpen
                series[k].mPoints[n].mHigh = series[k].mPoints[n + 1].mHigh
                series[k].mPoints[n].mLow = series[k].mPoints[n + 1].mLow
            series[k].mPoints[n].mTime = currentTime
            series[k].mSymbol.mMean += series[k].mPoints[n].mPoint
            currentTime -= PeriodSeconds(period)
        series[k].mSymbol.mMean = _fdiv(series[k].mSymbol.mMean, depth)
    return bars

def seriesByName(series, order, name):
    for k in range(0, order):
        if (series[k].mSymbol.mName) == name:
            return k
    return -1

def getMinIndex(series, order):
    minIndex = 0
    max_ = 0.0
    min_ = 1000000.0
    for k in range(0, order):
        currentMin = series[k].mPoints[0].mPoint
        currentMax = series[k].mPoints[0].mPoint
        if MathAbs(min_) > MathAbs(currentMin) and MathAbs(max_) > MathAbs(currentMax):
            min_ = currentMin
            max_ = currentMax
            minIndex = k
    return minIndex

def getReturnsMatrix(series, equity, order, depth, range_=1):
    for k in range(0, order):
        equity[k].mSymbol.mName = series[k].mSymbol.mName
        for n in range(0, range_):
            equity[k].mPoints[n].mPoint = series[k].mPoints[n].mPoint - series[k].mPoints[0].mPoint
        for n in range(range_, depth):
            equity[k].mPoints[n].mPoint = series[k].mPoints[n].mPoint - series[k].mPoints[n - range_].mPoint

def getEquityMatrix(series, equity, order, depth, mean=True):
    for k in range(0, order):
        cost = getTickCost(series[k].mSymbol.mName)
        equity[k].mSymbol.mMean = 0.0
        equity[k].mSymbol.mName = series[k].mSymbol.mName
        series[k].mSymbol.mUnit = (series[k].mPoints[0].mPoint if ((series[k].mSymbol.mUnit) == 0) else (series[k].mSymbol.mUnit))
        equity[k].mPoints[0].mPoint = equity[k].mPoints[0].mPoint
        for n in range(1, depth):
            equity[k].mPoints[n].mPoint = (series[k].mPoints[n].mPoint - (series[k].mSymbol.mUnit)) * cost
            equity[k].mSymbol.mMean += equity[k].mPoints[n].mPoint
        equity[k].mSymbol.mMean = _fdiv(equity[k].mSymbol.mMean, depth)
    if mean:
        for k in range(0, order):
            for n in range(0, depth):
                equity[k].mPoints[n].mPoint -= equity[k].mSymbol.mMean

def getLogMatrix(series, equity, order, depth):
    for k in range(0, order):
        equity[k].mSymbol.mMean = 0.0
        equity[k].mSymbol.mName = series[k].mSymbol.mName
        for n in range(0, depth):
            equity[k].mPoints[n].mPoint = MathLog(series[k].mPoints[n].mPoint)
            equity[k].mSymbol.mMean += equity[k].mPoints[n].mPoint
        equity[k].mSymbol.mMean = _fdiv(equity[k].mSymbol.mMean, depth)
    for k in range(0, order):
        for n in range(0, depth):
            equity[k].mPoints[n].mPoint -= equity[k].mSymbol.mMean

def getLimitMatrix(series, equity, order, depth):
    for k in range(0, order):
        equity[k].mSymbol.mMean = 0.0
        equity[k].mSymbol.mName = series[k].mSymbol.mName
        equity[k].mPoints[0].mPoint = series[k].mPoints[0].mPoint
        series[k].mSymbol.mUnit = (series[k].mPoints[0].mPoint if ((series[k].mSymbol.mUnit) == 0) else (series[k].mSymbol.mUnit))
        for n in range(0, depth):
            equity[k].mPoints[n].mPoint = (_fdiv(series[k].mPoints[n].mPoint, series[k].mSymbol.mUnit) - 1) * 100

def OnDeinit(reason):
    _delete(iExpression)

def OnInit():
    global iDepth, iExpression, iLoader, iSize
    SetIndexBuffer(0, S0, INDICATOR_DATA)
    ArraySetAsSeries(S0, True)
    ArrayInitialize(S0, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, 5)
    IndicatorSetString(INDICATOR_SHORTNAME, InpExpression)
    duplicates = ''
    iExpression = CExpression()
    expression = iExpression.getExpression(InpExpression, iTokens)
    tokens = ArraySize(iTokens)
    for k in range(0, tokens):
        if StringFind(duplicates, iTokens[k]) < 0 and SymbolSelect(iTokens[k], True):
            symbols = ArraySize(iSeries)
            ArrayResize(iSeries, symbols + 1)
            iSeries[symbols].mSymbol.mName = iTokens[k]
            duplicates += iTokens[k]
    iLoader = 0
    iDepth = InpDepth
    iSize = ArraySize(iSeries)
    ArrayResize(iNames, iSize)
    ArrayResize(iValues, iSize)
    setupSeries(iSeries, iSize, iDepth)
    setupSeries(iCharts, iSize, iDepth)
    EventSetMillisecondTimer(500)
    return 0

def OnTimer():
    global iDepth, iLoader
    bars = Bars(Symbol(), InpTimePeriod)
    if iDepth > bars:
        iDepth = MathMin(bars - 1, iDepth)
    if synchronize(iSeries, InpTimePeriod, iSize, iDepth, 0, False) < 1:
        return
    iLoader = 1
    Calculate()
    ChartRedraw(ChartID())
    EventKillTimer()

def OnCalculate(bars, counted, start, price):
    if iLoader == 1:
        Calculate()
    return bars

def Calculate():
    records = (getQuotes(iSeries, InpTimePeriod, iSize, iDepth, 0) if (PeriodSeconds(PERIOD_CURRENT) >= PeriodSeconds(PERIOD_D1)) else synchronize(iSeries, InpTimePeriod, iSize, iDepth, 0, False))
    if records < 1:
        return 0
    if InpAlign:
        getEquityMatrix(iSeries, iCharts, iSize, records, False)
    index = 0
    bars = ArraySize(S0)
    for k in range(records - 1, 0 - 1, -1):
        for n in range(0, iSize):
            iNames[n] = iSeries[n].mSymbol.mName
            iValues[n] = DoubleToString((iCharts[n].mPoints[k].mPoint if InpAlign else iSeries[n].mPoints[k].mPoint))
        if index >= (bars - 1):
            break
        S0[index] = iExpression.getResult(iTokens, iNames, iValues)
        index += 1
    return 1

# ---- global variables initialised from expressions
iSeries = Arr(0, 0, factory=SSeries)
iCharts = Arr(0, 0, factory=SSeries)

# ---- static local variables
_s_isNewPeriod_last = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Relation(_MQL5Indicator):
    name = 'Relation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDepth': 1500,
        'InpAlign': True,
        'InpTimePeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

