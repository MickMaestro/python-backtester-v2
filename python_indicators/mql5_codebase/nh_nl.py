"""nh_nl — converted from MQL5: MQL5 Indicators/New Highs-New Lows Index/nh_nl.mq5

Calculates the difference between the number of pairs that have reached new
highs or lows over a given period (USD currency rate is dealt with).
Copyright: Copyright © 2011, LenIFCHIK; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, LenIFCHIK', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 8421376, 14822282, 6053069, 16711935]}, 'widths': {1: 5}, 'styles': {1: 0}, 'labels': {1: 'NH-NL'}, 'levels': [], 'description': ['Calculates the difference between the number of pairs that have reached new', 'highs or lows over a given period (USD currency rate is dealt with).'], 'name': 'nh_nl', 'source': 'MQL5 Indicators/New Highs-New Lows Index/nh_nl.mq5', 'folder': 'New Highs-New Lows Index', 'inputs': [{'mql': 'Depth', 'py': 'Depth', 'param': 'Depth', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Depth = _input('Depth', 30)
min_rates_total = 0
NhNlBuffer = Arr(0, 0.0)
ColorNhNlBuffer = Arr(0, 0.0)
Array = Arr(0, 0.0)
Symbols = Arr.of(['EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDCHF', 'USDJPY', 'USDCAD'], fill="", dyn=False, size=7)

def OnInit():
    global min_rates_total
    min_rates_total = Depth
    ArrayResize(Array, Depth)
    ArraySetAsSeries(Array, True)
    SetIndexBuffer(0, NhNlBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(NhNlBuffer, True)
    SetIndexBuffer(1, ColorNhNlBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorNhNlBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'NhNl( ', Depth, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def Rates_Total():
    Bars_ = Arr(7, 0, dyn=False)
    for count in range(0, 7):
        Bars_[count] = Bars(Symbols[count], PERIOD_CURRENT)
    error = GetLastError()
    ResetLastError()
    if error == 4401:
        return -1
    return Bars_[ArrayMinimum(Bars_, 0, WHOLE_ARRAY)]

def SynchroCheck():
    Time0 = Arr(1, 0, dyn=False)
    TimeN = Arr(1, 0, dyn=False)
    Time0[0] = 0
    for count in range(0, 7):
        if CopyTime(Symbols[count], 0, 0, 1, Time0) > 0:
            break
    if Time0[0] == 0:
        return False
    for count in range(0, 7):
        if CopyTime(Symbols[count], 0, 0, 1, TimeN) <= 0:
            return False
        elif TimeN[0] != Time0[0]:
            return False
    return True

def newh(symbol, index):
    if CopyClose(symbol, Period(), index, Depth, Array) <= 0:
        return -1
    HC = Array[ArrayMaximum(Array, 0, Depth)]
    LC = Array[ArrayMinimum(Array, 0, Depth)]
    nh = 0
    if ((symbol == 'EURUSD' or symbol == 'GBPUSD') or symbol == 'AUDUSD') or symbol == 'NZDUSD':
        if Array[0] == LC:
            nh = 1
        else:
            nh = 0
    elif (symbol == 'USDCHF' or symbol == 'USDJPY') or symbol == 'USDCAD':
        if Array[0] == HC:
            nh = 1
        else:
            nh = 0
    else:
        Print('newh', '(', symbol, ') There is no such symbol! ')
        return -1
    return nh

def newl(symbol, index):
    if CopyClose(symbol, Period(), index, Depth, Array) <= 0:
        return -1
    HC = Array[ArrayMaximum(Array, 0, Depth)]
    LC = Array[ArrayMinimum(Array, 0, Depth)]
    nl = 0
    if ((symbol == 'EURUSD' or symbol == 'GBPUSD') or symbol == 'AUDUSD') or symbol == 'NZDUSD':
        if Array[0] == HC:
            nl = 1
        else:
            nl = 0
    elif (symbol == 'USDCHF' or symbol == 'USDJPY') or symbol == 'USDCAD':
        if Array[0] == LC:
            nl = 1
        else:
            nl = 0
    else:
        Print('newl', '(', symbol, ') There is no such symbol! ')
        return -1
    return nl

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    Bars_ = Rates_Total()
    if Bars_ < min_rates_total:
        return 0
    if not SynchroCheck():
        return prev_calculated
    limit = 0
    bar = 0
    NH = 0
    NL = 0
    res = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = Bars_ - min_rates_total - 1
    else:
        limit = MathMin(Bars_, rates_total - prev_calculated)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        NH = 0
        NL = 0
        for count in range(0, 7):
            res = newh(Symbols[count], bar)
            if res < 0:
                return 0
            NH += res
            res = newl(Symbols[count], bar)
            if res < 0:
                return 0
            NL += res
        if ((Symbol() == 'EURUSD' or Symbol() == 'GBPUSD') or Symbol() == 'AUDUSD') or Symbol() == 'NZDUSD':
            NhNlBuffer[bar] = NL - NH
        elif (Symbol() == 'USDCHF' or Symbol() == 'USDJPY') or Symbol() == 'USDCAD':
            NhNlBuffer[bar] = NH - NL
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorNhNlBuffer[bar] = 0.0
        if NhNlBuffer[bar] > 0:
            if NhNlBuffer[bar] > NhNlBuffer[bar + 1]:
                ColorNhNlBuffer[bar] = 1.0
            if NhNlBuffer[bar] < NhNlBuffer[bar + 1]:
                ColorNhNlBuffer[bar] = 2.0
        if NhNlBuffer[bar] < 0:
            if NhNlBuffer[bar] < NhNlBuffer[bar + 1]:
                ColorNhNlBuffer[bar] = 3.0
            if NhNlBuffer[bar] > NhNlBuffer[bar + 1]:
                ColorNhNlBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NhNl(_MQL5Indicator):
    name = 'nh_nl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Depth': 30,
    }

