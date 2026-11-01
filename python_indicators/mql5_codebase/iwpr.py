"""iWPR+ — converted from MQL5: MQL5 Indicators/iWPR+/iWPR+.mq5

iWPR+ is an iWPR %Range function with a positive value.
Because I don't like the negative value of the iWPR function.
Copyright: 2009-2019, MetaQuotes Software Corp. ~ By 3rjfx ~ Created: 26/12/2019; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009-2019, MetaQuotes Software Corp. ~ By 3rjfx ~ Created: 26/12/2019', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'separate', 'indicator_maximum': 100.0, 'indicator_minimum': 0.0, 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [20.0, 80.0], 'description': ['iWPR+ is an iWPR %Range function with a positive value.', "Because I don't like the negative value of the iWPR function."], 'name': 'iWPR+', 'source': 'MQL5 Indicators/iWPR+/iWPR+.mq5', 'folder': 'iWPR+', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 14, 'label': 'iWPR+ Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # iWPR+ Period
WPRBuffer = Arr(0, 0.0)
RANGE = Arr(0, 0.0)
ExtPeriodWPR = 0

def OnInit():
    global ExtPeriodWPR
    if InpPeriod < 3:
        ExtPeriodWPR = 14
        Print('Incorrect InpPeriod value. Indicator will use value= ', ExtPeriodWPR)
    else:
        ExtPeriodWPR = InpPeriod
    IndicatorSetString(INDICATOR_SHORTNAME, 'iWPR+%R' + '(' + _str(ExtPeriodWPR) + ')')
    SetIndexBuffer(0, WPRBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, RANGE, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodWPR + 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    barc = 0
    if rates_total < 100:
        return 0
    limit = rates_total - prev_calculated
    if limit == 0:
        limit = 100
    if prev_calculated > 0:
        limit += 1
    barc = limit - InpPeriod - 2
    ArrayResize(WPRBuffer, limit)
    ArrayResize(RANGE, limit)
    ArraySetAsSeries(WPRBuffer, True)
    ArraySetAsSeries(RANGE, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    i = barc
    for i in range(i, 0 - 1, -1):
        RHigh = high[ArrayMaximum(high, i, InpPeriod)]
        RLow = low[ArrayMinimum(low, i, InpPeriod)]
        RANGE[i] = _fdiv(RHigh - close[i], RHigh - RLow) * 100
        WPRBuffer[i] = fabs(100 - RANGE[i])
    else:
        i = _range_end(i, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IWPR(_MQL5Indicator):
    name = 'iWPR+'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # iWPR+ Period
    }
    y_range = (0.0, 100.0)

