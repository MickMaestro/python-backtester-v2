"""Price channel stop — converted from MQL5: MQL5 Indicators/Price Channel Stop/Price channel stop.mq5

Price channel stop
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [15130800, 12180223], 2: [16760576, 36095]}, 'widths': {2: 1}, 'styles': {}, 'labels': {1: 'Price channel stop', 2: 'Price channel stop'}, 'levels': [], 'description': ['Price channel stop'], 'name': 'Price channel stop', 'source': 'MQL5 Indicators/Price Channel Stop/Price channel stop.mq5', 'folder': 'Price Channel Stop', 'inputs': [{'mql': 'inpChannelPeriod', 'py': 'inpChannelPeriod', 'param': 'inpChannelPeriod', 'type': 'int', 'default': 14, 'label': 'Channel period', 'sinput': False}, {'mql': 'inpRisk', 'py': 'inpRisk', 'param': 'inpRisk', 'type': 'double', 'default': 0.3, 'label': 'Risk', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpChannelPeriod = _input('inpChannelPeriod', 14)  # Channel period
inpRisk = _input('inpRisk', 0.3)  # Risk
line = Arr(0, 0.0)
linec = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
bsmin = Arr(0, 0.0)
bsmax = Arr(0, 0.0)
trend = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, line, INDICATOR_DATA)
    SetIndexBuffer(3, linec, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, bsmin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, bsmax, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Price channel stop (' + _str(inpChannelPeriod) + ',' + _str(inpRisk) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpChannelPeriod + 1, 0)
        smin = low[ArrayMinimum(low, _start, inpChannelPeriod)]
        smax = high[ArrayMaximum(high, _start, inpChannelPeriod)]
        mid = 0.5 * (smin + smax)
        bsmax[i] = smax - ((smax - smin) * MathMin(inpRisk, 0.49))
        bsmin[i] = smin + ((smax - smin) * MathMin(inpRisk, 0.49))
        trend[i] = (trend[i - 1] if (i > 0) else 0)
        if inpRisk > 0:
            if close[i] > bsmax[i]:
                trend[i] = 1.0
            if close[i] < bsmin[i]:
                trend[i] = -1.0
        else:
            if i > 0 and close[i] > bsmax[i - 1]:
                trend[i] = 1.0
            if i > 0 and close[i] < bsmin[i - 1]:
                trend[i] = -1.0
        if trend[i] > 0 and bsmin[i] < bsmin[i - 1]:
            bsmin[i] = bsmin[i - 1]
        if trend[i] < 0 and bsmax[i] > bsmax[i - 1]:
            bsmax[i] = bsmax[i - 1]
        if trend[i] > 0:
            filld[i] = bsmin[i]
            fillu[i] = mid
        if trend[i] < 0:
            fillu[i] = mid
            filld[i] = bsmax[i]
        line[i] = filld[i]
        linec[i] = (0 if (trend[i] == 1) else 1)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceChannelStop(_MQL5Indicator):
    name = 'Price channel stop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpChannelPeriod': 14,  # Channel period
        'inpRisk': 0.3,  # Risk
    }

