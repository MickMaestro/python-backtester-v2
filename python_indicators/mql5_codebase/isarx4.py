"""isarx4 — converted from MQL5: MQL5 Indicators/iSarX4/isarx4.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [16711935], 3: [65280], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {}, 'labels': {1: 'iSar 1', 2: 'iSar 2', 3: 'iSar 3', 4: 'iSar 4'}, 'levels': [], 'description': [], 'name': 'isarx4', 'source': 'MQL5 Indicators/iSarX4/isarx4.mq5', 'folder': 'iSarX4', 'inputs': [{'mql': 'Start_Step', 'py': 'Start_Step', 'param': 'Start_Step', 'type': 'double', 'default': 0.002, 'label': 'Step for the lowest indicator', 'sinput': False}, {'mql': 'Step_Shift', 'py': 'Step_Shift', 'param': 'Step_Shift', 'type': 'double', 'default': 0.002, 'label': 'Step changing size', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'Maximum for all indicators', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Start_Step = _input('Start_Step', 0.002)  # Step for the lowest indicator
Step_Shift = _input('Step_Shift', 0.002)  # Step changing size
Maximum = _input('Maximum', 0.2)  # Maximum for all indicators
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)
ExtMapBuffer4 = Arr(0, 0.0)
min_rates_total = 0
Sar1_Handle = 0
Sar2_Handle = 0
Sar3_Handle = 0
Sar4_Handle = 0

def OnInit():
    global Sar1_Handle, Sar2_Handle, Sar3_Handle, Sar4_Handle, min_rates_total
    min_rates_total = 3
    Sar1_Handle = iSAR(None, PERIOD_CURRENT, Start_Step, Maximum)
    if Sar1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Sar1 indicator')
        return 1
    Sar2_Handle = iSAR(None, PERIOD_CURRENT, Start_Step + (1 * Step_Shift), Maximum)
    if Sar2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Sar2 indicator')
        return 1
    Sar3_Handle = iSAR(None, PERIOD_CURRENT, Start_Step + (2 * Step_Shift), Maximum)
    if Sar3_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Sar3 indicator')
        return 1
    Sar4_Handle = iSAR(None, PERIOD_CURRENT, Start_Step + (3 * Step_Shift), Maximum)
    if Sar4_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Sar4 indicator')
        return 1
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBuffer1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBuffer2, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, ExtMapBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBuffer3, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ExtMapBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBuffer4, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'iSarX4(', DoubleToString(Start_Step, 3), ', ', DoubleToString(Step_Shift, 3), ', ', DoubleToString(Maximum, 3), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(Sar1_Handle) < rates_total or BarsCalculated(Sar2_Handle) < rates_total) or BarsCalculated(Sar3_Handle) < rates_total) or BarsCalculated(Sar4_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(Sar1_Handle, 0, 0, to_copy, ExtMapBuffer1) <= 0:
        return 0
    if CopyBuffer(Sar2_Handle, 0, 0, to_copy, ExtMapBuffer2) <= 0:
        return 0
    if CopyBuffer(Sar3_Handle, 0, 0, to_copy, ExtMapBuffer3) <= 0:
        return 0
    if CopyBuffer(Sar4_Handle, 0, 0, to_copy, ExtMapBuffer4) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Isarx4(_MQL5Indicator):
    name = 'isarx4'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Start_Step': 0.002,  # Step for the lowest indicator
        'Step_Shift': 0.002,  # Step changing size
        'Maximum': 0.2,  # Maximum for all indicators
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

