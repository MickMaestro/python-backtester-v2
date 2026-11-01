"""Schaff trend cycle - Hull — converted from MQL5: MQL5 Indicators/Schaff trend cycle - Hull/Schaff trend cycle - Hull.mq5

Schaff trend cycle - of Hull
Copyright: Copyright 2017, mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Schaff trend cycle'}, 'levels': [], 'description': ['Schaff trend cycle - of Hull'], 'name': 'Schaff trend cycle - Hull', 'source': 'MQL5 Indicators/Schaff trend cycle - Hull/Schaff trend cycle - Hull.mq5', 'folder': 'Schaff trend cycle - Hull', 'inputs': [{'mql': 'inpSchaffPeriod', 'py': 'inpSchaffPeriod', 'param': 'inpSchaffPeriod', 'type': 'int', 'default': 32, 'label': 'Schaff period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 23, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 50, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'double', 'default': 1.0, 'label': 'Smoothing period (<=1 for no smoothing)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpSchaffPeriod = _input('inpSchaffPeriod', 32)  # Schaff period
inpFastPeriod = _input('inpFastPeriod', 23)  # Fast period
inpSlowPeriod = _input('inpSlowPeriod', 50)  # Slow period
inpSmoothPeriod = _input('inpSmoothPeriod', 1.0)  # Smoothing period (<=1 for no smoothing)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
macd = Arr(0, 0.0)
fastk1 = Arr(0, 0.0)
fastd1 = Arr(0, 0.0)
fastk2 = Arr(0, 0.0)
_alpha = 0.0

class sHullCoeffStruct(MqlObject):
    _q_fields = ('OriginalPeriod', 'OriginalDivisor', 'FullPeriod', 'HalfPeriod', 'SqrtPeriod')
    def __init__(self, *args):
        self.OriginalPeriod = 0
        self.OriginalDivisor = 0.0
        self.FullPeriod = 0
        self.HalfPeriod = 0
        self.SqrtPeriod = 0

class sHullArrayStruct(MqlObject):
    _q_fields = ('price', 'price3', 'wsum1', 'wsum2', 'wsum3', 'lsum1', 'lsum2', 'lsum3', 'weight1', 'weight2', 'weight3')
    def __init__(self, *args):
        self.price = 0.0
        self.price3 = 0.0
        self.wsum1 = 0.0
        self.wsum2 = 0.0
        self.wsum3 = 0.0
        self.lsum1 = 0.0
        self.lsum2 = 0.0
        self.lsum3 = 0.0
        self.weight1 = 0.0
        self.weight2 = 0.0
        self.weight3 = 0.0

def OnInit():
    global _alpha
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, macd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, fastk1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, fastk2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, fastd1, INDICATOR_CALCULATIONS)
    _alpha = _fdiv(2.0, 1.0 + (inpSmoothPeriod if (inpSmoothPeriod > 1) else 1))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Schaff trend cycle Hull (' + _str(inpSchaffPeriod) + ',' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSmoothPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            price = close[i]
        elif _sw1 == PRICE_OPEN:
            price = open[i]
        elif _sw1 == PRICE_HIGH:
            price = high[i]
        elif _sw1 == PRICE_LOW:
            price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            price = 0.0
        macd[i] = iHull(price, inpFastPeriod, 2.0, i, rates_total, 0) - iHull(price, inpSlowPeriod, 2.0, i, rates_total, 1)
        start = i - inpSchaffPeriod + 1
        if start < 0:
            start = 0
        lowMacd = macd[ArrayMinimum(macd, start, inpSchaffPeriod)]
        highMacd = macd[ArrayMaximum(macd, start, inpSchaffPeriod)] - lowMacd
        fastk1[i] = ((100.0 * _fdiv(macd[i] - lowMacd, highMacd)) if (highMacd > 0) else fastk1[i - 1] if (i > 0) else 0)
        fastd1[i] = ((fastd1[i - 1] + (_alpha * (fastk1[i] - fastd1[i - 1]))) if (i > 0) else fastk1[i])
        lowStoch = fastd1[ArrayMinimum(fastd1, start, inpSchaffPeriod)]
        highStoch = fastd1[ArrayMaximum(fastd1, start, inpSchaffPeriod)] - lowStoch
        fastk2[i] = ((100 * _fdiv(fastd1[i] - lowStoch, highStoch)) if (highStoch > 0) else fastk2[i - 1] if (i > 0) else 0)
        val[i] = ((val[i - 1] + (_alpha * (fastk2[i] - val[i - 1]))) if (i > 0) else fastk2[i])
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iHull(price, period, divisor, i, bars, instance=0):
    global _s_iHull_m_arraySize
    if _s_iHull_m_arraySize <= bars:
        _res = ArrayResize(_s_iHull_m_array, bars + 500)
        if _res <= bars:
            return 0.0
        _s_iHull_m_arraySize = _res
    if _s_iHull_m_coeff[instance].OriginalPeriod != period or _s_iHull_m_coeff[instance].OriginalDivisor != divisor:
        _s_iHull_m_coeff[instance].OriginalPeriod = period
        _s_iHull_m_coeff[instance].OriginalDivisor = divisor
        _s_iHull_m_coeff[instance].FullPeriod = (period if (period > 1) else 1)
        _s_iHull_m_coeff[instance].HalfPeriod = _int((_fdiv(_s_iHull_m_coeff[instance].FullPeriod, (divisor if (divisor > 1) else 1)) if (_s_iHull_m_coeff[instance].FullPeriod > 1) else 1))
        _s_iHull_m_coeff[instance].SqrtPeriod = _int(MathSqrt(_s_iHull_m_coeff[instance].FullPeriod))
    _s_iHull_m_array[i][instance].price = price
    if i > _s_iHull_m_coeff[instance].FullPeriod:
        _s_iHull_m_array[i][instance].weight1 = _s_iHull_m_array[i - 1][instance].weight1
        _s_iHull_m_array[i][instance].wsum1 = _s_iHull_m_array[i - 1][instance].wsum1 + (price * _s_iHull_m_coeff[instance].HalfPeriod) - _s_iHull_m_array[i - 1][instance].lsum1
        _s_iHull_m_array[i][instance].lsum1 = _s_iHull_m_array[i - 1][instance].lsum1 + price - _s_iHull_m_array[i - _s_iHull_m_coeff[instance].HalfPeriod][instance].price
        _s_iHull_m_array[i][instance].weight2 = _s_iHull_m_array[i - 1][instance].weight2
        _s_iHull_m_array[i][instance].wsum2 = _s_iHull_m_array[i - 1][instance].wsum2 + (price * _s_iHull_m_coeff[instance].FullPeriod) - _s_iHull_m_array[i - 1][instance].lsum2
        _s_iHull_m_array[i][instance].lsum2 = _s_iHull_m_array[i - 1][instance].lsum2 + price - _s_iHull_m_array[i - _s_iHull_m_coeff[instance].FullPeriod][instance].price
    else:
        _s_iHull_m_array[i][instance].weight2 = 0.0
        _s_iHull_m_array[i][instance].weight1 = _s_iHull_m_array[i][instance].weight2
        _s_iHull_m_array[i][instance].lsum2 = _s_iHull_m_array[i][instance].weight1
        _s_iHull_m_array[i][instance].lsum1 = _s_iHull_m_array[i][instance].lsum2
        _s_iHull_m_array[i][instance].wsum2 = _s_iHull_m_array[i][instance].lsum1
        _s_iHull_m_array[i][instance].wsum1 = _s_iHull_m_array[i][instance].wsum2
        k = 0
        w1 = _s_iHull_m_coeff[instance].HalfPeriod
        w2 = _s_iHull_m_coeff[instance].FullPeriod
        while w2 > 0 and i >= k:
            if w1 > 0:
                _s_iHull_m_array[i][instance].wsum1 += _s_iHull_m_array[i - k][instance].price * w1
                _s_iHull_m_array[i][instance].lsum1 += _s_iHull_m_array[i - k][instance].price
                _s_iHull_m_array[i][instance].weight1 += w1
            _s_iHull_m_array[i][instance].wsum2 += _s_iHull_m_array[i - k][instance].price * w2
            _s_iHull_m_array[i][instance].lsum2 += _s_iHull_m_array[i - k][instance].price
            _s_iHull_m_array[i][instance].weight2 += w2
            k += 1
            w1 -= 1
            w2 -= 1
    _s_iHull_m_array[i][instance].price3 = _fdiv(2.0 * _s_iHull_m_array[i][instance].wsum1, _s_iHull_m_array[i][instance].weight1) - _fdiv(_s_iHull_m_array[i][instance].wsum2, _s_iHull_m_array[i][instance].weight2)
    if i > _s_iHull_m_coeff[instance].SqrtPeriod:
        _s_iHull_m_array[i][instance].weight3 = _s_iHull_m_array[i - 1][instance].weight3
        _s_iHull_m_array[i][instance].wsum3 = _s_iHull_m_array[i - 1][instance].wsum3 + (_s_iHull_m_array[i][instance].price3 * _s_iHull_m_coeff[instance].SqrtPeriod) - _s_iHull_m_array[i - 1][instance].lsum3
        _s_iHull_m_array[i][instance].lsum3 = _s_iHull_m_array[i - 1][instance].lsum3 + _s_iHull_m_array[i][instance].price3 - _s_iHull_m_array[i - _s_iHull_m_coeff[instance].SqrtPeriod][instance].price3
    else:
        _s_iHull_m_array[i][instance].weight3 = 0.0
        _s_iHull_m_array[i][instance].lsum3 = _s_iHull_m_array[i][instance].weight3
        _s_iHull_m_array[i][instance].wsum3 = _s_iHull_m_array[i][instance].lsum3
        k = 0
        w3 = _s_iHull_m_coeff[instance].SqrtPeriod
        while w3 > 0 and i >= k:
            _s_iHull_m_array[i][instance].wsum3 += _s_iHull_m_array[i - k][instance].price3 * w3
            _s_iHull_m_array[i][instance].lsum3 += _s_iHull_m_array[i - k][instance].price3
            _s_iHull_m_array[i][instance].weight3 += w3
            k += 1
            w3 -= 1
    return _fdiv(_s_iHull_m_array[i][instance].wsum3, _s_iHull_m_array[i][instance].weight3)

# ---- static local variables
_s_iHull_m_coeff = Arr(2, 0, dyn=False, factory=sHullCoeffStruct)
_s_iHull_m_array = Arr(0, 0, factory=sHullArrayStruct, dims=(2,))
_s_iHull_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SchaffTrendCycleHull(_MQL5Indicator):
    name = 'Schaff trend cycle - Hull'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpSchaffPeriod': 32,  # Schaff period
        'inpFastPeriod': 23,  # Fast period
        'inpSlowPeriod': 50,  # Slow period
        'inpSmoothPeriod': 1.0,  # Smoothing period (<=1 for no smoothing)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

