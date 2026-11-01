"""Hull ribbon — converted from MQL5: MQL5 Indicators/Hull ribbon/Hull ribbon.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [15466475, 15461375], 2: [11119017, 7451452, 17919], 3: [11119017, 7451452, 17919]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Ribbon', 2: 'Hull fast', 3: 'Hull slow'}, 'levels': [], 'description': [], 'name': 'Hull ribbon', 'source': 'MQL5 Indicators/Hull ribbon/Hull ribbon.mq5', 'folder': 'Hull ribbon', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpDivisorf', 'py': 'inpDivisorf', 'param': 'inpDivisorf', 'type': 'double', 'default': 2.2, 'label': 'Fast "speed"', 'sinput': False}, {'mql': 'inpDivisors', 'py': 'inpDivisors', 'param': 'inpDivisors', 'type': 'double', 'default': 1.8, 'label': 'Slow "speed"', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpDivisorf = _input('inpDivisorf', 2.2)  # Fast "speed"
inpDivisors = _input('inpDivisors', 1.8)  # Slow "speed"
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
valf = Arr(0, 0.0)
valfc = Arr(0, 0.0)
vals = Arr(0, 0.0)
valsc = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)

class CHull(MqlObject):
    _q_fields = ('m_fullPeriod', 'm_halfPeriod', 'm_sqrtPeriod', 'm_arraySize', 'm_weight1', 'm_weight2', 'm_weight3', 'm_array')
    def __init__(self):
        self.m_fullPeriod = 0
        self.m_halfPeriod = 0
        self.m_sqrtPeriod = 0
        self.m_arraySize = 0
        self.m_weight1 = 0.0
        self.m_weight2 = 0.0
        self.m_weight3 = 0.0
        self.m_array = Arr(0, 0, factory=sHullArrayStruct)
        self.init(1, 2.0)
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period, divisor):
        self.m_fullPeriod = (period if (period > 1) else 1)
        self.m_halfPeriod = _int((_fdiv(self.m_fullPeriod, (divisor if (divisor > 1) else 1)) if (self.m_fullPeriod > 1) else 1))
        self.m_sqrtPeriod = _int(MathSqrt(self.m_fullPeriod))
        self.m_arraySize = -1
        self.m_weight3 = 1.0
        self.m_weight2 = self.m_weight3
        self.m_weight1 = self.m_weight2
        return True
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].value = value
        if i > self.m_fullPeriod:
            self.m_array[i].wsum1 = self.m_array[i - 1].wsum1 + (value * self.m_halfPeriod) - self.m_array[i - 1].lsum1
            self.m_array[i].lsum1 = self.m_array[i - 1].lsum1 + value - self.m_array[i - self.m_halfPeriod].value
            self.m_array[i].wsum2 = self.m_array[i - 1].wsum2 + (value * self.m_fullPeriod) - self.m_array[i - 1].lsum2
            self.m_array[i].lsum2 = self.m_array[i - 1].lsum2 + value - self.m_array[i - self.m_fullPeriod].value
        else:
            self.m_weight2 = 0.0
            self.m_weight1 = self.m_weight2
            self.m_array[i].lsum2 = self.m_weight1
            self.m_array[i].lsum1 = self.m_array[i].lsum2
            self.m_array[i].wsum2 = self.m_array[i].lsum1
            self.m_array[i].wsum1 = self.m_array[i].wsum2
            k = 0
            w1 = self.m_halfPeriod
            w2 = self.m_fullPeriod
            while w2 > 0 and i >= k:
                if w1 > 0:
                    self.m_array[i].wsum1 += self.m_array[i - k].value * w1
                    self.m_array[i].lsum1 += self.m_array[i - k].value
                    self.m_weight1 += w1
                self.m_array[i].wsum2 += self.m_array[i - k].value * w2
                self.m_array[i].lsum2 += self.m_array[i - k].value
                self.m_weight2 += w2
                k += 1
                w1 -= 1
                w2 -= 1
        self.m_array[i].value3 = _fdiv(2.0 * self.m_array[i].wsum1, self.m_weight1) - _fdiv(self.m_array[i].wsum2, self.m_weight2)
        if i > self.m_sqrtPeriod:
            self.m_array[i].wsum3 = self.m_array[i - 1].wsum3 + (self.m_array[i].value3 * self.m_sqrtPeriod) - self.m_array[i - 1].lsum3
            self.m_array[i].lsum3 = self.m_array[i - 1].lsum3 + self.m_array[i].value3 - self.m_array[i - self.m_sqrtPeriod].value3
        else:
            self.m_weight3 = 0.0
            self.m_array[i].lsum3 = self.m_weight3
            self.m_array[i].wsum3 = self.m_array[i].lsum3
            k = 0
            w = self.m_sqrtPeriod
            while w > 0 and i >= k:
                self.m_array[i].wsum3 += self.m_array[i - k].value3 * w
                self.m_array[i].lsum3 += self.m_array[i - k].value3
                self.m_weight3 += w
                k += 1
                w -= 1
        return _fdiv(self.m_array[i].wsum3, self.m_weight3)

class sHullArrayStruct(MqlObject):
    _q_fields = ('value', 'value3', 'wsum1', 'wsum2', 'wsum3', 'lsum1', 'lsum2', 'lsum3')
    def __init__(self, *args):
        self.value = 0.0
        self.value3 = 0.0
        self.wsum1 = 0.0
        self.wsum2 = 0.0
        self.wsum3 = 0.0
        self.lsum1 = 0.0
        self.lsum2 = 0.0
        self.lsum3 = 0.0

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valf, INDICATOR_DATA)
    SetIndexBuffer(3, valfc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, vals, INDICATOR_DATA)
    SetIndexBuffer(5, valsc, INDICATOR_COLOR_INDEX)
    iHull[0].init(inpPeriod, MathMax(inpDivisorf, inpDivisors))
    iHull[1].init(inpPeriod, MathMin(inpDivisorf, inpDivisors))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hull ribbon (' + _str(inpPeriod) + ',' + _str(inpDivisorf) + ',' + _str(inpDivisors) + ')')
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
        fillu[i] = iHull[0].calculate(_price, i, rates_total)
        valf[i] = fillu[i]
        filld[i] = iHull[1].calculate(_price, i, rates_total)
        vals[i] = filld[i]
        valsc[i] = (1 if (valf[i] > vals[i]) else 2 if (valf[i] < vals[i]) else valfc[i - 1] if (i > 0) else 0)
        valfc[i] = valsc[i]
        i += 1
    return i

# ---- global variables initialised from expressions
iHull = Arr(2, 0, dyn=False, factory=CHull)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HullRibbon(_MQL5Indicator):
    name = 'Hull ribbon'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpDivisorf': 2.2,  # Fast "speed"
        'inpDivisors': 1.8,  # Slow "speed"
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

