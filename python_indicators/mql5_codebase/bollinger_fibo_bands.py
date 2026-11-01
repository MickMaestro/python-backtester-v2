"""bollinger_fibo_bands — converted from MQL5: MQL5 Indicators/Bollinger bands at Fibonacci levels/bollinger_fibo_bands.mq5

Trade channel for the indicator and the iBand.
The Bollinger bands are located at extended Fibonacci levels.
Copyright: Copyright 2017, Sergey Pavlov (DC2008); Link: http://www.mql5.com/ru/users/dc2008; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, Sergey Pavlov (DC2008)', 'link': 'http://www.mql5.com/ru/users/dc2008', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 15, 'indicator_plots': 11}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1}, 'colors': {1: [13421823], 2: [16764108], 3: [10066430], 4: [16685465], 5: [255], 6: [16711680], 7: [255], 8: [16711680], 9: [255], 10: [16711680], 11: [16711680]}, 'widths': {5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 2}, 'styles': {5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 0}, 'labels': {1: 'Upper bands: fibo 100% - 138.2%', 2: 'Lower bands: fibo 100% - 138.2%', 3: 'Upper bands: fibo 138.2% - 161.8%', 4: 'Lower bands: fibo 138.2% - 161.8%', 5: 'Upper bands: fibo 261.8%', 6: 'Lower  bands: fibo 261.8%', 7: 'Upper bands: fibo 38.2%', 8: 'Lower bands: fibo 38.2%', 9: 'Upper bands: fibo 61.8%', 10: 'Lower bands: fibo 61.8%', 11: 'Middle line'}, 'levels': [], 'description': ['Trade channel for the indicator and the iBand.', 'The Bollinger bands are located at extended Fibonacci levels.'], 'name': 'bollinger_fibo_bands', 'source': 'MQL5 Indicators/Bollinger bands at Fibonacci levels/bollinger_fibo_bands.mq5', 'folder': 'Bollinger bands at Fibonacci levels', 'inputs': [{'mql': 'BB_period', 'py': 'BB_period', 'param': 'BB_period', 'type': 'int', 'default': 80, 'label': 'Moving average period', 'sinput': False}, {'mql': 'BB_deviation', 'py': 'BB_deviation', 'param': 'BB_deviation', 'type': 'double', 'default': 2.0, 'label': 'Number of standard deviations', 'sinput': False}, {'mql': 'BB_applied_price', 'py': 'BB_applied_price', 'param': 'BB_applied_price', 'type': 'int', 'default': 1, 'label': 'Price type', 'sinput': False}, {'mql': 'BB_bands_shift', 'py': 'BB_bands_shift', 'param': 'BB_bands_shift', 'type': 'int', 'default': 0, 'label': 'shift', 'sinput': False}, {'mql': 'history', 'py': 'history', 'param': 'history', 'type': 'int', 'default': 100, 'label': 'History depth', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BB_period = _input('BB_period', 80)  # Moving average period
BB_deviation = _input('BB_deviation', 2.0)  # Number of standard deviations
BB_applied_price = _input('BB_applied_price', PRICE_CLOSE)  # Price type
BB_bands_shift = _input('BB_bands_shift', 0)  # shift
history = _input('history', 100)  # History depth
handle = 0
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Buffer3 = Arr(0, 0.0)
Buffer4 = Arr(0, 0.0)
Buffer5 = Arr(0, 0.0)
Buffer6 = Arr(0, 0.0)
Buffer7 = Arr(0, 0.0)
Buffer8 = Arr(0, 0.0)
Buffer9 = Arr(0, 0.0)
Buffer10 = Arr(0, 0.0)
Buffer11 = Arr(0, 0.0)
Buffer12 = Arr(0, 0.0)
Buffer13 = Arr(0, 0.0)
Buffer14 = Arr(0, 0.0)
Buffer15 = Arr(0, 0.0)
fibo_38 = 0.0
fibo_62 = 0.0
fibo_138 = 0.0
fibo_162 = 0.0
fibo_262 = 0.0
sd = 0
count = 0

def OnInit():
    global count, fibo_138, fibo_162, fibo_262, fibo_38, fibo_62, handle, sd
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    ArraySetAsSeries(Buffer3, True)
    ArraySetAsSeries(Buffer4, True)
    ArraySetAsSeries(Buffer5, True)
    ArraySetAsSeries(Buffer6, True)
    ArraySetAsSeries(Buffer7, True)
    ArraySetAsSeries(Buffer8, True)
    ArraySetAsSeries(Buffer9, True)
    ArraySetAsSeries(Buffer10, True)
    ArraySetAsSeries(Buffer11, True)
    ArraySetAsSeries(Buffer12, True)
    ArraySetAsSeries(Buffer13, True)
    ArraySetAsSeries(Buffer14, True)
    ArraySetAsSeries(Buffer15, True)
    SetIndexBuffer(0, Buffer1, INDICATOR_DATA)
    SetIndexBuffer(1, Buffer2, INDICATOR_DATA)
    SetIndexBuffer(2, Buffer3, INDICATOR_DATA)
    SetIndexBuffer(3, Buffer4, INDICATOR_DATA)
    SetIndexBuffer(4, Buffer5, INDICATOR_DATA)
    SetIndexBuffer(5, Buffer6, INDICATOR_DATA)
    SetIndexBuffer(6, Buffer7, INDICATOR_DATA)
    SetIndexBuffer(7, Buffer8, INDICATOR_DATA)
    SetIndexBuffer(8, Buffer9, INDICATOR_DATA)
    SetIndexBuffer(9, Buffer10, INDICATOR_DATA)
    SetIndexBuffer(10, Buffer11, INDICATOR_DATA)
    SetIndexBuffer(11, Buffer12, INDICATOR_DATA)
    SetIndexBuffer(12, Buffer13, INDICATOR_DATA)
    SetIndexBuffer(13, Buffer14, INDICATOR_DATA)
    SetIndexBuffer(14, Buffer15, INDICATOR_DATA)
    handle = iBands(Symbol(), Period(), BB_period, BB_bands_shift, BB_deviation, BB_applied_price)
    ArraySetAsSeries(MiddleBuffer, True)
    ArraySetAsSeries(UpperBuffer, True)
    ArraySetAsSeries(LowerBuffer, True)
    fibo_38 = 55.0 / 144.0
    fibo_62 = 89.0 / 144.0
    fibo_138 = 2.0 - fibo_62
    fibo_162 = 233.0 / 144.0
    fibo_262 = 377.0 / 144.0
    sd = history
    count = history + BB_period
    ChartRedraw(0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global sd
    rt = rates_total - sd
    for i in range(0, 15):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, rt)
    if count > rates_total:
        sd = rates_total - BB_period
    CopyBuffer(handle, 0, 0, count, MiddleBuffer)
    CopyBuffer(handle, 1, 0, count, UpperBuffer)
    CopyBuffer(handle, 2, 0, count, LowerBuffer)
    mid = 0.0
    std = 0.0
    for i in range(0, count):
        mid = MiddleBuffer[i]
        std = UpperBuffer[i] - mid
        Buffer1[i] = mid + (std * fibo_138)
        Buffer2[i] = UpperBuffer[i]
        Buffer3[i] = LowerBuffer[i]
        Buffer4[i] = mid - (std * fibo_138)
        Buffer5[i] = mid + (std * fibo_162)
        Buffer6[i] = mid + (std * fibo_138)
        Buffer7[i] = mid - (std * fibo_138)
        Buffer8[i] = mid - (std * fibo_162)
        Buffer9[i] = mid + (std * fibo_262)
        Buffer10[i] = mid - (std * fibo_262)
        Buffer11[i] = mid + (std * fibo_38)
        Buffer12[i] = mid - (std * fibo_38)
        Buffer13[i] = mid + (std * fibo_62)
        Buffer14[i] = mid - (std * fibo_62)
        Buffer15[i] = mid
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerFiboBands(_MQL5Indicator):
    name = 'bollinger_fibo_bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'BB_period': 80,  # Moving average period
        'BB_deviation': 2.0,  # Number of standard deviations
        'BB_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price type
        'BB_bands_shift': 0,  # shift
        'history': 100,  # History depth
    }

