"""HLBands — converted from MQL5: MQL5 Indicators/HLBands/HLBands.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3937500], 2: [15624315], 3: [14599344]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 2}, 'labels': {1: 'Upper', 2: 'Lower', 3: 'Open'}, 'levels': [], 'description': [], 'name': 'HLBands', 'source': 'MQL5 Indicators/HLBands/HLBands.mq5', 'folder': 'HLBands', 'inputs': [{'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 16408, 'label': 'Bands period', 'sinput': False}, {'mql': 'InpBandUpdate', 'py': 'InpBandUpdate', 'param': 'InpBandUpdate', 'type': 'int', 'default': 0, 'label': 'Bands Update', 'sinput': False}, {'mql': 'InpBandCalcMethod', 'py': 'InpBandCalcMethod', 'param': 'InpBandCalcMethod', 'type': 'int', 'default': 0, 'label': 'Bands Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CALC_METHOD
PRICE_HL = 0
PRICE_OC = 1
_enum('ENUM_CALC_METHOD', {0: 'PRICE_HL', 1: 'PRICE_OC'})

# enum ENUM_MODE_UPDATE
MODE_UPDATE_OPEN = 0
MODE_UPDATE_ALWAYS = 1
_enum('ENUM_MODE_UPDATE', {0: 'MODE_UPDATE_OPEN', 1: 'MODE_UPDATE_ALWAYS'})

# ---- inputs and global variables
InpTimeframe = _input('InpTimeframe', PERIOD_D1)  # Bands period
InpBandUpdate = _input('InpBandUpdate', MODE_UPDATE_OPEN)  # Bands Update
InpBandCalcMethod = _input('InpBandCalcMethod', PRICE_HL)  # Bands Applied price
BufferH = Arr(0, 0.0)
BufferL = Arr(0, 0.0)
BufferOpen = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferH, INDICATOR_DATA)
    SetIndexBuffer(1, BufferL, INDICATOR_DATA)
    SetIndexBuffer(2, BufferOpen, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 220)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, True)
    tfn = StringSubstr(EnumToString(InpTimeframe, 'ENUM_TIMEFRAMES'), 7)
    IndicatorSetString(INDICATOR_SHORTNAME, 'High/Low Bands(' + tfn + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferH, True)
    ArraySetAsSeries(BufferL, True)
    ArraySetAsSeries(BufferOpen, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_index_curr, _s_OnCalculate_index_prev, _s_OnCalculate_time_bar
    if rates_total < 3:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        _s_OnCalculate_index_curr = (BarShift(Symbol(), InpTimeframe, time[limit]) if (InpTimeframe < PERIOD_MN1) else BarShift(Symbol(), InpTimeframe, BeginOfYear(time[limit])))
        if _s_OnCalculate_index_curr == WRONG_VALUE:
            return 0
        ArrayInitialize(BufferH, EMPTY_VALUE)
        ArrayInitialize(BufferL, EMPTY_VALUE)
        ArrayInitialize(BufferOpen, EMPTY_VALUE)
        BufferH[limit] = (high[limit] if (InpBandCalcMethod == PRICE_HL) else fmax(open[limit], close[limit]))
        BufferL[limit] = (low[limit] if (InpBandCalcMethod == PRICE_HL) else fmin(open[limit], close[limit]))
    for i in range(limit, 0 - 1, -1):
        _s_OnCalculate_index_curr = (BarShift(Symbol(), InpTimeframe, time[i]) if (InpTimeframe < PERIOD_MN1) else BarShift(Symbol(), InpTimeframe, BeginOfYear(time[i])))
        if _s_OnCalculate_index_curr == WRONG_VALUE:
            return 0
        H = UpperPrice(InpTimeframe, _s_OnCalculate_index_curr)
        L = LowerPrice(InpTimeframe, _s_OnCalculate_index_curr)
        if _s_OnCalculate_index_curr != _s_OnCalculate_index_prev:
            if _s_OnCalculate_index_prev > _s_OnCalculate_index_curr:
                _s_OnCalculate_time_bar = time[i]
                BufferH[i] = ((high[i] if (InpBandCalcMethod == PRICE_HL) else fmax(open[i], close[i])) if (InpBandUpdate == MODE_UPDATE_OPEN) else H)
                BufferL[i] = ((low[i] if (InpBandCalcMethod == PRICE_HL) else fmin(open[i], close[i])) if (InpBandUpdate == MODE_UPDATE_OPEN) else L)
                BufferOpen[i] = open[i]
            _s_OnCalculate_index_prev = _s_OnCalculate_index_curr
        bar = BarShift(Symbol(), PERIOD_CURRENT, _s_OnCalculate_time_bar)
        if bar == WRONG_VALUE:
            continue
        if bar == 0:
            BufferH[i] = (high[i] if (InpBandCalcMethod == PRICE_HL) else fmax(open[i], close[i]))
            BufferL[i] = (low[i] if (InpBandCalcMethod == PRICE_HL) else fmin(open[i], close[i]))
            BufferOpen[i] = open[i]
        else:
            BufferH[i] = BufferH[bar]
            BufferL[i] = BufferL[bar]
            BufferOpen[i] = BufferOpen[bar]
            if InpBandUpdate == MODE_UPDATE_ALWAYS:
                highest = (H if (InpBandCalcMethod == PRICE_HL) else HighestPrice(i, bar, open, close))
                lowhest = (L if (InpBandCalcMethod == PRICE_HL) else LowestPrice(i, bar, open, close))
                SetPrice(highest, i, bar, BufferH)
                SetPrice(lowhest, i, bar, BufferL)
    return rates_total

def HighestPrice(start, end, open, close):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    total = end - start + 1
    ArrayResize(array, total, 20)
    for i in range(0, total):
        array[i] = fmax(open[start + i], close[start + i])
    return array[ArrayMaximum(array)]

def LowestPrice(start, end, open, close):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    total = end - start + 1
    ArrayResize(array, total, 20)
    for i in range(0, total):
        array[i] = fmin(open[start + i], close[start + i])
    return array[ArrayMinimum(array)]

def SetPrice(price, start, end, buffer):
    for i in range(start, end + 1):
        buffer[i] = price

def UpperPrice(timeframe, index):
    return (High(timeframe, index) if (InpBandCalcMethod == PRICE_HL) else 0 if (Open(timeframe, index) == 0 or Close(timeframe, index) == 0) else fmax(Open(timeframe, index), Close(timeframe, index)))

def LowerPrice(timeframe, index):
    return (Low(timeframe, index) if (InpBandCalcMethod == PRICE_HL) else 0 if (Open(timeframe, index) == 0 or Close(timeframe, index) == 0) else fmin(Open(timeframe, index), Close(timeframe, index)))

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

def TimeDay_u(time):
    tm = MqlDateTime()
    day_number = WRONG_VALUE
    if TimeToStruct(time, tm):
        day_number = tm.day
    return day_number

def BeginOfYear(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    tm.mon = 1
    tm.day = 1
    return StructToTime(tm)

def NameTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_index_curr = WRONG_VALUE
_s_OnCalculate_index_prev = WRONG_VALUE
_s_OnCalculate_tm = 0
_s_OnCalculate_time_bar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HLBands(_MQL5Indicator):
    name = 'HLBands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Bands period
        'InpBandUpdate': _Choice({0: 'at the opening of the bar', 1: 'always'}, default=0),  # Bands Update
        'InpBandCalcMethod': _Choice({0: 'High/Low', 1: 'Open/Close'}, default=0),  # Bands Applied price
    }

