"""UnityPro — converted from MQL5: MQL5 Indicators/Unity Pro/UnityPro.mq5

Multi-asset cluster indicator taking all currencies as a sum of values forming market unity (1.0)
Copyright: 2018-2019 © Marketeer; Link: https://www.mql5.com/en/users/marketeer; Version: 2.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.csom_indarray import *  # #include IndArray.mqh
from backtester.mql5.lib.csom_hashmaptemplate import *  # #include HashMapTemplate.mqh

MQL5_META = {'props': {'copyright': '2018-2019 © Marketeer', 'link': 'https://www.mql5.com/en/users/marketeer', 'version': '2.0', 'window': 'separate', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {1: [32768], 2: [9109504], 3: [255], 4: [8421504], 5: [4163021], 6: [55295], 7: [8388736], 8: [8421376], 9: [9498256], 10: [15128749], 11: [42495], 12: [13882323], 13: [2763429], 14: [65535], 15: [16711935], 16: [8421504], 17: [8421504], 18: [13882323], 19: [13882323]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Multi-asset cluster indicator taking all currencies as a sum of values forming market unity (1.0)'], 'name': 'UnityPro', 'source': 'MQL5 Indicators/Unity Pro/UnityPro.mq5', 'folder': 'Unity Pro', 'inputs': [{'mql': '_1', 'py': '_1', 'param': None, 'type': 'string', 'default': '', 'label': 'Cluster Indicator Settings', 'sinput': False}, {'mql': 'Instruments', 'py': 'Instruments', 'param': None, 'type': 'string', 'default': 'EURUSD,GBPUSD,USDCHF,USDJPY,AUDUSD,USDCAD,NZDUSD', 'label': '·    Instruments', 'sinput': False}, {'mql': 'BarLimit', 'py': 'BarLimit', 'param': 'BarLimit', 'type': 'int', 'default': 1000, 'label': '·    BarLimit', 'sinput': False}, {'mql': 'Draw', 'py': 'Draw', 'param': 'Draw', 'type': 'int', 'default': 1, 'label': '·    Draw', 'sinput': False}, {'mql': 'PriceType', 'py': 'PriceType', 'param': 'PriceType', 'type': 'int', 'default': 1, 'label': '·    PriceType', 'sinput': False}, {'mql': 'PriceMethod', 'py': 'PriceMethod', 'param': 'PriceMethod', 'type': 'int', 'default': 1, 'label': '·    PriceMethod', 'sinput': False}, {'mql': 'PricePeriod', 'py': 'PricePeriod', 'param': 'PricePeriod', 'type': 'int', 'default': 1, 'label': '·    PricePeriod', 'sinput': False}, {'mql': 'AbsoluteValues', 'py': 'AbsoluteValues', 'param': 'AbsoluteValues', 'type': 'bool', 'default': False, 'label': '·    AbsoluteValues', 'sinput': False}, {'mql': 'Momentum', 'py': 'Momentum', 'param': 'Momentum', 'type': 'double', 'default': 0.0, 'label': '·    Momentum [0..1]', 'sinput': False}, {'mql': 'Sigma1', 'py': 'Sigma1', 'param': 'Sigma1', 'type': 'double', 'default': 1.0, 'label': '·    Deviation Level Sigma 1 [0..3]', 'sinput': False}, {'mql': 'Sigma2', 'py': 'Sigma2', 'param': 'Sigma2', 'type': 'double', 'default': 2.0, 'label': '·    Deviation Level Sigma 2 [0..3]', 'sinput': False}, {'mql': '_2', 'py': '_2', 'param': None, 'type': 'string', 'default': '', 'label': 'Data Export to CSV file', 'sinput': False}, {'mql': 'SaveToFile', 'py': 'SaveToFile', 'param': None, 'type': 'string', 'default': '', 'label': '·    SaveToFile', 'sinput': False}, {'mql': 'ShiftLastBuffer', 'py': 'ShiftLastBuffer', 'param': 'ShiftLastBuffer', 'type': 'bool', 'default': False, 'label': '·    ShiftLastBuffer', 'sinput': False}, {'mql': 'BarLookback', 'py': 'BarLookback', 'param': 'BarLookback', 'type': 'int', 'default': 1, 'label': '·    BarLookback', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['IndArray.mqh', 'HashMapTemplate.mqh']}

# ---- inputs and global variables
_1 = _input('_1', '')  # Cluster Indicator Settings
Instruments = _input('Instruments', 'EURUSD,GBPUSD,USDCHF,USDJPY,AUDUSD,USDCAD,NZDUSD')  # ·    Instruments
BarLimit = _input('BarLimit', 1000)  # ·    BarLimit
Draw = _input('Draw', DRAW_LINE)  # ·    Draw
PriceType = _input('PriceType', PRICE_CLOSE)  # ·    PriceType
PriceMethod = _input('PriceMethod', MODE_EMA)  # ·    PriceMethod
PricePeriod = _input('PricePeriod', 1)  # ·    PricePeriod
AbsoluteValues = _input('AbsoluteValues', False)  # ·    AbsoluteValues
Momentum = _input('Momentum', 0.0)  # ·    Momentum [0..1]
Sigma1 = _input('Sigma1', 1.0)  # ·    Deviation Level Sigma 1 [0..3]
Sigma2 = _input('Sigma2', 2.0)  # ·    Deviation Level Sigma 2 [0..3]
_2 = _input('_2', '')  # Data Export to CSV file
SaveToFile = _input('SaveToFile', '')  # ·    SaveToFile
ShiftLastBuffer = _input('ShiftLastBuffer', False)  # ·    ShiftLastBuffer
BarLookback = _input('BarLookback', 1)  # ·    BarLookback
ShiftedBuffer = -1
initDone = False
Symbols = Arr(0, "")
Direction = Arr(0, 0)
Contracts = Arr(0, 0.0)
Handles = Arr(0, 0)
SymbolCount = 0
baseIndex = 0
BaseCurrency = ""
LastBarCount = 0

def initSymbols():
    global BaseCurrency, ShiftedBuffer, SymbolCount, baseIndex
    SymbolCount = StringSplit(Instruments, 44, Symbols)
    if SymbolCount >= 15:
        SymbolCount = 15 - 1
        ArrayResize(Symbols, SymbolCount)
    elif SymbolCount == 0:
        SymbolCount = 1
        ArrayResize(Symbols, SymbolCount)
        Symbols[0] = Symbol()
    ArrayResize(Direction, SymbolCount)
    ArrayInitialize(Direction, 0)
    ArrayResize(Contracts, SymbolCount)
    ArrayInitialize(Contracts, 1)
    ArrayResize(Handles, SymbolCount)
    ArrayInitialize(Handles, INVALID_HANDLE)
    base = ""
    i = 0
    while i < SymbolCount:
        if not SymbolSelect(Symbols[i], True):
            Print("Can't select ", Symbols[i])
            return False
        first = ""
        second = ""
        first = SymbolInfoString(Symbols[i], SYMBOL_CURRENCY_BASE)
        second = SymbolInfoString(Symbols[i], SYMBOL_CURRENCY_PROFIT)
        if first != second:
            workCurrencies.inc(_copy(first), 1)
            workCurrencies.inc(_copy(second), 1)
        else:
            workCurrencies.inc(_copy(Symbols[i]), 1)
        i += 1
    if workCurrencies.getSize() >= 15:
        Print('Too many symbols, max ', 15 - 1)
        return False
    if ShiftLastBuffer:
        ShiftedBuffer = workCurrencies.getSize() - 1
    i = 0
    while i < workCurrencies.getSize():
        if workCurrencies[i] > 1:
            if base == "":
                base = _str(workCurrencies.getKey(i))
                baseIndex = i
            else:
                Print('Collision: multiple base symbols: ', base, '[', workCurrencies[base], '] ', workCurrencies.getKey(i), '[', workCurrencies[i], ']')
                return False
        i += 1
    BaseCurrency = base
    for i in range(0, SymbolCount):
        if SymbolInfoString(Symbols[i], SYMBOL_CURRENCY_PROFIT) == base:
            Direction[i] = 1
        elif SymbolInfoString(Symbols[i], SYMBOL_CURRENCY_BASE) == base:
            Direction[i] = -1
        else:
            Print('Ambiguous symbol direction ', Symbols[i], ', defaults used')
            Direction[i] = 1
        Contracts[i] = SymbolInfoDouble(Symbols[i], SYMBOL_TRADE_CONTRACT_SIZE)
        Handles[i] = iMA(Symbols[i], PERIOD_CURRENT, PricePeriod, 0, PriceMethod, PriceType)
    return True

def OnInit():
    global LastBarCount, ShiftedBuffer, initDone
    ShiftedBuffer = -1
    initDone = False
    if not initSymbols():
        return INIT_PARAMETERS_INCORRECT
    base = SymbolInfoString(Symbol(), SYMBOL_CURRENCY_BASE)
    profit = SymbolInfoString(Symbol(), SYMBOL_CURRENCY_PROFIT)
    replaceIndex = -1
    i = 0
    while i <= SymbolCount:
        name = ""
        if i == 0:
            name = BaseCurrency
            if StringToDouble(name) != workCurrencies.getKey(i):
                replaceIndex = i
        else:
            if StringToDouble(BaseCurrency) == workCurrencies.getKey(i) and replaceIndex > -1:
                name = _str(workCurrencies.getKey(replaceIndex))
            else:
                name = _str(workCurrencies.getKey(i))
        PlotIndexSetString(i, PLOT_LABEL, name)
        width = (2 if ((name == base or name == profit) or name == Symbol()) else 1)
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, Draw)
        PlotIndexSetInteger(i, PLOT_LINE_WIDTH, width)
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, True)
        i += 1
    for i in range(SymbolCount + 1, 15):
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    for i in range(15, 19):
        PlotIndexSetString(i, PLOT_LABEL, _str((Sigma1 if ((i - 15) < _idiv(19 - 15, 2)) else Sigma2)) + ' Sigma (StdDev)')
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, Draw)
        PlotIndexSetInteger(i, PLOT_LINE_WIDTH, 1)
        PlotIndexSetInteger(i, PLOT_LINE_STYLE, STYLE_DOT)
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, True)
        PlotIndexSetInteger(i, PLOT_SHIFT, 1)
    if not AbsoluteValues:
        IndicatorSetInteger(INDICATOR_LEVELS, 1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    price_type = Box(EnumToString(PriceType, 'ENUM_APPLIED_PRICE'))
    StringReplace(price_type, 'PRICE_', '')
    price_mode = Box(((' ' + EnumToString(PriceMethod, 'ENUM_MA_METHOD') + '(' + _str(PricePeriod) + ')') if (PricePeriod > 1) else ''))
    StringReplace(price_mode, 'MODE_', '')
    IndicatorSetString(INDICATOR_SHORTNAME, 'UnityPro [' + _str(workCurrencies.getSize()) + '] ' + price_type.v + price_mode.v + (' Abs ' if AbsoluteValues else '') + ((' M=' + _str(Momentum)) if (Momentum > 0) else ''))
    IndicatorSetInteger(INDICATOR_DIGITS, 5)
    LastBarCount = 0
    initDone = True
    EventSetTimer(1)
    return INIT_SUCCEEDED

def calculate(bar, result):
    time = iTime(Symbol(), PERIOD_CURRENT, bar)
    w = Arr.of([0.0], fill=0.0, dyn=False, size=2)
    v = Arr(0, 0.0, dims=(2,))
    ArrayResize(v, SymbolCount)
    for j in range(0, SymbolCount):
        if CopyBuffer(Handles[j], 0, _DT(time), 2, w) == -1:
            Print('CopyBuffer failed: ', Symbols[j], ' ', time, ' ', GetLastError())
            return False
        if Direction[j] == -1:
            w[0] = _fdiv(1.0, w[0])
            w[1] = _fdiv(1.0, w[1])
        w[1] *= Contracts[j]
        w[0] *= Contracts[j]
        v[j][0] = w[1]
        v[j][1] = w[0]
    sum_ = Arr.of([1.0, 1.0], fill=0.0, dyn=False, size=2)
    for j in range(0, SymbolCount):
        sum_[0] += v[j][0]
        sum_[1] += v[j][1]
    base_0 = _fdiv(1.0, sum_[0])
    base_1 = _fdiv(1.0, sum_[1])
    if AbsoluteValues:
        result[0] = base_0 * Contracts[0]
    else:
        result[0] = _fdiv(base_0, base_1) - 1.0
    for j in range(1, SymbolCount + 1):
        if AbsoluteValues:
            result[j] = base_0 * v[j - 1][0]
        else:
            result[j] = _fdiv(base_0 * v[j - 1][0], base_1 * v[j - 1][1]) - 1.0
    return True

def OnTimer():
    price = Arr.of([], fill=0.0)
    if LastBarCount != Bars(Symbol(), PERIOD_CURRENT):
        n = OnCalculate(Bars(Symbol(), PERIOD_CURRENT), 0, 0, price)
        if n > 0:
            EventKillTimer()
            ChartSetSymbolPeriod(0, Symbol(), PERIOD_CURRENT)
            ChartRedraw()
    else:
        EventKillTimer()

def OnCalculate(rates_total, prev_calculated, begin, price):
    global LastBarCount, _s_OnCalculate_fileSaved
    if not initDone:
        return 0
    if (LastBarCount == rates_total and prev_calculated == rates_total) and PriceType != PRICE_CLOSE:
        return prev_calculated
    if prev_calculated == 0:
        for i in range(0, rates_total):
            for j in range(0, 19):
                buffers[j][i] = EMPTY_VALUE
    limit = MathMin(rates_total - prev_calculated + 1, BarLimit)
    result = Arr(0, 0.0)
    result2 = Arr(0, 0.0)
    ArrayResize(result, SymbolCount + 1)
    if Momentum > 0:
        ArrayResize(result2, SymbolCount + 1)
    for i in range(0, limit):
        if not calculate(i, result):
            return 0
        if Momentum > 0:
            if not calculate(i + 1, result2):
                return 0
            for j in range(0, SymbolCount + 1):
                buffers[j][i] = ((result[j] - result2[j]) * Momentum) + (result[j] * (1 - Momentum))
        else:
            for j in range(0, SymbolCount + 1):
                buffers[j][i] = result[j]
        if not AbsoluteValues:
            buffers[19 - 4][i] = 0
            for j in range(0, SymbolCount + 1):
                buffers[19 - 4][i] += pow(getter[j][i], 2)
            sigma = sqrt(_fdiv(getter[19 - 4][i], SymbolCount))
            buffers[19 - 4][i] = sigma * Sigma1
            buffers[19 - 3][i] = (-sigma) * Sigma1
            buffers[19 - 2][i] = sigma * Sigma2
            buffers[19 - 1][i] = (-sigma) * Sigma2
    if _s_OnCalculate_fileSaved is _UNSET:
        _s_OnCalculate_fileSaved = SaveToFile == ''
    if (not _s_OnCalculate_fileSaved) and (not AbsoluteValues):
        SaveBuffersToFile(SaveToFile)
        _s_OnCalculate_fileSaved = True
    LastBarCount = rates_total
    return LastBarCount

def GetBuffer(index, bar):
    return getter[index][bar]

def SaveBuffersToFile(filename):
    h = FileOpen(filename, (((FILE_WRITE | FILE_CSV) | FILE_SHARE_READ) | FILE_SHARE_WRITE) | FILE_ANSI, 59)
    if h == INVALID_HANDLE:
        return False
    line = 'datetime'
    for k in range(BarLookback - 1, 0 - 1, -1):
        i = 0
        while i < workCurrencies.getSize():
            line += ';' + _str(workCurrencies.getKey(i)) + _str(k + 1)
            i += 1
    if ShiftLastBuffer:
        line += ';FORECAST'
    FileWriteString(h, line + '\n')
    i = BarLimit - BarLookback
    while i >= (1 if (ShiftedBuffer > -1) else 0):
        time = iTime(Symbol(), PERIOD_CURRENT, i)
        line = _str(time)
        for k in range(BarLookback - 1, 0 - 1, -1):
            j = 0
            while j < workCurrencies.getSize():
                line += ';' + _str(GetBuffer(j, i + k))
                j += 1
        if ShiftLastBuffer:
            line += ';' + _str(GetBuffer(ShiftedBuffer, i - 1))
        FileWriteString(h, line + '\n')
        i -= 1
    FileClose(h)
    Print('File saved ', filename)
    return True

# ---- global variables initialised from expressions
buffers = _alloc(IndicatorArray)
buffers.__init__(19)
getter = _alloc(IndicatorArrayGetter)
getter.__init__(buffers)
workCurrencies = _alloc(HashMapTemplate)
workCurrencies.__init__()

# ---- static local variables
_s_OnCalculate_fileSaved = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UnityPro(_MQL5Indicator):
    name = 'UnityPro'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BarLimit': 1000,  # ·    BarLimit
        'Draw': _Choice({0: 'None', 1: 'Line', 2: 'Section', 3: 'Histogram', 4: 'Histogram2', 5: 'Arrow', 6: 'Zigzag', 7: 'Filling', 8: 'Color Line', 9: 'Color Section', 10: 'Color Histogram', 11: 'Color Histogram2', 12: 'Color Arrow', 13: 'Color Zigzag', 14: 'Bars', 15: 'Candles', 16: 'Color Bars', 17: 'Color Candles'}, default=1),  # ·    Draw
        'PriceType': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # ·    PriceType
        'PriceMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # ·    PriceMethod
        'PricePeriod': 1,  # ·    PricePeriod
        'AbsoluteValues': False,  # ·    AbsoluteValues
        'Momentum': 0.0,  # ·    Momentum [0..1]
        'Sigma1': 1.0,  # ·    Deviation Level Sigma 1 [0..3]
        'Sigma2': 2.0,  # ·    Deviation Level Sigma 2 [0..3]
        'ShiftLastBuffer': False,  # ·    ShiftLastBuffer
        'BarLookback': 1,  # ·    BarLookback
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

