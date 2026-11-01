"""Double MA Cross — converted from MQL5: MQL5 Indicators/Doulble MA Cross Draw Histogram/Double MA Cross.mq5

Copyright: Submarine; Link: https://www.mql5.com/zh/users/carllin000; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Submarine', 'link': 'https://www.mql5.com/zh/users/carllin000', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 4, 4: 4}, 'colors': {1: [255], 2: [32768], 3: [255], 4: [32768]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'FastLine', 2: 'SlowLine', 3: 'Linear', 4: 'XLinear1'}, 'levels': [], 'description': [], 'name': 'Double MA Cross', 'source': 'MQL5 Indicators/Doulble MA Cross Draw Histogram/Double MA Cross.mq5', 'folder': 'Doulble MA Cross Draw Histogram', 'inputs': [{'mql': 'CommandFM', 'py': 'CommandFM', 'param': None, 'type': 'string', 'default': '=====Fast_MA Paramater=====', 'label': '', 'sinput': False}, {'mql': 'FastMA_timeframe', 'py': 'FastMA_timeframe', 'param': 'FastMA_timeframe', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'FastMA_period', 'py': 'FastMA_period', 'param': 'FastMA_period', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'FastMA_shift', 'py': 'FastMA_shift', 'param': 'FastMA_shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'FastMA_method', 'py': 'FastMA_method', 'param': 'FastMA_method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'FastMA_applied_price', 'py': 'FastMA_applied_price', 'param': 'FastMA_applied_price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'CommandSM', 'py': 'CommandSM', 'param': None, 'type': 'string', 'default': '=====Slow_MA Paramater=====', 'label': '', 'sinput': False}, {'mql': 'SlowMA_timeframe', 'py': 'SlowMA_timeframe', 'param': 'SlowMA_timeframe', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SlowMA_period', 'py': 'SlowMA_period', 'param': 'SlowMA_period', 'type': 'int', 'default': 36, 'label': '', 'sinput': False}, {'mql': 'SlowMA_shift', 'py': 'SlowMA_shift', 'param': 'SlowMA_shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SlowMA_method', 'py': 'SlowMA_method', 'param': 'SlowMA_method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SlowMA_applied_price', 'py': 'SlowMA_applied_price', 'param': 'SlowMA_applied_price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CommandFM = _input('CommandFM', '=====Fast_MA Paramater=====')
FastMA_timeframe = _input('FastMA_timeframe', 0)
FastMA_period = _input('FastMA_period', 9)
FastMA_shift = _input('FastMA_shift', 0)
FastMA_method = _input('FastMA_method', 0)
FastMA_applied_price = _input('FastMA_applied_price', PRICE_CLOSE)
CommandSM = _input('CommandSM', '=====Slow_MA Paramater=====')
SlowMA_timeframe = _input('SlowMA_timeframe', 0)
SlowMA_period = _input('SlowMA_period', 36)
SlowMA_shift = _input('SlowMA_shift', 0)
SlowMA_method = _input('SlowMA_method', 0)
SlowMA_applied_price = _input('SlowMA_applied_price', PRICE_CLOSE)
FastLineBuffer = Arr(0, 0.0)
SlowLineBuffer = Arr(0, 0.0)
LinearBuffer1 = Arr(0, 0.0)
LinearBuffer2 = Arr(0, 0.0)
LinearXBuffer1 = Arr(0, 0.0)
LinearXBuffer2 = Arr(0, 0.0)
FastShift = 0
SlowShift = 0

def OnInit():
    global FastShift, SlowShift
    SetIndexBuffer(0, FastLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SlowLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LinearBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, LinearBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, LinearXBuffer1, INDICATOR_DATA)
    SetIndexBuffer(5, LinearXBuffer2, INDICATOR_DATA)
    FastShift = iMA(None, FastMA_timeframe, FastMA_period, FastMA_shift, FastMA_method, FastMA_applied_price)
    SlowShift = iMA(None, SlowMA_timeframe, SlowMA_period, SlowMA_shift, SlowMA_method, SlowMA_applied_price)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    Fast = Arr(0, 0.0)
    if CopyBuffer(FastShift, 0, 0, rates_total, Fast) <= 0:
        return 0
    Slow = Arr(0, 0.0)
    if CopyBuffer(SlowShift, 0, 0, rates_total, Slow) <= 0:
        return 0
    start = 100
    if prev_calculated > 0:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        FastLineBuffer[i] = Fast[i]
        SlowLineBuffer[i] = Slow[i]
        if FastLineBuffer[i] >= SlowLineBuffer[i]:
            LinearBuffer1[i] = Fast[i]
            LinearBuffer2[i] = Slow[i]
        else:
            LinearXBuffer1[i] = Slow[i]
            LinearXBuffer2[i] = Fast[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleMACross(_MQL5Indicator):
    name = 'Double MA Cross'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMA_timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'FastMA_period': 9,
        'FastMA_shift': 0,
        'FastMA_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'FastMA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'SlowMA_timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),
        'SlowMA_period': 36,
        'SlowMA_shift': 0,
        'SlowMA_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'SlowMA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

