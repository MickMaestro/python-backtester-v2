"""WPR support resistance — converted from MQL5: MQL5 Indicators/WPR Support Resistance/WPR support resistance.mq5

WPR support/resistance
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [3329330], 2: [17919]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Support', 2: 'Resistance'}, 'levels': [], 'description': ['WPR support/resistance'], 'name': 'WPR support resistance', 'source': 'MQL5 Indicators/WPR Support Resistance/WPR support resistance.mq5', 'folder': 'WPR Support Resistance', 'inputs': [{'mql': 'inpWprPeriod', 'py': 'inpWprPeriod', 'param': 'inpWprPeriod', 'type': 'int', 'default': 14, 'label': 'WPR period', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': -20.0, 'label': 'Level up', 'sinput': False}, {'mql': 'inpLevelDown', 'py': 'inpLevelDown', 'param': 'inpLevelDown', 'type': 'double', 'default': -80.0, 'label': 'Level down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpWprPeriod = _input('inpWprPeriod', 14)  # WPR period
inpLevelUp = _input('inpLevelUp', -20.0)  # Level up
inpLevelDown = _input('inpLevelDown', -80.0)  # Level down
sup = Arr(0, 0.0)
res = Arr(0, 0.0)
trend = Arr(0, 0.0)
_wprHandle = 0

def OnInit():
    global _wprHandle
    SetIndexBuffer(0, sup, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    SetIndexBuffer(1, res, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    SetIndexBuffer(2, trend, INDICATOR_CALCULATIONS)
    _wprHandle = iWPR(Symbol(), 0, inpWprPeriod)
    if _wprHandle == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPR support/resistance (' + _str(inpWprPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_wprHandle) < rates_total:
        return prev_calculated
    _wprVal = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        trend[i] = (trend[i - 1] if (i > 0) else 0)
        _wprCopied = CopyBuffer(_wprHandle, 0, _DT(time[i]), 1, _wprVal)
        if _wprCopied == 1 and _wprVal[0] > inpLevelUp:
            trend[i] = 1.0
        if _wprCopied == 1 and _wprVal[0] < inpLevelDown:
            trend[i] = -1.0
        sup[i] = (sup[i - 1] if (i > 0) else close[i])
        res[i] = (res[i - 1] if (i > 0) else close[i])
        if i > 0 and trend[i] != trend[i - 1]:
            if trend[i] == 1:
                res[i] = high[i]
            if trend[i] == -1:
                sup[i] = low[i]
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPRSupportResistance(_MQL5Indicator):
    name = 'WPR support resistance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpWprPeriod': 14,  # WPR period
        'inpLevelUp': -20.0,  # Level up
        'inpLevelDown': -80.0,  # Level down
    }

