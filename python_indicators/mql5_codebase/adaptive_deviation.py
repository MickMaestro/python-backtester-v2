"""Adaptive deviation — converted from MQL5: MQL5 Indicators/Adaptive deviation/Adaptive deviation.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 7451452]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'adaptive deviation'}, 'levels': [], 'description': [], 'name': 'Adaptive deviation', 'source': 'MQL5 Indicators/Adaptive deviation/Adaptive deviation.mq5', 'folder': 'Adaptive deviation', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class cAdaptiveDeviation(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_fastEnd', 'm_slowEnd', 'm_periodDiff', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_fastEnd = 0.0
        self.m_slowEnd = 0.0
        self.m_periodDiff = 0.0
        self.m_array = Arr(0, 0, factory=sAdaptiveStruct)
        self.m_period = 1
        self.m_arraySize = -1
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_fastEnd = MathMax(self.m_period / 2.0, 1)
        self.m_slowEnd = self.m_period * 5
        self.m_periodDiff = self.m_slowEnd - self.m_fastEnd
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500, 2000)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].price = price
        self.m_array[i].difference = ((self.m_array[i].price - self.m_array[i - 1].price) if (i > 0) else 0)
        if self.m_array[i].difference < 0:
            self.m_array[i].difference *= -1.0
        signal = 0.0
        if i > self.m_period:
            signal = self.m_array[i].price - self.m_array[i - self.m_period].price
            if signal < 0:
                signal *= -1.0
            self.m_array[i].noise = self.m_array[i - 1].noise + self.m_array[i].difference - self.m_array[i - self.m_period].difference
        else:
            k = 0
            while k < self.m_period and i >= k:
                self.m_array[i].noise += self.m_array[i - k].difference
                k += 1
        if i > 0:
            averagePeriod = (((_fdiv(signal, self.m_array[i].noise) * self.m_periodDiff) + self.m_fastEnd) if (self.m_array[i].noise != 0) else self.m_period)
            alpha = _fdiv(2.0, 1.0 + averagePeriod)
            self.m_array[i].ema0 = self.m_array[i - 1].ema0 + (alpha * (price - self.m_array[i - 1].ema0))
            self.m_array[i].ema1 = self.m_array[i - 1].ema1 + (alpha * ((price * price) - self.m_array[i - 1].ema1))
            return MathSqrt(_fdiv(averagePeriod * (self.m_array[i].ema1 - (self.m_array[i].ema0 * self.m_array[i].ema0)), MathMax(averagePeriod - 1, 1)))
        else:
            self.m_array[i].ema1 = price
            self.m_array[i].ema0 = self.m_array[i].ema1
        return 0.0

class sAdaptiveStruct(MqlObject):
    _q_fields = ('price', 'ema0', 'ema1', 'difference', 'noise')
    def __init__(self, *args):
        self.price = 0.0
        self.ema0 = 0.0
        self.ema1 = 0.0
        self.difference = 0.0
        self.noise = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iAdaptiveDeviation.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Adaptive deviation (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = getPrice(inpPrice, open, high, low, close, i)
        val[i] = iAdaptiveDeviation.calculate(_price, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def getPrice(tprice, open, high, low, close, i):
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

# ---- global variables initialised from expressions
iAdaptiveDeviation = _alloc(cAdaptiveDeviation)
iAdaptiveDeviation.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdaptiveDeviation(_MQL5Indicator):
    name = 'Adaptive deviation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 20,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

