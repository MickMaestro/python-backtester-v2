"""Double smoothed Wilders EMA (vra) — converted from MQL5: MQL5 Indicators/Volatility ratio adaptive double smoothed Wilders EMA/Double smoothed Wilders EMA (vra).mq5

Double smoothed Wilders EMA - volatility ratio adaptive
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Double smoothed Wilders EMA'}, 'levels': [], 'description': ['Double smoothed Wilders EMA - volatility ratio adaptive'], 'name': 'Double smoothed Wilders EMA (vra)', 'source': 'MQL5 Indicators/Volatility ratio adaptive double smoothed Wilders EMA/Double smoothed Wilders EMA (vra).mq5', 'folder': 'Volatility ratio adaptive double smoothed Wilders EMA', 'inputs': [{'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpPeriod = _input('inpPeriod', 14)  # Period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
work = Arr(0, 0.0)
_alpha = 0.0

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
    SetIndexBuffer(2, work, INDICATOR_COLOR_INDEX)
    iVolatilityRatio.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Double smoothed Wilders EMA (vra)(' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _alpha
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i)
        if i > 0:
            _ratio = iVolatilityRatio.calculate(_price, i, rates_total)
            _alpha = _fdiv(1.0, MathSqrt((_fdiv(inpPeriod, _ratio) if (inpPeriod > 1) else 1)))
            work[i] = work[i - 1] + (_alpha * (_price - work[i - 1]))
            val[i] = val[i - 1] + (_alpha * (work[i] - val[i - 1]))
            valc[i] = (1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1])
        else:
            val[i] = _price
            work[i] = val[i]
            valc[i] = 0.0
        i += 1
    return i

def getPrice(tprice, open, close, high, low, i):
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
iVolatilityRatio = _alloc(cStdDevVolatilityRatio)
iVolatilityRatio.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DoubleSmoothedWildersEMAVra(_MQL5Indicator):
    name = 'Double smoothed Wilders EMA (vra)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpPeriod': 14,  # Period
    }

