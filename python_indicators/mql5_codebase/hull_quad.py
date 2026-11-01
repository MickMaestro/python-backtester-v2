"""Hull quad — converted from MQL5: MQL5 Indicators/Hull quad/Hull quad.mq5

Hull quad
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 5, 6: 5}, 'colors': {1: [12632256], 2: [12632256], 3: [12632256], 4: [12632256], 5: [16748574], 6: [17919]}, 'widths': {5: 1, 6: 1}, 'styles': {1: 2, 2: 2, 3: 2, 4: 2}, 'labels': {1: 'Hull 1', 2: 'Hull 2', 3: 'Hull 3', 4: 'Hull 4', 5: 'Arrow up', 6: 'Arrow down'}, 'levels': [], 'description': ['Hull quad'], 'name': 'Hull quad', 'source': 'MQL5 Indicators/Hull quad/Hull quad.mq5', 'folder': 'Hull quad', 'inputs': [{'mql': 'inpPeriod1', 'py': 'inpPeriod1', 'param': 'inpPeriod1', 'type': 'int', 'default': 8, 'label': 'Period 1', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 55, 'label': 'Period 2', 'sinput': False}, {'mql': 'inpPeriod3', 'py': 'inpPeriod3', 'param': 'inpPeriod3', 'type': 'int', 'default': 144, 'label': 'Period 3', 'sinput': False}, {'mql': 'inpPeriod4', 'py': 'inpPeriod4', 'param': 'inpPeriod4', 'type': 'int', 'default': 377, 'label': 'Period 4', 'sinput': False}, {'mql': 'inpDivisor', 'py': 'inpDivisor', 'param': 'inpDivisor', 'type': 'double', 'default': 2.0, 'label': 'Divisor ("speed")', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod1 = _input('inpPeriod1', 8)  # Period 1
inpPeriod2 = _input('inpPeriod2', 55)  # Period 2
inpPeriod3 = _input('inpPeriod3', 144)  # Period 3
inpPeriod4 = _input('inpPeriod4', 377)  # Period 4
inpDivisor = _input('inpDivisor', 2.0)  # Divisor ("speed")
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
hull1 = Arr(0, 0.0)
hull2 = Arr(0, 0.0)
hull3 = Arr(0, 0.0)
hull4 = Arr(0, 0.0)
arrowup = Arr(0, 0.0)
arrowdn = Arr(0, 0.0)
trend = Arr(0, 0.0)

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
    SetIndexBuffer(0, hull1, INDICATOR_DATA)
    SetIndexBuffer(1, hull2, INDICATOR_DATA)
    SetIndexBuffer(2, hull3, INDICATOR_DATA)
    SetIndexBuffer(3, hull4, INDICATOR_DATA)
    SetIndexBuffer(4, arrowup, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_ARROW, 241)
    PlotIndexSetInteger(4, PLOT_ARROW_SHIFT, 10)
    SetIndexBuffer(5, arrowdn, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_ARROW, 242)
    PlotIndexSetInteger(5, PLOT_ARROW_SHIFT, -10)
    SetIndexBuffer(6, trend, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hull quad (' + _str(inpPeriod1) + ',' + _str(inpPeriod2) + ',' + _str(inpPeriod3) + ',' + _str(inpPeriod4) + ',' + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
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
        hull1[i] = iHull(_price, inpPeriod1, inpDivisor, i, rates_total, 0)
        hull2[i] = iHull(_price, inpPeriod2, inpDivisor, i, rates_total, 1)
        hull3[i] = iHull(_price, inpPeriod3, inpDivisor, i, rates_total, 2)
        hull4[i] = iHull(_price, inpPeriod4, inpDivisor, i, rates_total, 3)
        arrowup[i] = EMPTY_VALUE
        arrowdn[i] = EMPTY_VALUE
        trend[i] = 0.0
        if i > 1:
            if (((hull1[i] > hull4[i] and hull2[i] > hull4[i]) and hull1[i] > hull1[i - 1]) and hull1[i] > hull1[i - 2]) and hull3[i] > hull3[i - 1]:
                trend[i] = 1.0
            if (((hull1[i] < hull4[i] and hull2[i] < hull4[i]) and hull1[i] < hull1[i - 1]) and hull1[i] < hull1[i - 2]) and hull3[i] < hull3[i - 1]:
                trend[i] = -1.0
            if trend[i] != 0 and trend[i] != trend[i - 1]:
                if trend[i] == 1:
                    arrowup[i] = low[i]
                else:
                    arrowdn[i] = high[i]
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
_s_iHull_m_coeff = Arr(4, 0, dyn=False, factory=sHullCoeffStruct)
_s_iHull_m_array = Arr(0, 0, factory=sHullArrayStruct, dims=(4,))
_s_iHull_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HullQuad(_MQL5Indicator):
    name = 'Hull quad'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod1': 8,  # Period 1
        'inpPeriod2': 55,  # Period 2
        'inpPeriod3': 144,  # Period 3
        'inpPeriod4': 377,  # Period 4
        'inpDivisor': 2.0,  # Divisor ("speed")
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

