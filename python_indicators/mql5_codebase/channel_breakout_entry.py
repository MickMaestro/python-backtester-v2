"""channel_breakout_entry — converted from MQL5: MQL5 Indicators/channel_breakout_entry/channel_breakout_entry.mq5

Copyright: Copyright © 2009, darmasdt; Link: http://indotraders.org/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, darmasdt', 'link': 'http://indotraders.org/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [11119017], 2: [11119017], 3: [16748574], 4: [16748574], 5: [4678655], 6: [4678655], 7: [16436871], 8: [14524637]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, 'labels': {1: 'trailing_Up', 2: 'trailing_Dn', 3: 'sys1_Up', 4: 'sys1_Dn', 5: 'failsafe_Up', 6: 'failsafe_Dn', 7: 'Sys 1 Stp', 8: 'Sys 2 Stp'}, 'levels': [], 'description': [''], 'name': 'channel_breakout_entry', 'source': 'MQL5 Indicators/channel_breakout_entry/channel_breakout_entry.mq5', 'folder': 'channel_breakout_entry', 'inputs': [{'mql': 'Range1', 'py': 'Range1', 'param': 'Range1', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Range2', 'py': 'Range2', 'param': 'Range2', 'type': 'uint', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'Range3', 'py': 'Range3', 'param': 'Range3', 'type': 'uint', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'atr_factor', 'py': 'atr_factor', 'param': 'atr_factor', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'atr_range', 'py': 'atr_range', 'param': 'atr_range', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Range1 = _input('Range1', 10)
Range2 = _input('Range2', 20)
Range3 = _input('Range3', 55)
atr_factor = _input('atr_factor', 2.0)
atr_range = _input('atr_range', 14)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = _int(MathMax(MathMax(MathMax(Range1, atr_factor), Range2), Range3))
    ATR_Handle = iATR(None, 0, atr_range)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
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
    shortname = Box("")
    StringConcatenate(shortname, 'channel_breakout_entry(', Range1, ',', Range2, ',', Range3, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ATR = Arr(0, 0.0)
    limit = 0
    to_copy = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 2
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtLineBuffer1[bar] = high[ArrayMaximum(high, bar, Range1)]
        ExtLineBuffer2[bar] = low[ArrayMinimum(low, bar, Range1)]
        ExtLineBuffer3[bar] = high[ArrayMaximum(high, bar, Range2)]
        ExtLineBuffer4[bar] = low[ArrayMinimum(low, bar, Range2)]
        ExtLineBuffer5[bar] = high[ArrayMaximum(high, bar, Range3)]
        ExtLineBuffer6[bar] = low[ArrayMinimum(low, bar, Range3)]
        if high[bar + 1] <= ExtLineBuffer3[bar + 1] and high[bar] > ExtLineBuffer3[bar]:
            ExtLineBuffer7[bar] = ExtLineBuffer3[bar] - (ATR[bar + 1] * atr_factor)
        if high[bar + 1] <= ExtLineBuffer5[bar + 1] and high[bar] > ExtLineBuffer5[bar]:
            ExtLineBuffer8[bar] = ExtLineBuffer5[bar] - (ATR[bar + 1] * atr_factor)
        if low[bar + 1] >= ExtLineBuffer4[bar + 1] and low[bar] < ExtLineBuffer4[bar]:
            ExtLineBuffer7[bar] = ExtLineBuffer4[bar] + (ATR[bar + 1] * atr_factor)
        if low[bar + 1] >= ExtLineBuffer6[bar + 1] and ExtLineBuffer6[bar]:
            ExtLineBuffer8[bar] = ExtLineBuffer6[bar] + (ATR[bar + 1] * atr_factor)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChannelBreakoutEntry(_MQL5Indicator):
    name = 'channel_breakout_entry'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Range1': 10,
        'Range2': 20,
        'Range3': 55,
        'atr_factor': 2.0,
        'atr_range': 14,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

