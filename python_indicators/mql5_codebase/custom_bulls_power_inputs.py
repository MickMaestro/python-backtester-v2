"""Custom Bulls Power Inputs — converted from MQL5: MQL5 Indicators/Custom Bulls Power Inputs/Custom Bulls Power Inputs.mq5

Custom Bulls Power Inputs
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [12632256]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Custom Bulls Power Inputs'], 'name': 'Custom Bulls Power Inputs', 'source': 'MQL5 Indicators/Custom Bulls Power Inputs/Custom Bulls Power Inputs.mq5', 'folder': 'Custom Bulls Power Inputs', 'inputs': [{'mql': 'InpBullsPeriod', 'py': 'InpBullsPeriod', 'param': 'InpBullsPeriod', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpColor', 'py': 'InpColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color', 'sinput': False}, {'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'int', 'default': 1, 'label': 'Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBullsPeriod = _input('InpBullsPeriod', 13)  # Period
InpColor = _input('InpColor', clrBlue)  # Color
InpWidth = _input('InpWidth', 1)  # Width
ExtBullsBuffer = Arr(0, 0.0)
ExtTempBuffer = Arr(0, 0.0)
ExtEmaHandle = 0

def OnInit():
    global ExtEmaHandle
    SetIndexBuffer(0, ExtBullsBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTempBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpBullsPeriod - 1)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, InpColor)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, InpWidth)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bulls(' + _str(InpBullsPeriod) + ')')
    ExtEmaHandle = iMA(None, 0, InpBullsPeriod, 0, MODE_EMA, PRICE_CLOSE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    if rates_total < InpBullsPeriod:
        return 0
    calculated = BarsCalculated(ExtEmaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtEmaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtEmaHandle, 0, 0, to_copy, ExtTempBuffer) <= 0:
        Print('getting ExtEmaHandle is failed! Error', GetLastError())
        return 0
    if prev_calculated < InpBullsPeriod:
        limit = InpBullsPeriod
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtBullsBuffer[i] = high[i] - ExtTempBuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomBullsPowerInputs(_MQL5Indicator):
    name = 'Custom Bulls Power Inputs'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBullsPeriod': 13,  # Period
        'InpWidth': 1,  # Width
    }

