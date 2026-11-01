"""wpr_hist — converted from MQL5: MQL5 Indicators/WPR_Hist/wpr_hist.mq5

Copyright: Copyright 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_minimum': -55.0, 'indicator_maximum': 55.0, 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 3, 2: 3, 3: 3, 4: 3}, 'colors': {1: [16748574], 2: [16748574], 3: [25600], 4: [2237106]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'indicator_color1', 2: 'indicator_color2', 3: 'indicator_color3', 4: 'indicator_color4'}, 'levels': [0.0, 40.0, -40.0], 'description': [], 'name': 'wpr_hist', 'source': 'MQL5 Indicators/WPR_Hist/wpr_hist.mq5', 'folder': 'WPR_Hist', 'inputs': [{'mql': 'InpWPRPeriod', 'py': 'InpWPRPeriod', 'param': 'InpWPRPeriod', 'type': 'int', 'default': 30, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpWPRPeriod = _input('InpWPRPeriod', 30)  # Period
ExtWPRBuffer1 = Arr(0, 0.0)
ExtWPRBuffer2 = Arr(0, 0.0)
ExtWPRLongBuffer1 = Arr(0, 0.0)
ExtWPRShortBuffer1 = Arr(0, 0.0)
ExtWPRPeriod = 0

def OnInit():
    global ExtWPRPeriod
    if InpWPRPeriod < 3:
        ExtWPRPeriod = 30
        Print('Incorrect InpWPRPeriod value. Indicator will use value=', ExtWPRPeriod)
    else:
        ExtWPRPeriod = InpWPRPeriod
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPR_hist' + '(' + _str(ExtWPRPeriod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'up')
    PlotIndexSetString(1, PLOT_LABEL, 'down')
    PlotIndexSetString(2, PLOT_LABEL, 'long')
    PlotIndexSetString(3, PLOT_LABEL, 'short')
    SetIndexBuffer(0, ExtWPRBuffer1)
    SetIndexBuffer(1, ExtWPRBuffer2)
    SetIndexBuffer(2, ExtWPRLongBuffer1)
    SetIndexBuffer(3, ExtWPRShortBuffer1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtWPRPeriod - 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    if rates_total < ExtWPRPeriod:
        return 0
    i = prev_calculated - 1
    if i < (ExtWPRPeriod - 1):
        i = ExtWPRPeriod - 1
    upperShadow = 0.0
    lowerShadow = 0.0
    body = 0.0
    while i < rates_total:
        dMaxHigh = MaxAr(High, ExtWPRPeriod, i)
        dMinLow = MinAr(Low, ExtWPRPeriod, i)
        if dMaxHigh != dMinLow:
            val = _fdiv(100 * (dMaxHigh - Close[i]), dMaxHigh - dMinLow)
            ExtWPRLongBuffer1[i] = 0.0
            if val <= 50:
                ExtWPRBuffer1[i] = (-val) + 50
                ExtWPRBuffer2[i] = 0.0
            else:
                ExtWPRBuffer1[i] = 0.0
                ExtWPRBuffer2[i] = (-val) + 50
            if Close[i] <= Open[i]:
                lowerShadow = Close[i] - Low[i]
                upperShadow = High[i] - Open[i]
                body = Open[i] - Close[i]
            if Close[i] >= Open[i]:
                lowerShadow = Open[i] - Low[i]
                upperShadow = High[i] - Close[i]
                body = Close[i] - Open[i]
            if ((ExtWPRBuffer2[i - 1] < ExtWPRBuffer2[i] and Low[i] <= dMinLow) and (Low[i] < Low[i - 1] or Close[i] > Open[i])) and lowerShadow >= 0:
                ExtWPRLongBuffer1[i] = ExtWPRBuffer2[i]
            elif ((ExtWPRBuffer1[i - 1] > ExtWPRBuffer1[i] and High[i] >= dMaxHigh) and High[i] > High[i - 1]) and upperShadow >= 0:
                ExtWPRShortBuffer1[i] = ExtWPRBuffer1[i]
            else:
                ExtWPRLongBuffer1[i] = 0.0
                ExtWPRShortBuffer1[i] = 0.0
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


class WprHist(_MQL5Indicator):
    name = 'wpr_hist'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpWPRPeriod': 30,  # Period
    }
    y_range = (-55.0, 55.0)

