"""Relative Moving Average — converted from MQL5: MQL5 Indicators/Moving Average-RMA/Relative Moving Average.mq5

Copyright: Copyright 2023, Mage; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, Mage', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RMA'}, 'levels': [], 'description': [], 'name': 'Relative Moving Average', 'source': 'MQL5 Indicators/Moving Average-RMA/Relative Moving Average.mq5', 'folder': 'Moving Average-RMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 12, 'label': 'RMA Period', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 12)  # RMA Period
buffer_m = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, buffer_m, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mage_RMA' + _str(InpPeriod))
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpPeriod)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpPeriod, price, buffer_m)
    return rates_total

def ExponentialMAOnBuffer(rates_total, prev_calculated, begin, period, price, buffer):
    if period <= 1 or period > (rates_total - begin):
        return 0
    as_series_price = ArrayGetAsSeries(price)
    as_series_buffer = ArrayGetAsSeries(buffer)
    ArraySetAsSeries(price, False)
    ArraySetAsSeries(buffer, False)
    start_position = 0
    smooth_factor = _fdiv(1.0, period)
    if prev_calculated == 0:
        for i in range(0, begin):
            buffer[i] = 0.0
        start_position = period + begin
        buffer[begin] = price[begin]
        for i in range(begin + 1, start_position):
            buffer[i] = (price[i] * smooth_factor) + (buffer[i - 1] * (1.0 - smooth_factor))
    else:
        start_position = prev_calculated - 1
    for i in range(start_position, rates_total):
        buffer[i] = (price[i] * smooth_factor) + (buffer[i - 1] * (1.0 - smooth_factor))
    ArraySetAsSeries(price, as_series_price)
    ArraySetAsSeries(buffer, as_series_buffer)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RelativeMovingAverage(_MQL5Indicator):
    name = 'Relative Moving Average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 12,  # RMA Period
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

