"""Hull levels — converted from MQL5: MQL5 Indicators/Hull levels/Hull levels.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 8}, 'colors': {1: [3329434, 9662683], 2: [32768], 3: [9639167], 4: [12632256, 7451452, 9639167]}, 'widths': {4: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'filling', 2: 'up level', 3: 'down level', 4: 'Hull'}, 'levels': [], 'description': [], 'name': 'Hull levels', 'source': 'MQL5 Indicators/Hull levels/Hull levels.mq5', 'folder': 'Hull levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpDivisor', 'py': 'inpDivisor', 'param': 'inpDivisor', 'type': 'double', 'default': 2.0, 'label': 'Divisor ("speed")', 'sinput': False}, {'mql': 'inpPeriodl', 'py': 'inpPeriodl', 'param': 'inpPeriodl', 'type': 'double', 'default': 3.0, 'label': 'Levels period (<=1 for same as Hull period)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDisplay', 'py': 'inpDisplay', 'param': 'inpDisplay', 'type': 'int', 'default': 0, 'label': 'Filled zones display :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayFill
fill_display = 0
fill_dont = 1
_enum('enDisplayFill', {0: 'fill_display', 1: 'fill_dont'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpDivisor = _input('inpDivisor', 2.0)  # Divisor ("speed")
inpPeriodl = _input('inpPeriodl', 3.0)  # Levels period (<=1 for same as Hull period)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDisplay = _input('inpDisplay', fill_display)  # Filled zones display :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levelUp = Arr(0, 0.0)
levelDn = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
_levelsPeriod = 0.0
_alphaLevels = 0.0
_workHull = Arr(0, 0.0, dims=(12,))

def OnInit():
    global _alphaLevels, _levelsPeriod
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, levelUp, INDICATOR_DATA)
    SetIndexBuffer(3, levelDn, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    _levelsPeriod = (inpPeriod if (inpPeriodl <= 1) else inpPeriodl)
    _alphaLevels = _fdiv(2.0, 1.0 + _levelsPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hull (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        val[i] = iHull(_price, inpPeriod, inpDivisor, i, rates_total, 0)
        levelUp[i] = (((levelUp[i - 1] + (_alphaLevels * (val[i] - levelUp[i - 1]))) if (val[i] > levelDn[i - 1]) else levelUp[i - 1]) if (i > 0) else val[i])
        levelDn[i] = (((levelDn[i - 1] + (_alphaLevels * (val[i] - levelDn[i - 1]))) if (val[i] < levelUp[i - 1]) else levelDn[i - 1]) if (i > 0) else val[i])
        valc[i] = (1 if (val[i] > levelUp[i]) else 2 if (val[i] < levelDn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        fillu[i] = (EMPTY_VALUE if (inpDisplay == fill_dont) else val[i])
        filld[i] = (EMPTY_VALUE if (inpDisplay == fill_dont) else val[i] if (valc[i] == 0) else levelUp[i] if (valc[i] == 1) else levelDn[i])
        i += 1
    return i

def iHull(price, period, divisor, i, bars, _inst=0):
    global _s_iHull__arrayError, _s_iHull__arrayResizedTo
    if _s_iHull__arrayResizedTo < bars:
        _res = bars + 500
        _res -= ArrayResize(_workHull, _res)
        if _res:
            _s_iHull__arrayError = True
        else:
            _s_iHull__arrayResizedTo = bars + 500
    if _workHull[0][_inst] != period:
        _workHull[0][_inst] = period
        _workHull[2][_inst] = (period if (period > 1) else 1)
        _workHull[1][_inst] = _int((_fdiv(_workHull[2][_inst], (divisor if (divisor > 1) else 1)) if (_workHull[2][_inst] > 1) else 1))
        _workHull[3][_inst] = _int(MathSqrt(_workHull[2][_inst]))
    _workHull[i][_inst + 1] = price
    if i > _workHull[2][_inst]:
        _workHull[i][_inst + 9] = _workHull[i - 1][_inst + 9]
        _workHull[i][_inst + 3] = _workHull[i - 1][_inst + 3] + (price * _workHull[1][_inst]) - _workHull[i - 1][_inst + 6]
        _workHull[i][_inst + 6] = _workHull[i - 1][_inst + 6] + price - _workHull[i - _int(_workHull[1][_inst])][_inst + 1]
        _workHull[i][_inst + 10] = _workHull[i - 1][_inst + 10]
        _workHull[i][_inst + 4] = _workHull[i - 1][_inst + 4] + (price * _workHull[2][_inst]) - _workHull[i - 1][_inst + 7]
        _workHull[i][_inst + 7] = _workHull[i - 1][_inst + 7] + price - _workHull[i - _int(_workHull[2][_inst])][_inst + 1]
    else:
        _workHull[i][_inst + 4] = 0.0
        _workHull[i][_inst + 3] = _workHull[i][_inst + 4]
        _workHull[i][_inst + 7] = 0.0
        _workHull[i][_inst + 6] = _workHull[i][_inst + 7]
        _workHull[i][_inst + 10] = 0.0
        _workHull[i][_inst + 9] = _workHull[i][_inst + 10]
        k = 0
        w1 = _int(_workHull[1][_inst])
        w2 = _int(_workHull[2][_inst])
        while w2 > 0 and i >= k:
            if w1 > 0:
                _workHull[i][_inst + 3] += _workHull[i - k][_inst + 1] * w1
                _workHull[i][_inst + 6] += _workHull[i - k][_inst + 1]
                _workHull[i][_inst + 9] += w1
            _workHull[i][_inst + 4] += _workHull[i - k][_inst + 1] * w2
            _workHull[i][_inst + 7] += _workHull[i - k][_inst + 1]
            _workHull[i][_inst + 10] += w2
            k += 1
            w1 -= 1
            w2 -= 1
    _workHull[i][_inst + 2] = _fdiv(2.0 * _workHull[i][_inst + 3], _workHull[i][_inst + 9]) - _fdiv(_workHull[i][_inst + 4], _workHull[i][_inst + 10])
    if i > _workHull[3][_inst]:
        _workHull[i][_inst + 11] = _workHull[i - 1][_inst + 11]
        _workHull[i][_inst + 5] = _workHull[i - 1][_inst + 5] + (_workHull[i][_inst + 2] * _workHull[3][_inst]) - _workHull[i - 1][_inst + 8]
        _workHull[i][_inst + 8] = _workHull[i - 1][_inst + 8] + _workHull[i][_inst + 2] - _workHull[i - _int(_workHull[3][_inst])][_inst + 2]
    else:
        _workHull[i][_inst + 5] = 0.0
        _workHull[i][_inst + 8] = 0.0
        _workHull[i][_inst + 11] = 0.0
        k = 0
        w3 = _int(_workHull[3][_inst])
        while w3 > 0 and i >= k:
            _workHull[i][_inst + 5] += _workHull[i - k][_inst + 2] * w3
            _workHull[i][_inst + 8] += _workHull[i - k][_inst + 2]
            _workHull[i][_inst + 11] += w3
            k += 1
            w3 -= 1
    return _fdiv(_workHull[i][_inst + 5], _workHull[i][_inst + 11])

# ---- static local variables
_s_iHull__arrayError = False
_s_iHull__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HullLevels(_MQL5Indicator):
    name = 'Hull levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 20,  # Period
        'inpDivisor': 2.0,  # Divisor ("speed")
        'inpPeriodl': 3.0,  # Levels period (<=1 for same as Hull period)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDisplay': _Choice({0: 'Display the filled zones', 1: "Don't display the filled zones"}, default=0),  # Filled zones display :
    }

