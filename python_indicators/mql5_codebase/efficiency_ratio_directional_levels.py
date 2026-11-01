"""Efficiency ratio directional levels — converted from MQL5: MQL5 Indicators/Efficiency ratio directional with levels/Efficiency ratio directional levels.mq5

Kaufman efficiency ratio
Directional efficiency ratio
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [11119017, 16760576, 17919]}, 'widths': {3: 2}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'Level up', 2: 'Level down', 3: 'Efficiency ratio'}, 'levels': [], 'description': ['Kaufman efficiency ratio', 'Directional efficiency ratio'], 'name': 'Efficiency ratio directional levels', 'source': 'MQL5 Indicators/Efficiency ratio directional with levels/Efficiency ratio directional levels.mq5', 'folder': 'Efficiency ratio directional with levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'ER period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpSmoothingPeriod', 'py': 'inpSmoothingPeriod', 'param': 'inpSmoothingPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpLevelPeriod', 'py': 'inpLevelPeriod', 'param': 'inpLevelPeriod', 'type': 'double', 'default': 10.0, 'label': 'Levels period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # ER period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpSmoothingPeriod = _input('inpSmoothingPeriod', 5)  # Smoothing period
inpLevelPeriod = _input('inpLevelPeriod', 10.0)  # Levels period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
lup = Arr(0, 0.0)
ldn = Arr(0, 0.0)
ª_alpha = 0.0
ª_alphal = 0.0
_erArray = Arr(0, 0.0, dims=(3,))

def OnInit():
    global ª_alpha, ª_alphal
    SetIndexBuffer(0, lup, INDICATOR_DATA)
    SetIndexBuffer(1, ldn, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    ª_alpha = _fdiv(2.0, 1.0 + (inpSmoothingPeriod if (inpSmoothingPeriod > 1) else 1))
    ª_alphal = _fdiv(2.0, 1.0 + (inpLevelPeriod if (inpLevelPeriod > 1) else 1))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Efficiency ratio (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _efr = iEr(getPrice(inpPrice, open, close, high, low, i), inpPeriod, i, rates_total)
        val[i] = ((val[i - 1] + (ª_alpha * (_efr - val[i - 1]))) if (i > 0) else _efr)
        lup[i] = ((lup[i - 1] if (val[i] < ldn[i - 1]) else (lup[i - 1] + (ª_alphal * (val[i] - lup[i - 1])))) if (i > 0) else val[i])
        ldn[i] = ((ldn[i - 1] if (val[i] > lup[i - 1]) else (ldn[i - 1] + (ª_alphal * (val[i] - ldn[i - 1])))) if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > lup[i]) else 2 if (val[i] < ldn[i]) else 0)
        i += 1
    return i

def iEr(value, period, i, bars, instance=0):
    global _s_iEr__arrayError, _s_iEr__arrayResizedTo
    if _s_iEr__arrayResizedTo < bars:
        _res = bars + 500
        _res -= ArrayResize(_erArray, bars + 500)
        if _res:
            _s_iEr__arrayError = True
        else:
            _s_iEr__arrayResizedTo = bars + 500
    instance *= 3
    _erArray[i][instance] = value
    _erArray[i][instance + 1] = (((_erArray[i][instance] - _erArray[i - 1][instance]) if (_erArray[i][instance] > _erArray[i - 1][instance]) else (_erArray[i - 1][instance] - _erArray[i][instance])) if (i > 0) else 0)
    if i <= period:
        _erArray[i][instance + 2] = _erArray[i][instance + 1]
        k = 1
        while k < period and (i - k) >= 0:
            _erArray[i][instance + 2] += _erArray[i - k][instance + 1]
            k += 1
    else:
        _erArray[i][instance + 2] = _erArray[i - 1][instance + 2] - _erArray[i - period][instance + 1] + _erArray[i][instance + 1]
    _efr = (_fdiv(_erArray[i][instance] - _erArray[i - period][instance], _erArray[i][instance + 2]) if (_erArray[i][instance + 2] != 0 and i > period) else 0)
    return _efr

def getPrice(tprice, open, close, high, low, i):
    _sw1 = tprice
    if _sw1 == PRICE_CLOSE:
        return close[i]
    elif _sw1 == PRICE_OPEN:
        return open[i]
    elif _sw1 == PRICE_HIGH:
        return high[i]
    elif _sw1 == PRICE_LOW:
        return low[i]
    elif _sw1 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- static local variables
_s_iEr__arrayError = False
_s_iEr__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EfficiencyRatioDirectionalLevels(_MQL5Indicator):
    name = 'Efficiency ratio directional levels'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 32,  # ER period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpSmoothingPeriod': 5,  # Smoothing period
        'inpLevelPeriod': 10.0,  # Levels period
    }

