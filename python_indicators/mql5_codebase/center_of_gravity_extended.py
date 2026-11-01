"""Center of Gravity - extended — converted from MQL5: MQL5 Indicators/Center of Gravity - extended/Center of Gravity - extended.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [12632256, 7451452, 17919], 2: [12632256]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'CoG', 2: 'CoG trigger'}, 'levels': [], 'description': [], 'name': 'Center of Gravity - extended', 'source': 'MQL5 Indicators/Center of Gravity - extended/Center of Gravity - extended.mq5', 'folder': 'Center of Gravity - extended', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 0, 'label': 'Color change method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
cch_onTrigger = 0
cch_onZero = 1
cch_onSlope = 2
_enum('enColorOn', {0: 'cch_onTrigger', 1: 'cch_onZero', 2: 'cch_onSlope'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Period
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpColorOn = _input('inpColorOn', cch_onTrigger)  # Color change method
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
valt = Arr(0, 0.0)

class cCg(MqlObject):
    _q_fields = ('originalPeriod', 'period', 'arraySize', 'correction', 'sump', 'sumw', 'prices')
    def __init__(self):
        self.originalPeriod = 0
        self.period = 0
        self.arraySize = 0
        self.correction = 0.0
        self.sump = Arr(0, 0.0)
        self.sumw = Arr(0, 0.0)
        self.prices = Arr(0, 0.0)
        self.originalPeriod = -1
        return
    def _q_dtor(self):
        ArrayFree(self.sump)
        ArrayFree(self.sumw)
        ArrayFree(self.prices)
        return
    def Calculate(self, price, calcPeriod, i):
        if self.originalPeriod != calcPeriod:
            self.originalPeriod = calcPeriod
            self.period = (calcPeriod if (calcPeriod > 1) else 1)
            self.arraySize = self.period + 32
            ArrayResize(self.sump, self.arraySize)
            ArrayInitialize(self.sump, 0)
            ArrayResize(self.sumw, self.arraySize)
            ArrayInitialize(self.sumw, 0)
            ArrayResize(self.prices, self.arraySize)
            ArrayInitialize(self.prices, 0)
        _indC = _imod(i, self.arraySize)
        self.prices[_indC] = price
        if i > self.period:
            _indP = _indC - 1
            if _indP < 0:
                _indP += self.arraySize
            _indF = _indC - self.period
            if _indF < 0:
                _indF += self.arraySize
            self.sump[_indC] = self.sump[_indP] + self.prices[_indC] - self.prices[_indF]
            self.sumw[_indC] = self.sumw[_indP] + self.sump[_indC] - (self.prices[_indF] * self.period)
        else:
            self.correction = 1.0
            self.sumw[_indC] = self.prices[_indC]
            self.sump[_indC] = self.sumw[_indC]
            k = 1
            _indP = _indC - 1
            while k < self.period:
                if _indP < 0:
                    _indP += self.arraySize
                self.sump[_indC] += self.prices[_indP]
                self.sumw[_indC] += self.prices[_indP] * (k + 1)
                self.correction += k + 1
                k += 1
                _indP -= 1
            self.correction = _fdiv(self.correction, self.period)
        return _fdiv(-self.sumw[_indC], self.sump[_indC]) + self.correction

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valt, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Center of gravity (' + _str(inpPeriod) + ')')

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
        val[i] = iCg.Calculate(_price, inpPeriod, i)
        valt[i] = (val[i - 1] if (i > 0) else val[i])
        _sw2 = inpColorOn
        if _sw2 == cch_onTrigger:
            valc[i] = (1 if (val[i] > valt[i]) else 2 if (val[i] < valt[i]) else valc[i - 1] if (i > 0) else 0)
        elif _sw2 == cch_onZero:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iCg = _alloc(cCg)
iCg.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CenterOfGravityExtended(_MQL5Indicator):
    name = 'Center of Gravity - extended'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 32,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpColorOn': _Choice({0: 'Change color on signal/trigger cross', 1: 'Change color on zero line cross', 2: 'Change color on slope change'}, default=0),  # Color change method
    }

