"""Jurik volty — converted from MQL5: MQL5 Indicators/Jurik Volty/Jurik volty.mq5

Jurik volty
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [12632256, 3329330, 42495], 2: [12632256, 3329330, 42495]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Jurik volty', 2: 'Jurik volty signal'}, 'levels': [], 'description': ['Jurik volty'], 'name': 'Jurik volty', 'source': 'MQL5 Indicators/Jurik Volty/Jurik volty.mq5', 'folder': 'Jurik Volty', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Volty period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Volty period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sig = Arr(0, 0.0)
sigc = Arr(0, 0.0)
wrk = Arr(0, 0.0, dims=(5,))

class sVoltyAnswer(MqlObject):
    _q_fields = ('volty', 'voltySignal')
    def __init__(self, *args):
        self.volty = 0.0
        self.voltySignal = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, sig, INDICATOR_DATA)
    SetIndexBuffer(3, sigc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Jurik volty (' + _str(inpPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return -1
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        price = getPrice(inpPrice, open, close, high, low, i, rates_total)
        _answer = iVolty(price, inpPeriod, i, rates_total)
        val[i] = _answer.volty
        sig[i] = _answer.voltySignal
        valc[i] = (1 if (val[i] > sig[i]) else 2 if (val[i] < sig[i]) else 0)
        sigc[i] = valc[i]
        i += 1
    return i

def iVolty(price, length, r, bars):
    if ArrayRange(wrk, 0) != bars:
        ArrayResize(wrk, bars)
    _answer = sVoltyAnswer()
    _answer.volty = 0.0
    _answer.voltySignal = 0.0
    if r == 0:
        for k in range(0, 5):
            wrk[0][k] = 0.0
        return _copy(_answer)
    len1 = MathMax(_fdiv(MathLog(MathSqrt(0.5 * (length - 1))), MathLog(2.0)) + 2.0, 0)
    pow1 = MathMax(len1 - 2.0, 0.5)
    del1 = ((price - wrk[r - 1][0]) if (r > 0) else 0)
    del2 = ((price - wrk[r - 1][1]) if (r > 0) else 0)
    wrk[r][2] = 0.0
    if MathAbs(del1) > MathAbs(del2):
        wrk[r][2] = MathAbs(del1)
    if MathAbs(del1) < MathAbs(del2):
        wrk[r][2] = MathAbs(del2)
    wrk[r][3] = ((wrk[r - 1][3] + (0.1 * (wrk[r][2] - wrk[r - 10][2]))) if (r > 9) else wrk[r][2])
    avg = wrk[r][3]
    k = 1
    while k < 65 and (r - k) >= 0:
        avg += wrk[r - k][3]
        k += 1
    avg = _fdiv(avg, k)
    wrk[r][4] = avg
    dVolty = (_fdiv(wrk[r][2], wrk[r][4]) if (wrk[r][4] > 0) else 0)
    if dVolty > MathPow(len1, _fdiv(1.0, pow1)):
        dVolty = MathPow(len1, _fdiv(1.0, pow1))
    if dVolty < 1:
        dVolty = 1.0
    pow2 = MathPow(dVolty, pow1)
    len2 = MathSqrt(0.5 * (length - 1)) * len1
    Kv = MathPow(_fdiv(len2, len2 + 1), MathSqrt(pow2))
    if del1 > 0:
        wrk[r][0] = price
    else:
        wrk[r][0] = price - (Kv * del1)
    if del2 < 0:
        wrk[r][1] = price
    else:
        wrk[r][1] = price - (Kv * del2)
    _answer.voltySignal = wrk[r][4]
    _answer.volty = wrk[r][3]
    return _copy(_answer)

def getPrice(tprice, open, close, high, low, i, _bars):
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


class JurikVolty(_MQL5Indicator):
    name = 'Jurik volty'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Volty period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

