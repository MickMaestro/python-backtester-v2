"""vegas — converted from MQL5: MQL5 Indicators/Vegas/vegas.mq5

Copyright: Copyright © 2007, Mr.Bah; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Mr.Bah', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [5197615], 2: [8388736], 3: [255], 4: [16711680], 5: [16711935], 6: [255], 7: [8388736], 8: [5197615]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 1, 7: 1, 8: 1}, 'styles': {1: 4, 2: 4, 3: 4, 4: 0, 5: 0, 6: 4, 7: 4, 8: 4}, 'labels': {1: '+Level 3', 2: '+Level 2', 3: '+Level 1', 4: 'Fast MA', 5: 'Slow MA', 6: '-Level 1', 7: '-Level 2', 8: '-Level 3'}, 'levels': [], 'description': [''], 'name': 'vegas', 'source': 'MQL5 Indicators/Vegas/vegas.mq5', 'folder': 'Vegas', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'RiskModel', 'py': 'RiskModel', 'param': 'RiskModel', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 169, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode
Mode_1 = 1
Mode_2 = 2
Mode_3 = 3
Mode_4 = 4
_enum('Mode', {1: 'Mode_1', 2: 'Mode_2', 3: 'Mode_3', 4: 'Mode_4'})

# ---- inputs and global variables
Step = _input('Step', 10)
RiskModel = _input('RiskModel', Mode_1)
FastPeriod = _input('FastPeriod', 100)
SlowPeriod = _input('SlowPeriod', 169)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
dRange = 0.0
min_rates_total = 0
fMA_Handle = 0
sMA_Handle = 0

def OnInit():
    global dRange, fMA_Handle, min_rates_total, sMA_Handle
    min_rates_total = _int(MathMax(FastPeriod, SlowPeriod))
    dRange = Step * Point()
    fMA_Handle = iMA(None, 0, FastPeriod, 0, MAType, MAPrice)
    if fMA_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iMA 1')
        return INIT_FAILED
    sMA_Handle = iMA(None, 0, SlowPeriod, 0, MAType, MAPrice)
    if sMA_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iMA 2')
        return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer8, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    ArraySetAsSeries(ExtLineBuffer7, True)
    ArraySetAsSeries(ExtLineBuffer8, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Vegas')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(fMA_Handle) < rates_total or BarsCalculated(sMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(fMA_Handle, 0, 0, to_copy, ExtLineBuffer4) <= 0:
        return 0
    if CopyBuffer(sMA_Handle, 0, 0, to_copy, ExtLineBuffer5) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        _sw1 = RiskModel
        if _sw1 == Mode_1:
            ExtLineBuffer3[bar] = ExtLineBuffer5[bar] + (34 * dRange)
            ExtLineBuffer2[bar] = ExtLineBuffer5[bar] + (55 * dRange)
            ExtLineBuffer1[bar] = ExtLineBuffer5[bar] + (89 * dRange)
            ExtLineBuffer6[bar] = ExtLineBuffer5[bar] - (34 * dRange)
            ExtLineBuffer7[bar] = ExtLineBuffer5[bar] - (55 * dRange)
            ExtLineBuffer8[bar] = ExtLineBuffer5[bar] - (89 * dRange)
        elif _sw1 == Mode_2:
            ExtLineBuffer3[bar] = ExtLineBuffer5[bar] + (55 * dRange)
            ExtLineBuffer2[bar] = ExtLineBuffer5[bar] + (89 * dRange)
            ExtLineBuffer1[bar] = ExtLineBuffer5[bar] + (144 * dRange)
            ExtLineBuffer6[bar] = ExtLineBuffer5[bar] - (55 * dRange)
            ExtLineBuffer7[bar] = ExtLineBuffer5[bar] - (88 * dRange)
            ExtLineBuffer8[bar] = ExtLineBuffer5[bar] - (144 * dRange)
        elif _sw1 == Mode_3:
            ExtLineBuffer3[bar] = ExtLineBuffer5[bar] + (89 * dRange)
            ExtLineBuffer2[bar] = ExtLineBuffer5[bar] + (144 * dRange)
            ExtLineBuffer1[bar] = ExtLineBuffer5[bar] + (233 * dRange)
            ExtLineBuffer6[bar] = ExtLineBuffer5[bar] - (89 * dRange)
            ExtLineBuffer7[bar] = ExtLineBuffer5[bar] - (144 * dRange)
            ExtLineBuffer8[bar] = ExtLineBuffer5[bar] - (233 * dRange)
        elif _sw1 == Mode_4:
            ExtLineBuffer3[bar] = ExtLineBuffer5[bar] + (144 * dRange)
            ExtLineBuffer2[bar] = ExtLineBuffer5[bar] + (233 * dRange)
            ExtLineBuffer1[bar] = ExtLineBuffer5[bar] + (377 * dRange)
            ExtLineBuffer6[bar] = ExtLineBuffer5[bar] - (144 * dRange)
            ExtLineBuffer7[bar] = ExtLineBuffer5[bar] - (233 * dRange)
            ExtLineBuffer8[bar] = ExtLineBuffer5[bar] - (377 * dRange)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vegas(_MQL5Indicator):
    name = 'vegas'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 10,
        'RiskModel': _Choice({1: '1', 2: '2', 3: '3', 4: '4'}, default=1),
        'FastPeriod': 100,
        'SlowPeriod': 169,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

