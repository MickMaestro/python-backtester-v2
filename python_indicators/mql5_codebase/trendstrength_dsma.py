"""TrendStrength DSMA — converted from MQL5: MQL5 Indicators/TrendStrength DSMA/TrendStrength DSMA.mq5

TrendStrength of deviation scaled MA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [11119017], 2: [16748574], 3: [6333684]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'DSMA', 2: 'trend up', 3: 'trend down'}, 'levels': [], 'description': ['TrendStrength of deviation scaled MA'], 'name': 'TrendStrength DSMA', 'source': 'MQL5 Indicators/TrendStrength DSMA/TrendStrength DSMA.mq5', 'folder': 'TrendStrength DSMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'DSMA period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpStrength', 'py': 'inpStrength', 'param': 'inpStrength', 'type': 'double', 'default': 4.236, 'label': 'Strength', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # DSMA period
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

class cDsma(MqlObject):
    _q_fields = ('m_OK', 'm_period', 'm_arraysize', 'm_periodMultiplier', 'm_sc1', 'm_sc2', 'm_sc3', 'm_array')
    def __init__(self):
        self.m_OK = False
        self.m_period = 0
        self.m_arraysize = 0
        self.m_periodMultiplier = 0.0
        self.m_sc1 = 0.0
        self.m_sc2 = 0.0
        self.m_sc3 = 0.0
        self.m_array = Arr(0, 0, factory=sDsmaArray)
        self.init(1)
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_periodMultiplier = _fdiv(5.0, float(self.m_period))
        self.m_arraysize = self.m_period + 32
        self.m_OK = ArrayResize(self.m_array, self.m_arraysize) == self.m_arraysize
        a1 = MathExp(_fdiv(-1.414 * M_PI_2, self.m_period))
        self.m_sc2 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, self.m_period))
        self.m_sc3 = (-a1) * a1
        self.m_sc1 = 1.0 - self.m_sc2 - self.m_sc3
        return self.m_OK
    def calculate(self, price, i):
        if not self.m_OK:
            return price
        _indC = _imod(i, self.m_arraysize)
        self.m_array[_indC].price = price
        if i > 1:
            _indP = _imod(i - 1, self.m_arraysize)
            _indP2 = _imod(i - 2, self.m_arraysize)
            self.m_array[_indC].filter = self.m_array[_indC].price - self.m_array[_indP2].price
            self.m_array[_indC].ssm = ((self.m_sc1 * (self.m_array[_indC].filter + self.m_array[_indP].filter)) / 2.0) + (self.m_sc2 * self.m_array[_indP].ssm) + (self.m_sc3 * self.m_array[_indP2].ssm)
            self.m_array[_indC].mul = self.m_array[_indC].ssm * self.m_array[_indC].ssm
            if i > self.m_period:
                self.m_array[_indC].sum = self.m_array[_indP].sum + self.m_array[_indC].mul - self.m_array[_imod(i - self.m_period, self.m_arraysize)].mul
            else:
                self.m_array[_indC].sum = self.m_array[_indC].mul
                k = 1
                while k < self.m_period and i >= k:
                    self.m_array[_indC].sum += self.m_array[_indC - k].mul
                    k += 1
            rms = (MathSqrt(_fdiv(self.m_array[_indC].sum, self.m_period)) if self.m_array[_indC].sum else 1)
            _scaledFilt = _fdiv(self.m_array[_indC].ssm, rms)
            _alpha = (_scaledFilt if (_scaledFilt > 0) else (-_scaledFilt)) * self.m_periodMultiplier
            self.m_array[_indC].dsm = self.m_array[_indP].dsm + (_alpha * (price - self.m_array[_indP].dsm))
        else:
            self.m_array[_indC].dsm = price
            self.m_array[_indC].filter = 0.0
            self.m_array[_indC].mul = self.m_array[_indC].filter
            self.m_array[_indC].ssm = self.m_array[_indC].mul
        return self.m_array[_indC].dsm

class sDsmaArray(MqlObject):
    _q_fields = ('filter', 'price', 'dsm', 'ssm', 'mul', 'sum')
    def __init__(self, *args):
        self.filter = 0.0
        self.price = 0.0
        self.dsm = 0.0
        self.ssm = 0.0
        self.mul = 0.0
        self.sum = 0.0

def OnInit():
    SetIndexBuffer(0, avg, INDICATOR_DATA)
    SetIndexBuffer(1, valu, INDICATOR_DATA)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    iDsma.init(inpPeriod)
    iTrendStrength.init(inpStrength)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend strength DSMA (' + _str(inpPeriod) + ',' + _str(inpStrength) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        avg[i] = iDsma.calculate(getPrice(inpPrice, open, close, high, low, i), i)
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
iDsma = _alloc(cDsma)
iDsma.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendStrengthDSMA(_MQL5Indicator):
    name = 'TrendStrength DSMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # DSMA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpStrength': 4.236,  # Strength
    }

