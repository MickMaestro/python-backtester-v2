"""fxtrend25ema — converted from MQL5: MQL5 Indicators/FxTrend 25EMA/fxtrend25ema.mq5

Copyright: dec.-2013, Jose Luis Gongora Fernandez aka. jossfx; Link: http://www.forexploit.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'dec.-2013, Jose Luis Gongora Fernandez aka. jossfx', 'link': 'http://www.forexploit.com', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 255, 12632256]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'FxTrend 25EMA'}, 'levels': [], 'description': [], 'name': 'fxtrend25ema', 'source': 'MQL5 Indicators/FxTrend 25EMA/fxtrend25ema.mq5', 'folder': 'FxTrend 25EMA', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iMA_handle25EMA = 0
iND_buff = Arr(0, 0.0)
iMA_buff25EMA = Arr(0, 0.0)
iND_color = Arr(0, 0.0)
last_side = 0

def OnInit():
    global iMA_handle25EMA, last_side
    SetIndexBuffer(0, iND_buff, INDICATOR_DATA)
    SetIndexBuffer(1, iND_color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, iMA_buff25EMA, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 24)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FxTrend 25EMA')
    iMA_handle25EMA = iMA(None, 0, 25, 0, MODE_EMA, PRICE_CLOSE)
    last_side = 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global last_side
    if rates_total <= 24:
        return 0
    calculated = BarsCalculated(iMA_handle25EMA)
    if calculated < rates_total:
        Print('Not all data of iMA_handle25EMA is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated >= rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
    if False:
        return 0
    if CopyBuffer(iMA_handle25EMA, 0, 0, to_copy, iMA_buff25EMA) <= 0:
        Print('Getting 25EMA buffer is failed! Error', GetLastError())
        return 0
    i = 0
    limit = 0
    if prev_calculated <= 24:
        i = 0
        for i in range(i, 24):
            iND_buff[i] = 0.0
        else:
            i = _range_end(i, 24, 1)
        limit = 24
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        if Close[i] > iMA_buff25EMA[i]:
            last_side = 1
        elif Close[i] < iMA_buff25EMA[i]:
            last_side = -1
        iND_buff[i] = iMA_buff25EMA[i] - iMA_buff25EMA[i - 2]
        if (Close[i] >= iMA_buff25EMA[i] and (iMA_buff25EMA[i] - iMA_buff25EMA[i - 2]) >= 0) and last_side == 1:
            iND_color[i] = 0.0
        elif (Close[i] <= iMA_buff25EMA[i] and (iMA_buff25EMA[i] - iMA_buff25EMA[i - 2]) <= 0) and last_side == -1:
            iND_color[i] = 1.0
        else:
            iND_color[i] = 2.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fxtrend25ema(_MQL5Indicator):
    name = 'fxtrend25ema'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

