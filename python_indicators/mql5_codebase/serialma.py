"""SerialMA — converted from MQL5: MQL5 Indicators/SerialMA/SerialMA.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MA', 2: 'Point'}, 'levels': [], 'description': [], 'name': 'SerialMA', 'source': 'MQL5 Indicators/SerialMA/SerialMA.mq5', 'folder': 'SerialMA', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferMA = Arr(0, 0.0)
BufferPoint = Arr(0, 0.0)
BufferTime = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPoint, INDICATOR_DATA)
    SetIndexBuffer(2, BufferTime, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Serial MA')
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferPoint, True)
    ArraySetAsSeries(BufferTime, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    total = rates_total - 2
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = total
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferPoint, EMPTY_VALUE)
        ArrayInitialize(BufferTime, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        if i == total:
            BufferTime[i] = float(time[i])
        else:
            BufferTime[i] = BufferTime[i + 1]
            period_ma = BarShift(Symbol(), PERIOD_CURRENT, _long(BufferTime[i])) - i + 1
            summ = 0.0
            for n in range(0, period_ma):
                summ += close[i + n]
            if period_ma != 0:
                BufferMA[i] = _fdiv(summ, period_ma)
            if ((BufferMA[i] - close[i]) * (BufferMA[i + 1] - close[i + 1])) < 0:
                BufferTime[i] = float(time[i])
                BufferMA[i] = close[i]
                BufferPoint[i] = BufferMA[i]
            else:
                BufferPoint[i] = EMPTY_VALUE
    return rates_total

def BarShift(symbol_name, timeframe, time):
    if symbol_name == "" or symbol_name == '':
        symbol_name = Symbol()
    res = WRONG_VALUE
    last_bar = 0
    if SeriesInfoInteger(symbol_name, timeframe, SERIES_LASTBAR_DATE, _ValRef(last_bar)):
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


class SerialMA(_MQL5Indicator):
    name = 'SerialMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

