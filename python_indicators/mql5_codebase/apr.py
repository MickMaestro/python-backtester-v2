"""APR — converted from MQL5: MQL5 Indicators/APR/APR.mq5

Average Period Range
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'APR'}, 'levels': [], 'description': ['Average Period Range'], 'name': 'APR', 'source': 'MQL5 Indicators/APR/APR.mq5', 'folder': 'APR', 'inputs': [{'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 16408, 'label': 'Timeframe', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 5, 'label': 'Period', 'sinput': False}, {'mql': 'InpCalcPrice', 'py': 'InpCalcPrice', 'param': 'InpCalcPrice', 'type': 'int', 'default': 0, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpCalcMode', 'py': 'InpCalcMode', 'param': 'InpCalcMode', 'type': 'int', 'default': 0, 'label': 'Calculation mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CALC_PRICE
PRICE_HL = 0
PRICE_OC = 1
_enum('ENUM_CALC_PRICE', {0: 'PRICE_HL', 1: 'PRICE_OC'})

# enum ENUM_CALC_MODE
MODE_ABSOLUTE = 0
MODE_RELATIVE = 1
_enum('ENUM_CALC_MODE', {0: 'MODE_ABSOLUTE', 1: 'MODE_RELATIVE'})

# ---- inputs and global variables
InpTimeframe = _input('InpTimeframe', PERIOD_D1)  # Timeframe
InpPeriod = _input('InpPeriod', 5)  # Period
InpCalcPrice = _input('InpCalcPrice', PRICE_HL)  # Applied price
InpCalcMode = _input('InpCalcMode', MODE_ABSOLUTE)  # Calculation mode
BufferAPR = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferAPR, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'APR(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferAPR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferAPR, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        index = BarShift(Symbol(), InpTimeframe, time[i], False)
        if index == WRONG_VALUE:
            return 0
        sum_ = 0.0
        j = 0
        while j < period:
            if InpCalcPrice == PRICE_HL:
                h = High(InpTimeframe, index + j)
                l = Low(InpTimeframe, index + j)
                if h == 0 or l == 0:
                    return 0
                sum_ += h - l
            else:
                o = Open(InpTimeframe, index + j)
                c = Close(InpTimeframe, index + j)
                if o == 0 or c == 0:
                    return 0
                sum_ += fabs(o - c)
            j += 1
        if InpCalcMode == MODE_ABSOLUTE:
            BufferAPR[i] = _fdiv(sum_, period)
        else:
            opn = Open(InpTimeframe, index)
            if opn == 0:
                return 0
            BufferAPR[i] = _fdiv(100 * sum_, period * opn)
    return rates_total

def BarShift(symbol_name, timeframe, time, exact=False):
    last_bar = Box(0)
    if not SeriesInfoInteger(symbol_name, timeframe, SERIES_LASTBAR_DATE, last_bar):
        array = Arr(1, 0, dyn=False)
        if CopyTime(symbol_name, timeframe, 0, 1, array) == 1:
            last_bar.v = array[0]
        else:
            return WRONG_VALUE
    if time > last_bar.v:
        return 0
    shift = Bars(symbol_name, timeframe, time, last_bar.v)
    array = Arr(1, 0, dyn=False)
    if CopyTime(symbol_name, timeframe, _DT(time), 1, array) == 1:
        return ((shift - 1) if (array[0] == time) else WRONG_VALUE if (exact and time > (array[0] + PeriodSeconds(timeframe))) else shift)
    return WRONG_VALUE

def Time(timeframe, index):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    if CopyTime(Symbol(), timeframe, index, 1, array) == 1:
        return array[0]
    return 0

def Open(timeframe, index):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyOpen(Symbol(), timeframe, index, 1, array) == 1:
        return array[0]
    return 0.0

def High(timeframe, index):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), timeframe, index, 1, array) == 1:
        return array[0]
    return 0.0

def Low(timeframe, index):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), timeframe, index, 1, array) == 1:
        return array[0]
    return 0.0

def Close(timeframe, index):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyClose(Symbol(), timeframe, index, 1, array) == 1:
        return array[0]
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class APR(_MQL5Indicator):
    name = 'APR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Timeframe
        'InpPeriod': 5,  # Period
        'InpCalcPrice': _Choice({0: 'High/Low', 1: 'Open/Close'}, default=0),  # Applied price
        'InpCalcMode': _Choice({0: 'Absolute', 1: 'Relative'}, default=0),  # Calculation mode
    }

