"""Portable Moving Average (Series version) — converted from MQL5: MQL5 Indicators/Portable Moving Average/Portable Moving Average (Series version).mq5

Copyright: Copyright phade 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright phade 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8, 2: 0, 3: 0}, 'colors': {1: [32768, 255, 4294967295]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'MA Line', 2: 'Uptrend', 3: 'Downtrend'}, 'levels': [], 'description': [], 'name': 'Portable Moving Average (Series version)', 'source': 'MQL5 Indicators/Portable Moving Average/Portable Moving Average (Series version).mq5', 'folder': 'Portable Moving Average', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 10, 'label': 'MA Period', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'MA Mode', 'sinput': False}, {'mql': 'MA_Price', 'py': 'MA_Price', 'param': 'MA_Price', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Period = _input('MA_Period', 10)  # MA Period
MA_Method = _input('MA_Method', MODE_SMA)  # MA Mode
MA_Price = _input('MA_Price', PRICE_CLOSE)  # Applied price
ma = Arr(0, 0.0)
color_buf = Arr(0, 0.0)
uptrend = Arr(0, 0.0)
downtrend = Arr(0, 0.0)
ma_handle = INVALID_HANDLE

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA (Period ' + IntegerToString(MA_Period) + ')')
    InitializeMovingAverage(_GlobRef(globals(), 'ma_handle'), ma, color_buf, MA_Period, MA_Method, MA_Price)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    BuildMovingAverage(ma_handle, prev_calculated, rates_total, ma, color_buf)
    shift = 0
    if uptrend[shift] > 0:
        Comment('Bull trend')
    if downtrend[shift] > 0:
        Comment('Bear trend')
    return rates_total

def OnDeinit(reason):
    Comment('')

def InitializeMovingAverage(handle, buffer, color_buffer, ma_period, ma_method, applied_price):
    SetIndexBuffer(0, buffer, INDICATOR_DATA)
    SetIndexBuffer(1, color_buffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, uptrend, INDICATOR_DATA)
    SetIndexBuffer(3, downtrend, INDICATOR_DATA)
    ArraySetAsSeries(buffer, True)
    ArraySetAsSeries(color_buffer, True)
    ArraySetAsSeries(uptrend, True)
    ArraySetAsSeries(downtrend, True)
    handle.v = iMA(Symbol(), Period(), ma_period, 0, ma_method, applied_price)
    return handle.v != INVALID_HANDLE

def BuildMovingAverage(handle, prev_calculated, rates_total, buffer, colbuff):
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyBuffer(handle, 0, 0, to_copy, buffer) < 0:
        ChartRedraw()
    start = (0 if (prev_calculated < 0) else (prev_calculated - 1))
    for i in range(start, 0 - 1, -1):
        if (i + 2) < start:
            uptrend[i] = 0.0
            downtrend[i] = 0.0
            if ma[i] > ma[i + 1] and ma[i + 1] > ma[i + 2]:
                colbuff[i] = 0.0
                uptrend[i] = 1.0
                downtrend[i] = 0.0
            elif ma[i] < ma[i + 1] and ma[i + 1] < ma[i + 2]:
                colbuff[i] = 1.0
                uptrend[i] = 0.0
                downtrend[i] = 1.0
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PortableMovingAverageSeriesVersion(_MQL5Indicator):
    name = 'Portable Moving Average (Series version)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Period': 10,  # MA Period
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Mode
        'MA_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

