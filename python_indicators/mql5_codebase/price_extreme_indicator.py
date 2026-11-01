"""Price_Extreme_Indicator — converted from MQL5: MQL5 Indicators/Channel based on extreme prices/Price_Extreme_Indicator.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65535], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Border High', 2: 'Border Low'}, 'levels': [], 'description': [], 'name': 'Price_Extreme_Indicator', 'source': 'MQL5 Indicators/Channel based on extreme prices/Price_Extreme_Indicator.mq5', 'folder': 'Channel based on extreme prices', 'inputs': [{'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'int', 'default': 5, 'label': 'Length of levels', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMultiplier = _input('InpMultiplier', 5)  # Length of levels
BufferBorderHigh = Arr(0, 0.0)
BufferBorderLow = Arr(0, 0.0)
multiplier = 0
coeff = 0

def OnInit():
    global coeff, multiplier
    multiplier = (1 if (InpMultiplier < 1) else InpMultiplier)
    coeff = PeriodSeconds() * multiplier
    SetIndexBuffer(0, BufferBorderHigh, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBorderLow, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, multiplier)
    PlotIndexSetInteger(1, PLOT_SHIFT, multiplier)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (multiplier + 2):
        return 0
    ArraySetAsSeries(BufferBorderHigh, True)
    ArraySetAsSeries(BufferBorderLow, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1 - multiplier
    else:
        limit += multiplier + 2
    for i in range(0, limit):
        BeginTime = _long(ceil(_idiv(time[i], coeff))) * coeff
        EndTime = _long(ceil(_idiv(time[i], coeff) + 1)) * coeff
        begin_bar = BarShift(PERIOD_CURRENT, BeginTime)
        end_bar = BarShift(PERIOD_CURRENT, EndTime)
        if begin_bar == WRONG_VALUE or end_bar == WRONG_VALUE:
            continue
        bar_h = Highest(PERIOD_CURRENT, begin_bar - end_bar + 1, end_bar)
        bar_l = Lowest(PERIOD_CURRENT, begin_bar - end_bar + 1, end_bar)
        if bar_h == WRONG_VALUE or bar_l == WRONG_VALUE:
            continue
        BufferBorderHigh[i] = high[bar_h]
        BufferBorderLow[i] = low[bar_l]
    return rates_total

def Highest(timeframe, count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), timeframe, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(timeframe, count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), timeframe, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE

def BarShift(timeframe, time):
    res = WRONG_VALUE
    last_bar = 0
    if SeriesInfoInteger(Symbol(), timeframe, SERIES_LASTBAR_DATE, _ValRef(last_bar)):
        if time > last_bar:
            res = 0
        else:
            shift = Bars(Symbol(), timeframe, time, last_bar)
            if shift > 0:
                res = shift - 1
    return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceExtremeIndicator(_MQL5Indicator):
    name = 'Price_Extreme_Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpMultiplier': 5,  # Length of levels
    }

