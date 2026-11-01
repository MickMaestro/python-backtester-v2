"""muv_diff — converted from MQL5: MQL5 Indicators/MUV_DIFF/muv_diff.mq5

Copyright: Copyright © 2008, svm-d; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, svm-d', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'SMA MUV_DIFF', 2: 'EMA MUV_DIFF'}, 'levels': [0.0], 'description': [], 'name': 'muv_diff', 'source': 'MQL5 Indicators/MUV_DIFF/muv_diff.mq5', 'folder': 'MUV_DIFF', 'inputs': [{'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'uint', 'default': 14, 'label': 'the indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MAPeriod = _input('MAPeriod', 14)  # the indicator period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
SmaDiffBuffer = Arr(0, 0.0)
EmaDiffBuffer = Arr(0, 0.0)
E_Handle = 0
S_Handle = 0
min_rates_total = 0

def OnInit():
    global E_Handle, S_Handle, min_rates_total
    min_rates_total = _int(MAPeriod + 1)
    S_Handle = iCustom(None, 0, 'XMUV', 0, MAPeriod, 0, 0, 0)
    if S_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of XMUV SMA indicator')
    E_Handle = iCustom(None, 0, 'XMUV', 1, MAPeriod, 0, 0, 0)
    if E_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of XMUV EMA indicator')
    SetIndexBuffer(0, SmaDiffBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SmaDiffBuffer, True)
    SetIndexBuffer(1, EmaDiffBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(EmaDiffBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'MUV_DIFF(', MAPeriod, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(S_Handle) < rates_total or BarsCalculated(E_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    SDiff = Arr(0, 0.0)
    EDiff = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(S_Handle, 0, 0, to_copy, SDiff) <= 0:
        return 0
    if CopyBuffer(E_Handle, 0, 0, to_copy, EDiff) <= 0:
        return 0
    ArraySetAsSeries(SDiff, True)
    ArraySetAsSeries(EDiff, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SmaDiffBuffer[bar] = _fdiv(SDiff[bar] - SDiff[bar + 1], Point())
        EmaDiffBuffer[bar] = _fdiv(EDiff[bar] - EDiff[bar + 1], Point())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MuvDiff(_MQL5Indicator):
    name = 'muv_diff'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAPeriod': 14,  # the indicator period
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

