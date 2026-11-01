"""SSL_Channel_Chart — converted from MQL5: MQL5 Indicators/SSL Channel Chart/SSL_Channel_Chart.mq5

Copyright: Copyright 2020, MetaQuotes Software Corp.; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [42495], 2: [16776960]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Bears', 2: 'Bulls'}, 'levels': [], 'description': [], 'name': 'SSL_Channel_Chart', 'source': 'MQL5 Indicators/SSL Channel Chart/SSL_Channel_Chart.mq5', 'folder': 'SSL Channel Chart', 'inputs': [{'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'Lb', 'py': 'Lb', 'param': 'Lb', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Method = _input('MA_Method', MODE_SMA)  # Method
Lb = _input('Lb', 10)
ssld = Arr(0, 0.0)
sslu = Arr(0, 0.0)
Hlv = Arr(0, 0.0)
hMAHigh = 0
hMALow = 0

def OnInit():
    global hMAHigh, hMALow
    SetIndexBuffer(0, ssld, INDICATOR_DATA)
    SetIndexBuffer(1, sslu, INDICATOR_DATA)
    SetIndexBuffer(2, Hlv, INDICATOR_CALCULATIONS)
    hMAHigh = iMA(Symbol(), PERIOD_CURRENT, Lb, 0, MA_Method, PRICE_HIGH)
    hMALow = iMA(Symbol(), PERIOD_CURRENT, Lb, 0, MA_Method, PRICE_LOW)
    if hMAHigh == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    if hMALow == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    ArraySetAsSeries(ssld, True)
    ArraySetAsSeries(sslu, True)
    ArraySetAsSeries(Hlv, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    counted_bars = prev_calculated
    i = 0
    limit = 0
    MAHigh = Arr(0, 0.0)
    MALow = Arr(0, 0.0)
    if counted_bars < 0:
        return -1
    if counted_bars > 0:
        counted_bars -= 1
    limit = MathMax(rates_total - counted_bars - Lb, 1)
    CopyBuffer(hMAHigh, 0, 0, limit + 1, MAHigh)
    CopyBuffer(hMALow, 0, 0, limit + 1, MALow)
    i = limit
    for i in range(i, 0 - 1, -1):
        Hlv[i] = Hlv[i + 1]
        if close[rates_total - 1 - i] > MAHigh[limit - i]:
            Hlv[i] = 1.0
        if close[rates_total - 1 - i] < MALow[limit - i]:
            Hlv[i] = -1.0
        if Hlv[i] == -1:
            ssld[i] = MAHigh[limit - i]
            sslu[i] = MALow[limit - i]
        else:
            ssld[i] = MALow[limit - i]
            sslu[i] = MAHigh[limit - i]
    else:
        i = _range_end(i, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SSLChannelChart(_MQL5Indicator):
    name = 'SSL_Channel_Chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'Lb': 10,
    }

