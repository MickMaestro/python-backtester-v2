"""CCI (Hull) — converted from MQL5: MQL5 Indicators/CCI - Hull pre-filtered/CCI (Hull).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'CCI'}, 'levels': [], 'description': [], 'name': 'CCI (Hull)', 'source': 'MQL5 Indicators/CCI - Hull pre-filtered/CCI (Hull).mq5', 'folder': 'CCI - Hull pre-filtered', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpHullPeriod', 'py': 'inpHullPeriod', 'param': 'inpHullPeriod', 'type': 'int', 'default': 14, 'label': 'Hull period', 'sinput': False}, {'mql': 'inpHullDivisor', 'py': 'inpHullDivisor', 'param': 'inpHullDivisor', 'type': 'double', 'default': 2.0, 'label': 'Hull divisor', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # CCI period
inpHullPeriod = _input('inpHullPeriod', 14)  # Hull period
inpHullDivisor = _input('inpHullDivisor', 2.0)  # Hull divisor
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)

class CCci(MqlObject):
    _q_fields = ('m_work', 'm_period', 'm_period2', 'm_arraySize')
    def __init__(self):
        self.m_work = Arr(0, 0, factory=sCciWork)
        self.m_period = 0
        self.m_period2 = 0.0
        self.m_arraySize = 0
        self.m_arraySize = -1
        self.m_period = 1
    def _q_dtor(self):
        self.m_arraySize = -1
        ArrayFree(self.m_work)
    def init(self, period):
        self.m_period = period
        return
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_work, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_work[i].value = value
        self.m_work[i].value2 = value * value
        if i > self.m_period:
            self.m_work[i].summ = self.m_work[i - 1].summ + self.m_work[i].value - self.m_work[i - self.m_period].value
            self.m_work[i].summ2 = self.m_work[i - 1].summ2 + self.m_work[i].value2 - self.m_work[i - self.m_period].value2
        else:
            self.m_work[i].summ = self.m_work[i].value
            self.m_work[i].summ2 = self.m_work[i].value2
            k = 1
            while k < self.m_period and i >= k:
                self.m_work[i].summ += self.m_work[i - k].value
                self.m_work[i].summ2 += self.m_work[i - k].value2
                k += 1
        _avg = _fdiv(self.m_work[i].summ, float(self.m_period))
        _dev = MathSqrt(_fdiv(self.m_work[i].summ2 - (self.m_work[i].summ * _avg), float(self.m_period)))
        return (_fdiv(value - _avg, 0.015 * _dev) if (_dev != 0) else 0)

class sCciWork(MqlObject):
    _q_fields = ('value', 'value2', 'summ', 'summ2')
    def __init__(self, *args):
        self.value = 0.0
        self.value2 = 0.0
        self.summ = 0.0
        self.summ2 = 0.0

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
        self.m_array[i].price = value
        if i > self.m_fullPeriod:
            self.m_array[i].wsum1 = self.m_array[i - 1].wsum1 + (value * self.m_halfPeriod) - self.m_array[i - 1].lsum1
            self.m_array[i].lsum1 = self.m_array[i - 1].lsum1 + value - self.m_array[i - self.m_halfPeriod].price
            self.m_array[i].wsum2 = self.m_array[i - 1].wsum2 + (value * self.m_fullPeriod) - self.m_array[i - 1].lsum2
            self.m_array[i].lsum2 = self.m_array[i - 1].lsum2 + value - self.m_array[i - self.m_fullPeriod].price
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
                    self.m_array[i].wsum1 += self.m_array[i - k].price * w1
                    self.m_array[i].lsum1 += self.m_array[i - k].price
                    self.m_weight1 += w1
                self.m_array[i].wsum2 += self.m_array[i - k].price * w2
                self.m_array[i].lsum2 += self.m_array[i - k].price
                self.m_weight2 += w2
                k += 1
                w1 -= 1
                w2 -= 1
        self.m_array[i].price3 = _fdiv(2.0 * self.m_array[i].wsum1, self.m_weight1) - _fdiv(self.m_array[i].wsum2, self.m_weight2)
        if i > self.m_sqrtPeriod:
            self.m_array[i].wsum3 = self.m_array[i - 1].wsum3 + (self.m_array[i].price3 * self.m_sqrtPeriod) - self.m_array[i - 1].lsum3
            self.m_array[i].lsum3 = self.m_array[i - 1].lsum3 + self.m_array[i].price3 - self.m_array[i - self.m_sqrtPeriod].price3
        else:
            self.m_weight3 = 0.0
            self.m_array[i].lsum3 = self.m_weight3
            self.m_array[i].wsum3 = self.m_array[i].lsum3
            k = 0
            w3 = self.m_sqrtPeriod
            while w3 > 0 and i >= k:
                self.m_array[i].wsum3 += self.m_array[i - k].price3 * w3
                self.m_array[i].lsum3 += self.m_array[i - k].price3
                self.m_weight3 += w3
                k += 1
                w3 -= 1
        return _fdiv(self.m_array[i].wsum3, self.m_weight3)

class sHullArrayStruct(MqlObject):
    _q_fields = ('price', 'price3', 'wsum1', 'wsum2', 'wsum3', 'lsum1', 'lsum2', 'lsum3')
    def __init__(self, *args):
        self.price = 0.0
        self.price3 = 0.0
        self.wsum1 = 0.0
        self.wsum2 = 0.0
        self.wsum3 = 0.0
        self.lsum1 = 0.0
        self.lsum2 = 0.0
        self.lsum3 = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    _workCci.init(inpPeriod)
    iHull.init(inpHullPeriod, inpHullDivisor)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI std based (' + _str(inpPeriod) + ')(Hull ' + _str(inpHullPeriod) + ' smoothed)')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            prices[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prices[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prices[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prices[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prices[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prices[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prices[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prices[i] = 0.0
        val[i] = _workCci.calculate(iHull.calculate(prices[i], i, rates_total), i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return rates_total

# ---- global variables initialised from expressions
_workCci = _alloc(CCci)
_workCci.__init__()
iHull = _alloc(CHull)
iHull.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIHull(_MQL5Indicator):
    name = 'CCI (Hull)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # CCI period
        'inpHullPeriod': 14,  # Hull period
        'inpHullDivisor': 2.0,  # Hull divisor
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
    }

