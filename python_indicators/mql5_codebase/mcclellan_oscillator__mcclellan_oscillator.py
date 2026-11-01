"""McClellan_Oscillator — converted from MQL5: MQL5 Indicators/McClellan_Oscillator/McClellan_Oscillator.mq5

McClellan oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'McClellanOSC'}, 'levels': [], 'description': ['McClellan oscillator'], 'name': 'McClellan_Oscillator', 'source': 'MQL5 Indicators/McClellan_Oscillator/McClellan_Oscillator.mq5', 'folder': 'McClellan_Oscillator', 'inputs': [{'mql': 'InpBaseCurrency', 'py': 'InpBaseCurrency', 'param': None, 'type': 'string', 'default': 'USD', 'label': 'Base currency', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 19, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 39, 'label': 'Slow MA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpBaseCurrency = _input('InpBaseCurrency', 'USD')  # Base currency
InpPeriodFast = _input('InpPeriodFast', 19)  # Fast MA period
InpPeriodSlow = _input('InpPeriodSlow', 39)  # Slow MA period
BufferMO = Arr(0, 0.0)
BufferRANA = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
base_symbol = ""
num_symbols = 0
period_fast = 0
period_slow = 0

class SSymbol(MqlObject):
    _q_fields = ('name', 'inverse', 'bars')
    def __init__(self, *args):
        self.name = ""
        self.inverse = False
        self.bars = 0
    def Refresh(self):
        array = Arr(0, 0)
        CopyTime(self.name, PERIOD_CURRENT, 0, 1, array)

def OnInit():
    global base_symbol, num_symbols, period_fast, period_slow
    EventSetTimer(90)
    base_symbol = InpBaseCurrency
    period_fast = (2 if (InpPeriodFast < 2) else InpPeriodFast)
    period_slow = (2 if (InpPeriodSlow < 2) else InpPeriodSlow)
    StringTrimLeft(_GlobRef(globals(), 'base_symbol'))
    StringTrimRight(_GlobRef(globals(), 'base_symbol'))
    num_symbols = InitSymbols(InpBaseCurrency)
    SetIndexBuffer(0, BufferMO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRANA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'McClellan OSC ' + base_symbol + '(' + _str(num_symbols) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMO, True)
    ArraySetAsSeries(BufferRANA, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    min_bars = 4
    if rates_total < min_bars or (not CheckBars(rates_total, min_bars)):
        return 0
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMO, EMPTY_VALUE)
        ArrayInitialize(BufferRANA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferFMA, 0)
    limit_min = fmin(rates_total, MinBars(rates_total)) - 1
    total = (limit if (limit == 0) else limit_min)
    for i in range(total, 0 - 1, -1):
        Up = 0.0
        Dn = 0.0
        j = 0
        while j < num_symbols:
            symbol = array_symbols[j].name
            index = BarShift(symbol, PERIOD_CURRENT, time[i], True)
            if index == WRONG_VALUE:
                j += 1
                continue
            C = Close(symbol, index)
            O = Open(symbol, index)
            if array_symbols[j].inverse:
                if C > O:
                    Dn += 1
                if C < O:
                    Up += 1
            else:
                if C > O:
                    Up += 1
                if C < O:
                    Dn += 1
            j += 1
        BufferRANA[i] = (_fdiv(Up - Dn, Up + Dn) if ((Up + Dn) != 0) else 0)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_fast, BufferRANA, BufferFMA)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_slow, BufferRANA, BufferSMA)
    for i in range(total, 0 - 1, -1):
        BufferMO[i] = (BufferFMA[i] - BufferSMA[i]) * (period_fast + period_slow)
    return rates_total

def OnTimer():
    total = num_symbols
    if total == 0:
        return
    for i in range(0, total):
        array_symbols[i].Refresh()

def InitSymbols(base):
    array = Arr(0, "")
    n = 0
    total = SymbolsTotal(True)
    ArrayResize(array, total, 100)
    for i in range(0, total):
        symbol = SymbolName(i, True)
        if StringFind(symbol, base) == WRONG_VALUE:
            continue
        n += 1
        ArrayResize(array, n, 100)
        array[n - 1] = symbol
    n = 0
    total = ArraySize(array)
    ArrayResize(array_symbols, total, 100)
    for i in range(0, total):
        symbol = array[i]
        pos = StringFind(symbol, base)
        if pos == WRONG_VALUE:
            continue
        n += 1
        array_symbols[n - 1].name = symbol
        array_symbols[n - 1].inverse = (True if (pos > 0) else False)
        array_symbols[n - 1].bars = Bars(symbol, PERIOD_CURRENT)
    return n

def CheckBars(rates_total, min_bars):
    res = True
    total = ArraySize(array_symbols)
    for i in range(0, total):
        symbol = array_symbols[i].name
        array_symbols[i].bars = (rates_total if (symbol == Symbol()) else Bars(symbol, PERIOD_CURRENT))
        array_symbols[i].Refresh()
        if array_symbols[i].bars < min_bars:
            res = False
    return res

def MinBars(rates_total):
    total = ArraySize(array_symbols)
    min_bars = rates_total
    for i in range(0, total):
        if array_symbols[i].bars < min_bars:
            min_bars = array_symbols[i].bars
    return min_bars

def Open(symbol_name, shift):
    array = Arr(0, 0.0)
    if CopyOpen(symbol_name, PERIOD_CURRENT, shift, 1, array) == 1:
        return array[0]
    return 0.0

def Close(symbol_name, shift):
    array = Arr(0, 0.0)
    if CopyClose(symbol_name, PERIOD_CURRENT, shift, 1, array) == 1:
        return array[0]
    return 0.0

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

# ---- global variables initialised from expressions
array_symbols = Arr(0, 0, factory=SSymbol)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class McClellanOscillator(_MQL5Indicator):
    name = 'McClellan_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 19,  # Fast MA period
        'InpPeriodSlow': 39,  # Slow MA period
    }

