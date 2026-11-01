"""Adaptive ATR channel — converted from MQL5: MQL5 Indicators/Adaptive ATR channel/Adaptive ATR channel.mq5

Adaptive ATR channel
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 8, 2: 1, 3: 1}, 'colors': {1: [12632256, 7451452, 36095], 2: [8421504], 3: [8421504]}, 'widths': {1: 2}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'Average', 2: 'Upper band', 3: 'Lower band'}, 'levels': [], 'description': ['Adaptive ATR channel'], 'name': 'Adaptive ATR channel', 'source': 'MQL5 Indicators/Adaptive ATR channel/Adaptive ATR channel.mq5', 'folder': 'Adaptive ATR channel', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpMultiplier', 'py': 'inpMultiplier', 'param': 'inpMultiplier', 'type': 'double', 'default': 1.0, 'label': 'ATR multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpMultiplier = _input('inpMultiplier', 1.0)  # ATR multiplier
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
tr = Arr(0, 0.0)
atr = Arr(0, 0.0)
ª_minPeriod = 0.0
ª_maxPeriod = 0.0

def OnInit():
    global ª_maxPeriod, ª_minPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valu, INDICATOR_DATA)
    SetIndexBuffer(3, vald, INDICATOR_DATA)
    SetIndexBuffer(4, tr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, atr, INDICATOR_CALCULATIONS)
    ª_minPeriod = inpPeriod / 2.0
    if ª_minPeriod < 1:
        ª_minPeriod = 1.0
    ª_maxPeriod = ª_minPeriod * 2.0
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptive ATR channel (' + _str(inpPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        tr[i] = (((high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
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
        _averagePeriod = (iEr(_price, inpPeriod, i, rates_total) * (ª_maxPeriod - ª_minPeriod)) + ª_minPeriod
        _alpha = _fdiv(2.0, 1.0 + _averagePeriod)
        _atr = tr[i]
        k = 1
        while k < _averagePeriod and i >= k:
            _atr += tr[i - k]
            k += 1
        _atr = _fdiv(_atr, float(k))
        atr[i] = ((atr[i - 1] + (_alpha * (_atr - atr[i - 1]))) if (i > 0) else _atr)
        val[i] = ((val[i - 1] + (_alpha * (_price - val[i - 1]))) if (i > 0) else _price)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        valu[i] = val[i] + (inpMultiplier * atr[i])
        vald[i] = val[i] - (inpMultiplier * atr[i])
        i += 1
    return i

def iEr(value, period, i, bars, _instance=0):
    global _s_iEr__arrayError, _s_iEr__arrayResizedTo
    if _s_iEr__arrayResizedTo < bars:
        _res = bars + 500
        _res -= ArrayResize(_s_iEr__workArray, _res)
        if _res:
            _s_iEr__arrayError = True
        else:
            _s_iEr__arrayResizedTo = bars + 500
    _s_iEr__workArray[i][_instance] = value
    _s_iEr__workArray[i][_instance + 1] = (((_s_iEr__workArray[i][_instance] - _s_iEr__workArray[i - 1][_instance]) if (_s_iEr__workArray[i][_instance] > _s_iEr__workArray[i - 1][_instance]) else (_s_iEr__workArray[i - 1][_instance] - _s_iEr__workArray[i][_instance])) if (i > 0) else 0)
    if i <= period:
        _s_iEr__workArray[i][_instance + 2] = _s_iEr__workArray[i][_instance + 1]
        k = 1
        while k < period and (i - k) >= 0:
            _s_iEr__workArray[i][_instance + 2] += _s_iEr__workArray[i - k][_instance + 1]
            k += 1
    else:
        _s_iEr__workArray[i][_instance + 2] = _s_iEr__workArray[i - 1][_instance + 2] - _s_iEr__workArray[i - period][_instance + 1] + _s_iEr__workArray[i][_instance + 1]
    _efr = (_fdiv(((_s_iEr__workArray[i][_instance] - _s_iEr__workArray[i - period][_instance]) if (_s_iEr__workArray[i][_instance] > _s_iEr__workArray[i - period][_instance]) else (_s_iEr__workArray[i - period][_instance] - _s_iEr__workArray[i][_instance])), _s_iEr__workArray[i][_instance + 2]) if (_s_iEr__workArray[i][_instance + 2] != 0 and i > period) else 0)
    return _efr

# ---- static local variables
_s_iEr__workArray = Arr(0, 0.0, dims=(3,))
_s_iEr__arrayError = False
_s_iEr__arrayResizedTo = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveATRChannel(_MQL5Indicator):
    name = 'Adaptive ATR channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpMultiplier': 1.0,  # ATR multiplier
    }

