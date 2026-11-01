"""Ssm RSI — converted from MQL5: MQL5 Indicators/Super smoother RSI/Ssm RSI.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Ssm RSI'}, 'levels': [], 'description': [], 'name': 'Ssm RSI', 'source': 'MQL5 Indicators/Super smoother RSI/Ssm RSI.mq5', 'folder': 'Super smoother RSI', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 10)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CSsmRsi(MqlObject):
    _q_fields = ('m_period', 'm_coeff1', 'm_coeff2', 'm_coeff3', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_coeff1 = 0.0
        self.m_coeff2 = 0.0
        self.m_coeff3 = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sSsmRsiArrayStruct)
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        a = MathExp(_fdiv(-1.414 * M_PI, self.m_period))
        self.m_coeff2 = 2 * a * MathCos(_fdiv(1.414 * M_PI, self.m_period))
        self.m_coeff3 = (-a) * a
        self.m_coeff1 = 1 - self.m_coeff2 - self.m_coeff3
        self.m_arraySize = self.m_period + 32
        if ArrayResize(self.m_array, self.m_arraySize) != self.m_arraySize:
            return False
        return True
    def caculate(self, value, i):
        _indC = _imod(i, self.m_arraySize)
        self.m_array[_indC].value = value
        _indP = _indC - 1
        if _indP < 0:
            _indP += self.m_arraySize
        if i > self.m_period:
            _indF = _imod(i - self.m_period, self.m_arraySize)
            if self.m_array[_indC].value > self.m_array[_indP].value:
                self.m_array[_indC].diffp = self.m_array[_indC].value - self.m_array[_indP].value
                self.m_array[_indC].diffn = 0.0
            else:
                self.m_array[_indC].diffn = self.m_array[_indP].value - self.m_array[_indC].value
                self.m_array[_indC].diffp = 0.0
            self.m_array[_indC].sump = self.m_array[_indP].sump + self.m_array[_indC].diffp - self.m_array[_indF].diffp
            self.m_array[_indC].sumn = self.m_array[_indP].sumn + self.m_array[_indC].diffn - self.m_array[_indF].diffn
        else:
            self.m_array[_indC].diffp = (((self.m_array[_indC].value - self.m_array[_indP].value) if (self.m_array[_indC].value > self.m_array[_indP].value) else 0) if (i > 0) else 0)
            self.m_array[_indC].diffn = (((self.m_array[_indP].value - self.m_array[_indC].value) if (self.m_array[_indC].value < self.m_array[_indP].value) else 0) if (i > 0) else 0)
            self.m_array[_indC].sump = self.m_array[_indC].diffp
            self.m_array[_indC].sumn = self.m_array[_indC].diffn
            k = 1
            _indF = _indP
            while k < self.m_period and i >= k:
                self.m_array[_indC].sump += self.m_array[_indF].diffp
                self.m_array[_indC].sumn += self.m_array[_indF].diffn
                k += 1
                _indF -= 1
        if i > 1:
            self.m_array[_indC].sumps = ((self.m_coeff1 * (self.m_array[_indC].sump + self.m_array[_indP].sump)) / 2.0) + (self.m_coeff2 * self.m_array[_indP].sumps) + (self.m_coeff3 * self.m_array[_imod(i - 2, self.m_arraySize)].sumps)
            self.m_array[_indC].sumns = ((self.m_coeff1 * (self.m_array[_indC].sumn + self.m_array[_indP].sumn)) / 2.0) + (self.m_coeff2 * self.m_array[_indP].sumns) + (self.m_coeff3 * self.m_array[_imod(i - 2, self.m_arraySize)].sumns)
        else:
            self.m_array[_indC].sumps = self.m_array[_indC].sump
            self.m_array[_indC].sumns = self.m_array[_indC].sumn
        return ((100.0 - _fdiv(100.0, 1.0 + _fdiv(self.m_array[_indC].sumps, self.m_array[_indC].sumns))) if (self.m_array[_indC].sumns != 0) else 0)

class sSsmRsiArrayStruct(MqlObject):
    _q_fields = ('value', 'diffp', 'diffn', 'sump', 'sumn', 'sumps', 'sumns')
    def __init__(self, *args):
        self.value = 0.0
        self.diffp = 0.0
        self.diffn = 0.0
        self.sump = 0.0
        self.sumn = 0.0
        self.sumps = 0.0
        self.sumns = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iSsmRsi.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ssm RSI (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

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
        val[i] = iSsmRsi.caculate(_price, i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iSsmRsi = _alloc(CSsmRsi)
iSsmRsi.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SsmRSI(_MQL5Indicator):
    name = 'Ssm RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 10,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

