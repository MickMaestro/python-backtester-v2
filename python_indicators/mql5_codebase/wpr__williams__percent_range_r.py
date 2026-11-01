"""wpr — converted from MQL5: MQL5 Indicators/Williams’ Percent Range (%R)/wpr.mq5

Larry Williams' Percent Range
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_maximum': 0.0, 'indicator_minimum': -100.0, 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [-20.0, -80.0], 'description': ["Larry Williams' Percent Range"], 'name': 'wpr', 'source': 'MQL5 Indicators/Williams’ Percent Range (%R)/wpr.mq5', 'folder': 'Williams’ Percent Range (%R)', 'inputs': [{'mql': 'InpWPRPeriod', 'py': 'InpWPRPeriod', 'param': 'InpWPRPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpWPRPeriod = _input('InpWPRPeriod', 14)  # Period
ExtWPRBuffer = Arr(0, 0.0)
ExtPeriodWPR = 0

def OnInit():
    global ExtPeriodWPR
    if InpWPRPeriod < 3:
        ExtPeriodWPR = 14
        Print('Incorrect InpWPRPeriod value. Indicator will use value=', ExtPeriodWPR)
    else:
        ExtPeriodWPR = InpWPRPeriod
    IndicatorSetString(INDICATOR_SHORTNAME, '%R' + '(' + _str(ExtPeriodWPR) + ')')
    SetIndexBuffer(0, ExtWPRBuffer)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodWPR - 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < ExtPeriodWPR:
        return 0
    i = prev_calculated - 1
    if i < (ExtPeriodWPR - 1):
        i = ExtPeriodWPR - 1
    while i < rates_total:
        dMaxHigh = MaxAr(High, ExtPeriodWPR, i)
        dMinLow = MinAr(Low, ExtPeriodWPR, i)
        if dMaxHigh != dMinLow:
            ExtWPRBuffer[i] = _fdiv((-(dMaxHigh - Close[i])) * 100, dMaxHigh - dMinLow)
        else:
            ExtWPRBuffer[i] = ExtWPRBuffer[i - 1]
        i += 1
    return rates_total

def MaxAr(array, period, cur_position):
    Highest = array[cur_position]
    for i in range(cur_position - 1, cur_position - period, -1):
        if Highest < array[i]:
            Highest = array[i]
    return Highest

def MinAr(array, period, cur_position):
    Lowest = array[cur_position]
    for i in range(cur_position - 1, cur_position - period, -1):
        if Lowest > array[i]:
            Lowest = array[i]
    return Lowest


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wpr(_MQL5Indicator):
    name = 'wpr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpWPRPeriod': 14,  # Period
    }
    y_range = (-100.0, 0.0)

