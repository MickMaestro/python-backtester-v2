"""Squeeze — converted from MQL5: MQL5 Indicators/Squeeze/Squeeze.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [11119017, 7451452, 17919], 2: [8421504]}, 'widths': {1: 2, 2: 0}, 'styles': {}, 'labels': {1: 'Squeeze', 2: 'Squeeze line'}, 'levels': [], 'description': [], 'name': 'Squeeze', 'source': 'MQL5 Indicators/Squeeze/Squeeze.mq5', 'folder': 'Squeeze', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpDevMultiplier', 'py': 'inpDevMultiplier', 'param': 'inpDevMultiplier', 'type': 'double', 'default': 1.0, 'label': 'Deviation multiplier', 'sinput': False}, {'mql': 'inpAtrMultiplier', 'py': 'inpAtrMultiplier', 'param': 'inpAtrMultiplier', 'type': 'double', 'default': 1.0, 'label': 'ATR multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpDevMultiplier = _input('inpDevMultiplier', 1.0)  # Deviation multiplier
inpAtrMultiplier = _input('inpAtrMultiplier', 1.0)  # ATR multiplier
val = Arr(0, 0.0)
vall = Arr(0, 0.0)
valc = Arr(0, 0.0)

class cSqueeze(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_devMultiplier', 'm_atrMultiplier', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_devMultiplier = 0.0
        self.m_atrMultiplier = 0.0
        self.m_array = Arr(0, 0, factory=sSqueezeStruct)
        self.m_period = 1
        self.m_arraySize = -1
        self.m_devMultiplier = 2.0
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period, devMultiplier, atrMultiplier):
        self.m_period = (period if (period > 1) else 1)
        self.m_devMultiplier = devMultiplier
        self.m_atrMultiplier = atrMultiplier
    def calculate(self, close, high, low, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].price = close[i]
        self.m_array[i].price2 = close[i] * close[i]
        self.m_array[i].tr = (((high[i] if (close[i - 1] < high[i]) else close[i - 1]) - (low[i] if (close[i - 1] > low[i]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
        if i > self.m_period:
            self.m_array[i].sum = self.m_array[i - 1].sum + self.m_array[i].price - self.m_array[i - self.m_period].price
            self.m_array[i].sum2 = self.m_array[i - 1].sum2 + self.m_array[i].price2 - self.m_array[i - self.m_period].price2
            self.m_array[i].sumtr = self.m_array[i - 1].sumtr + self.m_array[i].tr - self.m_array[i - self.m_period].tr
        else:
            self.m_array[i].sum = self.m_array[i].price
            self.m_array[i].sum2 = self.m_array[i].price2
            self.m_array[i].sumtr = self.m_array[i].tr
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sum += self.m_array[i - k].price
                self.m_array[i].sum2 += self.m_array[i - k].price2
                self.m_array[i].sumtr += self.m_array[i - k].tr
                k += 1
        _dev = MathSqrt(_fdiv(self.m_array[i].sum2 - _fdiv(self.m_array[i].sum * self.m_array[i].sum, float(self.m_period)), float(self.m_period)))
        _atr = _fdiv(self.m_array[i].sumtr, float(self.m_period))
        _avg = _fdiv(self.m_array[i].sum, float(self.m_period))
        return ((1 if (((high[i] + low[i]) / 2.0) > _avg) else -1) if ((self.m_devMultiplier * _dev) > (self.m_atrMultiplier * _atr)) else 0)

class sSqueezeStruct(MqlObject):
    _q_fields = ('price', 'price2', 'sum', 'sum2', 'tr', 'sumtr')
    def __init__(self, *args):
        self.price = 0.0
        self.price2 = 0.0
        self.sum = 0.0
        self.sum2 = 0.0
        self.tr = 0.0
        self.sumtr = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vall, INDICATOR_DATA)
    iSqueeze.init(inpPeriod, inpDevMultiplier, inpAtrMultiplier)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Squeeze (' + _str(inpPeriod) + ',' + _str(inpDevMultiplier) + ',' + _str(inpAtrMultiplier) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        vall[i] = iSqueeze.calculate(close, high, low, i, rates_total)
        val[i] = vall[i]
        valc[i] = (1 if (val[i] == 1) else 2 if (val[i] == -1) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iSqueeze = _alloc(cSqueeze)
iSqueeze.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Squeeze(_MQL5Indicator):
    name = 'Squeeze'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period
        'inpDevMultiplier': 1.0,  # Deviation multiplier
        'inpAtrMultiplier': 1.0,  # ATR multiplier
    }

