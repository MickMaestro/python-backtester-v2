"""Parabolic weighted MA velocity — converted from MQL5: MQL5 Indicators/Parabolic Weighted Velocity/Parabolic weighted MA velocity.mq5

Parabolic weighted MA velocity
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Parabolic weighted MA velocity'}, 'levels': [], 'description': ['Parabolic weighted MA velocity'], 'name': 'Parabolic weighted MA velocity', 'source': 'MQL5 Indicators/Parabolic Weighted Velocity/Parabolic weighted MA velocity.mq5', 'folder': 'Parabolic Weighted Velocity', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 27, 'label': 'Period', 'sinput': False}, {'mql': 'inpPower', 'py': 'inpPower', 'param': 'inpPower', 'type': 'double', 'default': 1.0, 'label': 'Power', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 27)  # Period
inpPower = _input('inpPower', 1.0)  # Power
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
_velWork = Arr(0, 0.0, dims=(1,))

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Parabolic weighted MA velocity (' + _str(inpPeriod) + ',' + _str(inpPower) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        val[i] = iVelocity(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, inpPower, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iVelocity(price, period, power, i, bars, instanceNo=0):
    if ArrayRange(_velWork, 0) != bars:
        ArrayResize(_velWork, bars)
    _velWork[i][instanceNo] = price
    suma = 0.0
    sumwa = 0.0
    sumb = 0.0
    sumwb = 0.0
    k = 0
    while k < period and (i - k) >= 0:
        weight = MathPow(period - k, power)
        suma += _velWork[i - k][instanceNo] * weight
        sumb += _velWork[i - k][instanceNo] * weight * weight
        sumwa += weight
        sumwb += weight * weight
        k += 1
    return _fdiv(sumb, sumwb) - _fdiv(suma, sumwa)

def getPrice(tprice, open, close, high, low, i, _bars):
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


class ParabolicWeightedMAVelocity(_MQL5Indicator):
    name = 'Parabolic weighted MA velocity'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 27,  # Period
        'inpPower': 1.0,  # Power
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

