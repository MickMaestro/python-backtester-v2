"""Vidya — converted from MQL5: MQL5 Indicators/Vidya/Vidya.mq5

Vidya
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [8421504], 2: [11119017, 9639167, 3329330]}, 'widths': {1: 6, 2: 2}, 'styles': {}, 'labels': {1: 'Shadow', 2: 'Vidya'}, 'levels': [], 'description': ['Vidya'], 'name': 'Vidya', 'source': 'MQL5 Indicators/Vidya/Vidya.mq5', 'folder': 'Vidya', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 12, 'label': 'Vidya period', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 0, 'label': 'Momentum period (<=1 for same as Vidya period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 12)  # Vidya period
inpPeriod2 = _input('inpPeriod2', 0)  # Momentum period (<=1 for same as Vidya period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
cmo1 = Arr(0, 0.0)
cmo2 = Arr(0, 0.0)
cmo3 = Arr(0, 0.0)
cmo4 = Arr(0, 0.0)
_alpha = 0.0
_adpPeriod = 0

def OnInit():
    global _adpPeriod, _alpha
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, cmo1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, cmo2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, cmo3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, cmo4, INDICATOR_CALCULATIONS)
    _alpha = _fdiv(2.0, 1.0 + inpPeriod)
    _adpPeriod = (inpPeriod if (inpPeriod2 <= 1) else inpPeriod2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Vidya (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i)
        _cmo = iCmo(_adpPeriod, close, cmo1, cmo2, cmo3, cmo4, i)
        if _cmo < 0:
            _cmo = -_cmo
        val[i] = ((val[i - 1] + (_alpha * _cmo * (_price - val[i - 1]))) if (i > 0) else _price)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        vals[i] = val[i]
        i += 1
    return i

def iCmo(period, price, diffu, diffd, cumu, cumd, i):
    diff = ((price[i] - price[i - 1]) if (i > 0) else 0)
    if diff > 0:
        diffu[i] = diff
        diffd[i] = 0.0
    else:
        diffd[i] = -diff
        diffu[i] = 0.0
    if i < period:
        cumd[i] = 0.0
        cumu[i] = cumd[i]
        k = 0
        while k < period and (i - k) >= 0:
            cumu[i] += diffu[i - k]
            cumd[i] += diffd[i - k]
            k += 1
    else:
        cumu[i] = cumu[i - 1] - diffu[i - period] + diffu[i]
        cumd[i] = cumd[i - 1] - diffd[i - period] + diffd[i]
    return (_fdiv(cumu[i] - cumd[i], cumu[i] + cumd[i]) if ((cumu[i] + cumd[i]) != 0) else 0)

def getPrice(tprice, open, close, high, low, i):
    if i >= 0:
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vidya(_MQL5Indicator):
    name = 'Vidya'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 12,  # Vidya period
        'inpPeriod2': 0,  # Momentum period (<=1 for same as Vidya period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

