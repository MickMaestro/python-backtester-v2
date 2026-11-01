"""rvi — converted from MQL5: MQL5 Indicators/Relative Vigor Index (RVI)/rvi.mq5

Relative Vigor Index
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RVI', 2: 'Signal'}, 'levels': [], 'description': ['Relative Vigor Index'], 'name': 'rvi', 'source': 'MQL5 Indicators/Relative Vigor Index (RVI)/rvi.mq5', 'folder': 'Relative Vigor Index (RVI)', 'inputs': [{'mql': 'InpRVIPeriod', 'py': 'InpRVIPeriod', 'param': 'InpRVIPeriod', 'type': 'int', 'default': 10, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpRVIPeriod = _input('InpRVIPeriod', 10)  # Period
ExtRVIBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtRVIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSignalBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpRVIPeriod - 1 + 3)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpRVIPeriod - 1 + (3 * 2))
    IndicatorSetString(INDICATOR_SHORTNAME, 'RVI(' + _str(InpRVIPeriod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'RVI(' + _str(InpRVIPeriod) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Signal(' + _str(InpRVIPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    j = 0
    nLimit = 0
    dValueUp = 0.0
    dValueDown = 0.0
    dNum = 0.0
    dDeNum = 0.0
    if rates_total <= (InpRVIPeriod + (3 * 2) + 2):
        return 0
    if prev_calculated < 0:
        return 0
    nLimit = InpRVIPeriod + 2
    if prev_calculated > (InpRVIPeriod + 3 + 2):
        nLimit = prev_calculated - 1
    if prev_calculated == 0:
        i = 0
        for i in range(i, InpRVIPeriod + 3):
            ExtRVIBuffer[i] = 0.0
        else:
            i = _range_end(i, InpRVIPeriod + 3, 1)
        i = 0
        for i in range(i, InpRVIPeriod + (3 * 2)):
            ExtSignalBuffer[i] = 0.0
        else:
            i = _range_end(i, InpRVIPeriod + (3 * 2), 1)
    i = nLimit
    for i in range(i, rates_total):
        dNum = 0.0
        dDeNum = 0.0
        j = i
        for j in range(j, i - InpRVIPeriod, -1):
            dValueUp = Close[j] - Open[j] + (2 * (Close[j - 1] - Open[j - 1])) + (2 * (Close[j - 2] - Open[j - 2])) + Close[j - 3] - Open[j - 3]
            dValueDown = High[j] - Low[j] + (2 * (High[j - 1] - Low[j - 1])) + (2 * (High[j - 2] - Low[j - 2])) + High[j - 3] - Low[j - 3]
            dNum += dValueUp
            dDeNum += dValueDown
        else:
            j = _range_end(j, i - InpRVIPeriod, -1)
        if dDeNum != 0.0:
            ExtRVIBuffer[i] = _fdiv(dNum, dDeNum)
        else:
            ExtRVIBuffer[i] = dNum
    else:
        i = _range_end(i, rates_total, 1)
    nLimit = InpRVIPeriod + 3 + 2
    if prev_calculated > (InpRVIPeriod + (3 * 2) + 2):
        nLimit = prev_calculated - 1
    i = nLimit
    for i in range(i, rates_total):
        ExtSignalBuffer[i] = (ExtRVIBuffer[i] + (2 * ExtRVIBuffer[i - 1]) + (2 * ExtRVIBuffer[i - 2]) + ExtRVIBuffer[i - 3]) / (3 * 2)
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rvi(_MQL5Indicator):
    name = 'rvi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpRVIPeriod': 10,  # Period
    }

