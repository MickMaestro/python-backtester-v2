"""TrendStrength average — converted from MQL5: MQL5 Indicators/Trend Strength Average/TrendStrength average.mq5

TrendStrength average
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11119017], 2: [16748574], 3: [6333684]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'average', 2: 'trend up', 3: 'trend down'}, 'levels': [], 'description': ['TrendStrength average'], 'name': 'TrendStrength average', 'source': 'MQL5 Indicators/Trend Strength Average/TrendStrength average.mq5', 'folder': 'Trend Strength Average', 'inputs': [{'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'inpMaMethod', 'py': 'inpMaMethod', 'param': 'inpMaMethod', 'type': 'int', 'default': 0, 'label': 'Average method', 'sinput': False}, {'mql': 'inpStrength', 'py': 'inpStrength', 'param': 'inpStrength', 'type': 'double', 'default': 4.236, 'label': 'Strength', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMaPeriod = _input('inpMaPeriod', 14)  # Average period
inpMaMethod = _input('inpMaMethod', MODE_SMA)  # Average method
inpStrength = _input('inpStrength', 4.236)  # Strength
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
avg = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
smin = Arr(0, 0.0)
smax = Arr(0, 0.0)
trend = Arr(0, 0.0)
_maHandle = 0

def OnInit():
    global _maHandle
    SetIndexBuffer(0, avg, INDICATOR_DATA)
    SetIndexBuffer(1, valu, INDICATOR_DATA)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    SetIndexBuffer(3, smin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, smax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, trend, INDICATOR_CALCULATIONS)
    _maHandle = iMA(Symbol(), 0, inpMaPeriod, 0, inpMaMethod, inpPrice)
    if _maHandle == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendStrength average (' + _str(inpMaPeriod) + ',' + _str(inpStrength) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_maHandle) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        _maVal = Arr(1, 0.0, dyn=False)
        _maValCopied = CopyBuffer(_maHandle, 0, _DT(time[i]), 1, _maVal)
        avg[i] = (_maVal[0] if (_maValCopied == 1) else 0)
        valu[i] = EMPTY_VALUE
        vald[i] = EMPTY_VALUE
        trend[i] = 0.0
        if i > 0:
            havg = avg[i]
            lavg = avg[i]
            if avg[i] > avg[i - 1]:
                havg = avg[i]
                lavg = avg[i - 1]
            if avg[i] < avg[i - 1]:
                havg = avg[i - 1]
                lavg = avg[i]
            delta = havg - lavg
            smin[i] = avg[i] - (inpStrength * delta)
            smax[i] = avg[i] + (inpStrength * delta)
            trend[i] = trend[i - 1]
            if avg[i] > smax[i - 1]:
                trend[i] = 1.0
            if avg[i] < smin[i - 1]:
                trend[i] = -1.0
            if trend[i] > 0:
                if smin[i] < smin[i - 1]:
                    smin[i] = smin[i - 1]
                valu[i] = smin[i]
            if trend[i] < 0:
                if smax[i] > smax[i - 1]:
                    smax[i] = smax[i - 1]
                vald[i] = smax[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendStrengthAverage(_MQL5Indicator):
    name = 'TrendStrength average'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaPeriod': 14,  # Average period
        'inpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Average method
        'inpStrength': 4.236,  # Strength
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

