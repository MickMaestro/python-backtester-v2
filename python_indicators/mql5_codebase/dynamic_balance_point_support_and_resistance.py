"""Dynamic balance point - support and resistance — converted from MQL5: MQL5 Indicators/Dynamic Balance Point - Support & Resistance/Dynamic balance point - support and resistance.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16748574, 6333684]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Dynamic balance point support & resistance'}, 'levels': [], 'description': [], 'name': 'Dynamic balance point - support and resistance', 'source': 'MQL5 Indicators/Dynamic Balance Point - Support & Resistance/Dynamic balance point - support and resistance.mq5', 'folder': 'Dynamic Balance Point - Support & Resistance', 'inputs': [{'mql': 'inpDbpPeriod', 'py': 'inpDbpPeriod', 'param': 'inpDbpPeriod', 'type': 'int', 'default': 5, 'label': 'Dynamic balance point period', 'sinput': False}, {'mql': 'inpDbpTimeFrame', 'py': 'inpDbpTimeFrame', 'param': 'inpDbpTimeFrame', 'type': 'int', 'default': 16408, 'label': 'Dynamic balance point time frame', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpDbpPeriod = _input('inpDbpPeriod', 5)  # Dynamic balance point period
inpDbpTimeFrame = _input('inpDbpTimeFrame', PERIOD_D1)  # Dynamic balance point time frame
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
dpb = Arr(0, 0.0)
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    if inpDbpTimeFrame <= Period():
        Alert('Or set the time frame parameter to a time frame higher than ' + timeFrameToString(Period()))
        Alert('Indicator must be used on time frame lower than ' + timeFrameToString(inpDbpTimeFrame))
        return INIT_FAILED
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, dpb, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dynamic balance point S/R (' + _str(inpDbpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _start = 0
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _times = Arr(0, 0)
        _timesCopied = CopyTime(Symbol(), inpDbpTimeFrame, _DT(time[i]), inpDbpPeriod, _times)
        if _timesCopied != inpDbpPeriod:
            break
        if time[_start] < _times[0]:
            _start = i
            while _start > 1:
                if time[_start] == _times[0] or time[_start - 1] < _times[0]:
                    break
                _start -= 1
        hi = high[ArrayMaximum(high, _start, i - _start + 1)]
        lo = low[ArrayMinimum(low, _start, i - _start + 1)]
        dpb[i] = (hi + lo + close[i]) / 3.0
        val[i] = (MathMax((val[i - 1] if (i > 0) else dpb[i]), dpb[i]) if (close[i] > dpb[i]) else MathMin((val[i - 1] if (i > 0) else dpb[i]), dpb[i]))
        valc[i] = (0 if (close[i] > dpb[i]) else 1)
        i += 1
    return i

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicBalancePointSupportAndResistance(_MQL5Indicator):
    name = 'Dynamic balance point - support and resistance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDbpPeriod': 5,  # Dynamic balance point period
        'inpDbpTimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Dynamic balance point time frame
    }

