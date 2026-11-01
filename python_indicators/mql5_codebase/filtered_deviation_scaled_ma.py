"""Filtered Deviation scaled MA — converted from MQL5: MQL5 Indicators/Filtered deviation scaled MA/Filtered Deviation scaled MA.mq5

Filtered Deviation scaled MA
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'DSMA'}, 'levels': [], 'description': ['Filtered Deviation scaled MA'], 'name': 'Filtered Deviation scaled MA', 'source': 'MQL5 Indicators/Filtered deviation scaled MA/Filtered Deviation scaled MA.mq5', 'folder': 'Filtered deviation scaled MA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 25, 'label': 'MA period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpPeriodf', 'py': 'inpPeriodf', 'param': 'inpPeriodf', 'type': 'int', 'default': 0, 'label': 'Filter period (<= 1 - same as ma period)', 'sinput': False}, {'mql': 'inpFilter', 'py': 'inpFilter', 'param': 'inpFilter', 'type': 'double', 'default': 1.0, 'label': 'Filter size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 25)  # MA period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpPeriodf = _input('inpPeriodf', 0)  # Filter period (<= 1 - same as ma period)
inpFilter = _input('inpFilter', 1.0)  # Filter size
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class cDsma(MqlObject):
    _q_fields = ('m_period', 'm_arraysize', 'm_periodMultiplier', 'm_sc1', 'm_sc2', 'm_sc3', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraysize = 0
        self.m_periodMultiplier = 0.0
        self.m_sc1 = 0.0
        self.m_sc2 = 0.0
        self.m_sc3 = 0.0
        self.m_array = Arr(0, 0, factory=sDsmaArray)
        self.m_period = INT_MIN
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_periodMultiplier = _fdiv(5.0, float(self.m_period))
        self.m_arraysize = self.m_period + 32
        ArrayResize(self.m_array, self.m_arraysize)
        a1 = MathExp(_fdiv(-1.414 * M_PI_2, self.m_period))
        self.m_sc2 = 2.0 * a1 * MathCos(_fdiv(1.414 * M_PI, self.m_period))
        self.m_sc3 = (-a1) * a1
        self.m_sc1 = 1.0 - self.m_sc2 - self.m_sc3
    def calculate(self, price, i):
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

class cFilter(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_filter', 'm_filter2', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_filter = 0.0
        self.m_filter2 = 0.0
        self.m_array = Arr(0, 0, factory=sFilterArrayStruct)
        self.init(1, 0.0)
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period, filter_):
        self.m_period = (period if (period > 1) else 1)
        self.m_filter = filter_
        self.m_filter2 = self.m_filter * self.m_filter
        self.m_arraySize = self.m_period + 32
        ArrayResize(self.m_array, self.m_arraySize)
    def calculate(self, value, i):
        if self.m_filter <= 0:
            return value
        _indC = _imod(i, self.m_arraySize)
        _indP = _imod(i - 1, self.m_arraySize)
        self.m_array[_indC].value = value
        self.m_array[_indC].change = (((self.m_array[_indC].value - self.m_array[_indP].value) if (self.m_array[_indC].value > self.m_array[_indP].value) else (self.m_array[_indP].value - self.m_array[_indC].value)) if (i > 0) else 0)
        if i > self.m_period:
            _indF = _imod(i - self.m_period, self.m_arraySize)
            self.m_array[_indC].sumc = self.m_array[_indP].sumc + self.m_array[_indC].change - self.m_array[_indF].change
            self.m_array[_indC].power = (self.m_array[_indC].change - _fdiv(self.m_array[_indC].sumc, float(self.m_period))) * (self.m_array[_indC].change - _fdiv(self.m_array[_indC].sumc, float(self.m_period)))
            self.m_array[_indC].sump = self.m_array[_indP].sump + self.m_array[_indC].power - self.m_array[_indF].power
            if _fdiv(self.m_array[_indC].change * self.m_array[_indC].change, self.m_filter2) < _fdiv(self.m_array[_indC].sump, float(self.m_period)):
                self.m_array[_indC].value = self.m_array[_indP].value
        else:
            self.m_array[_indC].sump = 0.0
            self.m_array[_indC].sumc = self.m_array[_indC].sump
            k = 0
            while k < self.m_period and i >= k:
                self.m_array[_indC].sumc += self.m_array[i - k].change
                k += 1
            self.m_array[_indC].power = (self.m_array[_indC].change - _fdiv(self.m_array[_indC].sumc, float(self.m_period))) * (self.m_array[_indC].change - _fdiv(self.m_array[_indC].sumc, float(self.m_period)))
            k = 0
            while k < self.m_period and i >= k:
                self.m_array[_indC].sump += self.m_array[i - k].power
                k += 1
        return self.m_array[_indC].value

class sFilterArrayStruct(MqlObject):
    _q_fields = ('value', 'change', 'power', 'sumc', 'sump')
    def __init__(self, *args):
        self.value = 0.0
        self.change = 0.0
        self.power = 0.0
        self.sumc = 0.0
        self.sump = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iDsma.init(inpPeriod)
    iFilter.init((inpPeriodf if (inpPeriodf > 1) else inpPeriod), inpFilter)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Deviation scaled MA (' + _str(inpPeriod) + ')')
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
        val[i] = iFilter.calculate(iDsma.calculate(_price, i), i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iDsma = _alloc(cDsma)
iDsma.__init__()
iFilter = _alloc(cFilter)
iFilter.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FilteredDeviationScaledMA(_MQL5Indicator):
    name = 'Filtered Deviation scaled MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 25,  # MA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpPeriodf': 0,  # Filter period (<= 1 - same as ma period)
        'inpFilter': 1.0,  # Filter size
    }

