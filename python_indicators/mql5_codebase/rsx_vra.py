"""Rsx (vra) — converted from MQL5: MQL5 Indicators/RSX volatility ratio adaptive/Rsx (vra).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Rsx'}, 'levels': [], 'description': [], 'name': 'Rsx (vra)', 'source': 'MQL5 Indicators/RSX volatility ratio adaptive/Rsx (vra).mq5', 'folder': 'RSX volatility ratio adaptive', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpSpeed', 'py': 'inpSpeed', 'param': 'inpSpeed', 'type': 'double', 'default': 0.5, 'label': '"Speed" (0.5 for original RSX)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpSpeed = _input('inpSpeed', 0.5)  # "Speed" (0.5 for original RSX)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class cRsx(MqlObject):
    _q_fields = ('speed', 'speedp1', 'kg', 'hg', 'm_array', 'm_arraySize')
    def __init__(self):
        self.speed = 0.0
        self.speedp1 = 0.0
        self.kg = 0.0
        self.hg = 0.0
        self.m_array = Arr(0, 0.0, dims=(13,))
        self.m_arraySize = 0.0
        self.m_arraySize = -1.0
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, _period, _speed):
        self.kg = _fdiv(3.0, 2.0 + (_period if (_period > 1) else 1))
        self.hg = 1.0 - self.kg
        self.speed = ((_speed if (_speed < 1) else 1) if (_speed > 0) else 0)
        self.speedp1 = self.speed + 1.0
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        res = 50.0
        self.m_array[i][12] = price
        if i > 0:
            mom = self.m_array[i][12] - self.m_array[i - 1][12]
            moa = (mom if (mom > 0) else (-mom))
            self.m_array[i][0] = (self.kg * mom) + (self.hg * self.m_array[i - 1][0])
            self.m_array[i][1] = (self.kg * self.m_array[i][0]) + (self.hg * self.m_array[i - 1][1])
            self.m_array[i][2] = (self.kg * ((self.speedp1 * self.m_array[i][0]) - (self.speed * self.m_array[i][1]))) + (self.hg * self.m_array[i - 1][2])
            self.m_array[i][3] = (self.kg * self.m_array[i][2]) + (self.hg * self.m_array[i - 1][3])
            self.m_array[i][4] = (self.kg * ((self.speedp1 * self.m_array[i][2]) - (self.speed * self.m_array[i][3]))) + (self.hg * self.m_array[i - 1][4])
            self.m_array[i][5] = (self.kg * self.m_array[i][4]) + (self.hg * self.m_array[i - 1][5])
            self.m_array[i][6] = (self.kg * moa) + (self.hg * self.m_array[i - 1][6])
            self.m_array[i][7] = (self.kg * self.m_array[i][6]) + (self.hg * self.m_array[i - 1][7])
            self.m_array[i][8] = (self.kg * ((self.speedp1 * self.m_array[i][6]) - (self.speed * self.m_array[i][7]))) + (self.hg * self.m_array[i - 1][8])
            self.m_array[i][9] = (self.kg * self.m_array[i][8]) + (self.hg * self.m_array[i - 1][9])
            self.m_array[i][10] = (self.kg * ((self.speedp1 * self.m_array[i][8]) - (self.speed * self.m_array[i][9]))) + (self.hg * self.m_array[i - 1][10])
            self.m_array[i][11] = (self.kg * self.m_array[i][10]) + (self.hg * self.m_array[i - 1][11])
            mom = (self.speedp1 * self.m_array[i][4]) - (self.speed * self.m_array[i][5])
            moa = (self.speedp1 * self.m_array[i][10]) - (self.speed * self.m_array[i][11])
            res = (_fdiv(mom, (moa if (moa > DBL_MIN) else DBL_MIN)) + 1.0) * 50.0
            if res > 100:
                res = 100.0
            if res < 0:
                res = 0.0
        else:
            for k in range(0, 12):
                self.m_array[i][k] = 0.0
        return res

class cStdDevVolatilityRatio(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sStdDevVolatilityRatioStruct)
        self.m_arraySize = -1
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].price = price
        self.m_array[i].price2 = price * price
        if i > self.m_period:
            self.m_array[i].sum = self.m_array[i - 1].sum + self.m_array[i].price - self.m_array[i - self.m_period].price
            self.m_array[i].sum2 = self.m_array[i - 1].sum2 + self.m_array[i].price2 - self.m_array[i - self.m_period].price2
        else:
            self.m_array[i].sum = self.m_array[i].price
            self.m_array[i].sum2 = self.m_array[i].price2
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sum += self.m_array[i - k].price
                self.m_array[i].sum2 += self.m_array[i - k].price2
                k += 1
        self.m_array[i].deviation = MathSqrt(_fdiv(self.m_array[i].sum2 - _fdiv(self.m_array[i].sum * self.m_array[i].sum, float(self.m_period)), float(self.m_period)))
        if i > self.m_period:
            self.m_array[i].sumd = self.m_array[i - 1].sumd + self.m_array[i].deviation - self.m_array[i - self.m_period].deviation
        else:
            self.m_array[i].sumd = self.m_array[i].deviation
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sumd += self.m_array[i - k].deviation
                k += 1
        deviationAverage = _fdiv(self.m_array[i].sumd, float(self.m_period))
        return (_fdiv(self.m_array[i].deviation, deviationAverage) if (deviationAverage != 0) else 1)

class sStdDevVolatilityRatioStruct(MqlObject):
    _q_fields = ('price', 'price2', 'sum', 'sum2', 'sumd', 'deviation')
    def __init__(self, *args):
        self.price = 0.0
        self.price2 = 0.0
        self.sum = 0.0
        self.sum2 = 0.0
        self.sumd = 0.0
        self.deviation = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iVolatilityRatio.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rsx (vra)(' + _str(inpPeriod) + ')')

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
        _ratio = iVolatilityRatio.calculate(_price, i, rates_total)
        iRsx.init(_fdiv(inpPeriod, _ratio), inpSpeed)
        val[i] = iRsx.calculate(_price, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iRsx = _alloc(cRsx)
iRsx.__init__()
iVolatilityRatio = _alloc(cStdDevVolatilityRatio)
iVolatilityRatio.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsxVra(_MQL5Indicator):
    name = 'Rsx (vra)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpSpeed': 0.5,  # "Speed" (0.5 for original RSX)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

