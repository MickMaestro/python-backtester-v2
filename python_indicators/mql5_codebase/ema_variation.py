"""Ema variation — converted from MQL5: MQL5 Indicators/EMA variation/Ema variation.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'EMA'}, 'levels': [], 'description': [], 'name': 'Ema variation', 'source': 'MQL5 Indicators/EMA variation/Ema variation.mq5', 'folder': 'EMA variation', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpDivisor', 'py': 'inpDivisor', 'param': 'inpDivisor', 'type': 'double', 'default': 3.0, 'label': 'Speed', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpDivisor = _input('inpDivisor', 3.0)  # Speed
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

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
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iEma.init(inpPeriod, inpDivisor)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ema variation (' + _str(inpPeriod) + ',' + _str(inpDivisor) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
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
        val[i] = iEma.calculate(_price, i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iEma = _alloc(CEmaVar)
iEma.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EmaVariation(_MQL5Indicator):
    name = 'Ema variation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period
        'inpDivisor': 3.0,  # Speed
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

