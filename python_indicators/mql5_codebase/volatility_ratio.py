"""Volatility ratio — converted from MQL5: MQL5 Indicators/Volatility ratio/Volatility ratio.mq5

Volatility ratio
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Volatility ratio'}, 'levels': [1.0], 'description': ['Volatility ratio'], 'name': 'Volatility ratio', 'source': 'MQL5 Indicators/Volatility ratio/Volatility ratio.mq5', 'folder': 'Volatility ratio', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 25, 'label': 'Volatility period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25)  # Volatility period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

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
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility ratio (' + _str(inpPeriod) + ')')
    return 0

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
        val[i] = iVolatilityRatio.calculate(_price, i, rates_total)
        valc[i] = (1 if (val[i] > 1) else 2 if (val[i] < 1) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iVolatilityRatio = _alloc(cStdDevVolatilityRatio)
iVolatilityRatio.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityRatio(_MQL5Indicator):
    name = 'Volatility ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25,  # Volatility period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

