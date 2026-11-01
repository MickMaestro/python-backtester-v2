"""lwma — converted from MQL5: MQL5 Indicators/Linear Weighted Moving Average/lwma.mq5

Linear Weighted Moving Average
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LWMA'}, 'levels': [], 'description': ['Linear Weighted Moving Average'], 'name': 'lwma', 'source': 'MQL5 Indicators/Linear Weighted Moving Average/lwma.mq5', 'folder': 'Linear Weighted Moving Average', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CLwma(MqlObject):
    _q_fields = ('m_array', 'm_arraySize', 'm_period', 'm_weight')
    def __init__(self):
        self.m_array = Arr(0, 0, factory=sLwmaArrayStruct)
        self.m_arraySize = 0
        self.m_period = 0
        self.m_weight = 0.0
        self.m_period = 1
        self.m_weight = 1.0
        self.m_arraySize = -1
        return
    def _q_dtor(self):
        ArrayFree(self.m_array)
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].value = value
        if i > self.m_period:
            self.m_array[i].wsumm = self.m_array[i - 1].wsumm + (value * self.m_period) - self.m_array[i - 1].vsumm
            self.m_array[i].vsumm = self.m_array[i - 1].vsumm + value - self.m_array[i - self.m_period].value
        else:
            self.m_weight = 0.0
            self.m_array[i].wsumm = 0.0
            self.m_array[i].vsumm = 0.0
            k = 0
            w = self.m_period
            while k < self.m_period and i >= k:
                self.m_weight += w
                self.m_array[i].wsumm += self.m_array[i - k].value * float(w)
                self.m_array[i].vsumm += self.m_array[i - k].value
                k += 1
                w -= 1
        return _fdiv(self.m_array[i].wsumm, self.m_weight)

class sLwmaArrayStruct(MqlObject):
    _q_fields = ('value', 'wsumm', 'vsumm')
    def __init__(self, *args):
        self.value = 0.0
        self.wsumm = 0.0
        self.vsumm = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    _lwma.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Linear Weighted Moving Average (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        val[i] = _lwma.calculate(getPrice(inpPrice, open, high, low, close, i), i, rates_total)
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
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
_lwma = _alloc(CLwma)
_lwma.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Lwma(_MQL5Indicator):
    name = 'lwma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

