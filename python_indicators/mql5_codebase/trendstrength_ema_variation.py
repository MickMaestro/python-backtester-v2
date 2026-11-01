"""TrendStrength EMA variation — converted from MQL5: MQL5 Indicators/TrendStrength EMA variation/TrendStrength EMA variation.mq5

TrendStrength of EMA variation
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11119017], 2: [16748574], 3: [6333684]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'EMA', 2: 'trend up', 3: 'trend down'}, 'levels': [], 'description': ['TrendStrength of EMA variation'], 'name': 'TrendStrength EMA variation', 'source': 'MQL5 Indicators/TrendStrength EMA variation/TrendStrength EMA variation.mq5', 'folder': 'TrendStrength EMA variation', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'EMA period', 'sinput': False}, {'mql': 'inpDivisor', 'py': 'inpDivisor', 'param': 'inpDivisor', 'type': 'double', 'default': 2.0, 'label': 'Speed', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpStrength', 'py': 'inpStrength', 'param': 'inpStrength', 'type': 'double', 'default': 4.236, 'label': 'Strength', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # EMA period
inpDivisor = _input('inpDivisor', 2.0)  # Speed
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpStrength = _input('inpStrength', 4.236)  # Strength
avg = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)

class CTrendStrength(MqlObject):
    _q_fields = ('m_arraySize', 'm_strength', 'm_array')
    def __init__(self):
        self.m_arraySize = 0
        self.m_strength = 0.0
        self.m_array = Arr(0, 0, factory=sTrendStrengthStruct)
        self.m_arraySize = 32
        self.init(1.0)
    def _q_dtor(self):
        pass
    def init(self, strength):
        self.m_strength = strength
        if ArrayResize(self.m_array, self.m_arraySize) == self.m_arraySize:
            return True
        return False
    def calculate(self, value, valueHi, valueLow, resultUp, resultDown, i):
        _indC = _imod(i, self.m_arraySize)
        delta = valueHi - valueLow
        self.m_array[_indC].smin = value - (self.m_strength * delta)
        self.m_array[_indC].smax = value + (self.m_strength * delta)
        if i > 0:
            _indP = _imod(i - 1, self.m_arraySize)
            self.m_array[_indC].trend = self.m_array[_indP].trend
            if value > self.m_array[_indP].smax:
                self.m_array[_indC].trend = 1
            if value < self.m_array[_indP].smin:
                self.m_array[_indC].trend = -1
            if self.m_array[_indC].trend > 0:
                if self.m_array[_indC].smin < self.m_array[_indP].smin:
                    self.m_array[_indC].smin = self.m_array[_indP].smin
                resultUp.v = self.m_array[_indC].smin
                resultDown.v = EMPTY_VALUE
            if self.m_array[_indC].trend < 0:
                if self.m_array[_indC].smax > self.m_array[_indP].smax:
                    self.m_array[_indC].smax = self.m_array[_indP].smax
                resultDown.v = self.m_array[_indC].smax
                resultUp.v = EMPTY_VALUE
        else:
            self.m_array[_indC].trend = 0
            resultDown.v = EMPTY_VALUE
            resultUp.v = resultDown.v
        return True

class sTrendStrengthStruct(MqlObject):
    _q_fields = ('smin', 'smax', 'trend')
    def __init__(self, *args):
        self.smin = 0.0
        self.smax = 0.0
        self.trend = 0

class CEmaVar(MqlObject):
    _q_fields = ('m_period', 'm_divisor', 'm_alpha', 'm_array')
    def __init__(self):
        self.m_period = 0.0
        self.m_divisor = 0.0
        self.m_alpha = 0.0
        self.m_array = Arr(32, 0, dyn=False, factory=sEmaVarStruct)
        self.init(1, 1.0)
        return
    def _q_dtor(self):
        return
    def init(self, period, divisor):
        self.m_period = (period if (period > 1) else 1)
        self.m_divisor = (divisor if (divisor > 0) else 1)
        self.m_alpha = _fdiv(2.0, 1.0 + _fdiv(self.m_period, self.m_divisor))
        return True
    def calculate(self, value, i):
        _indC = _imod(i, 32)
        _indP = _indC - 1
        if _indP < 0:
            _indP += 32
        if i > 0:
            self.m_array[_indC].ema1 = self.m_array[_indP].ema1 + (self.m_alpha * (value - self.m_array[_indP].ema1))
            self.m_array[_indC].ema2 = self.m_array[_indP].ema2 + (self.m_alpha * (self.m_array[_indC].ema1 - self.m_array[_indP].ema2))
        else:
            self.m_array[_indC].ema2 = value
            self.m_array[_indC].ema1 = self.m_array[_indC].ema2
        return self.m_array[_indC].ema2

class sEmaVarStruct(MqlObject):
    _q_fields = ('ema1', 'ema2')
    def __init__(self, *args):
        self.ema1 = 0.0
        self.ema2 = 0.0

def OnInit():
    SetIndexBuffer(0, avg, INDICATOR_DATA)
    SetIndexBuffer(1, valu, INDICATOR_DATA)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    iEmaVar.init(inpPeriod, inpDivisor)
    iTrendStrength.init(inpStrength)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend strength EMA variation (' + _str(inpPeriod) + ',' + _str(inpDivisor) + ',' + _str(inpStrength) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        avg[i] = iEmaVar.calculate(getPrice(inpPrice, open, close, high, low, i), i)
        hval = avg[i]
        lval = avg[i]
        if i > 0:
            if avg[i] > avg[i - 1]:
                lval = avg[i - 1]
            if avg[i] < avg[i - 1]:
                hval = avg[i - 1]
        iTrendStrength.calculate(avg[i], hval, lval, _ElemRef(valu, i), _ElemRef(vald, i), i)
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
iTrendStrength = _alloc(CTrendStrength)
iTrendStrength.__init__()
iEmaVar = _alloc(CEmaVar)
iEmaVar.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendStrengthEMAVariation(_MQL5Indicator):
    name = 'TrendStrength EMA variation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # EMA period
        'inpDivisor': 2.0,  # Speed
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpStrength': 4.236,  # Strength
    }

