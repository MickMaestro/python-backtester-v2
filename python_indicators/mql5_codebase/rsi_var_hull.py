"""Rsi(var)(Hull) — converted from MQL5: MQL5 Indicators/Rsi (var) - Hull/Rsi(var)(Hull).mq5

Rsi(var) Hull of Hulll average
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_minimum': -5.0, 'indicator_maximum': 105.0}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [50.0], 'description': ['Rsi(var) Hull of Hulll average'], 'name': 'Rsi(var)(Hull)', 'source': 'MQL5 Indicators/Rsi (var) - Hull/Rsi(var)(Hull).mq5', 'folder': 'Rsi (var) - Hull', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'int', 'default': 14, 'label': 'Price smoothing period (<=1 for not smoothing)', 'sinput': False}, {'mql': 'inpDivisor', 'py': 'inpDivisor', 'param': 'inpDivisor', 'type': 'double', 'default': 1.5, 'label': 'Hull divisor', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # RSI period
inpSmooth = _input('inpSmooth', 14)  # Price smoothing period (<=1 for not smoothing)
inpDivisor = _input('inpDivisor', 1.5)  # Hull divisor
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
_ub9__smoothPeriod = 0
_workHull = Arr(0, 0.0, dims=(36,))

def OnInit():
    global _ub9__smoothPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    _ub9__smoothPeriod = (inpSmooth if (inpSmooth > 1) else 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsi(var) Hull (' + _str(inpPeriod) + ',' + _str(_ub9__smoothPeriod) + ',' + _str(inpDivisor) + ')')
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
        prices[i] = iHull(_price, _ub9__smoothPeriod, inpDivisor, i, rates_total, 2)
        _diff = prices[i] - (prices[i - 1] if (i > 0) else prices[i])
        _difa = (_diff if (_diff > 0) else (-_diff))
        _avgBulls = iHull(0.5 * (_difa + _diff), inpPeriod, inpDivisor, i, rates_total, 0)
        _avgBears = iHull(0.5 * (_difa - _diff), inpPeriod, inpDivisor, i, rates_total, 1)
        val[i] = (_fdiv(100.0, 1.0 + _fdiv(_avgBears, _avgBulls)) if (_avgBulls != 0) else 0)
        if val[i] > 100:
            val[i] = 100.0
        if val[i] < 0:
            val[i] = 0.0
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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
    _inst *= 12
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


class RsiVarHull(_MQL5Indicator):
    name = 'Rsi(var)(Hull)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # RSI period
        'inpSmooth': 14,  # Price smoothing period (<=1 for not smoothing)
        'inpDivisor': 1.5,  # Hull divisor
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }
    y_range = (-5.0, 105.0)

