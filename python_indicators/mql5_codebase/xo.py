"""XO — converted from MQL5: MQL5 Indicators/XO/XO.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [11119017, 3329330, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'XO'}, 'levels': [], 'description': [], 'name': 'XO', 'source': 'MQL5 Indicators/XO/XO.mq5', 'folder': 'XO', 'inputs': [{'mql': 'inpBoxSize', 'py': 'inpBoxSize', 'param': 'inpBoxSize', 'type': 'double', 'default': 6.5, 'label': 'Box size', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBoxSize = _input('inpBoxSize', 6.5)  # Box size
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CXo(MqlObject):
    _q_fields = ('m_symbol', 'm_boxSize', 'm_firstCalcDone', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_symbol = ""
        self.m_boxSize = 0.0
        self.m_firstCalcDone = False
        self.m_array = Arr(0, 0, factory=sXoStruct)
        self.m_arraySize = 0
        self.m_arraySize = -1
        self.m_boxSize = 0.0
        self.m_firstCalcDone = False
    def _q_dtor(self):
        pass
    def init(self, _boxSize, _symbol=''):
        self.m_symbol = (Symbol() if (_symbol == '') else _symbol)
        self.m_boxSize = _boxSize * SymbolInfoDouble(self.m_symbol, SYMBOL_POINT) * MathPow(10, _imod(_int(SymbolInfoInteger(self.m_symbol, SYMBOL_DIGITS)), 2))
    def calculate(self, _value, _trend, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                _trend.v = 0.0
                return 0.0
        if i > 0 and self.m_firstCalcDone:
            self.m_array[i].high = self.m_array[i - 1].high
            self.m_array[i].low = self.m_array[i - 1].low
            self.m_array[i].pos = self.m_array[i - 1].pos
            self.m_array[i].neg = self.m_array[i - 1].neg
            self.m_array[i].trend = self.m_array[i - 1].trend
            if _value > (self.m_array[i].high + self.m_boxSize):
                self.m_array[i].high = _value
                self.m_array[i].low = _value - self.m_boxSize
                self.m_array[i].pos = self.m_array[i - 1].pos + 1
                self.m_array[i].neg = 0.0
                self.m_array[i].trend = 1.0
            if _value < (self.m_array[i].low - self.m_boxSize):
                self.m_array[i].low = _value
                self.m_array[i].high = _value + self.m_boxSize
                self.m_array[i].neg = self.m_array[i - 1].neg - 1
                self.m_array[i].pos = 0.0
                self.m_array[i].trend = -1.0
        else:
            self.m_array[i].low = _value
            self.m_array[i].high = self.m_array[i].low
            self.m_array[i].trend = 0.0
            self.m_array[i].neg = self.m_array[i].trend
            self.m_array[i].pos = self.m_array[i].neg
            self.m_firstCalcDone = True
        _trend.v = self.m_array[i].trend
        return (self.m_array[i].pos if (self.m_array[i].trend == 1) else self.m_array[i].neg)

class sXoStruct(MqlObject):
    _q_fields = ('high', 'low', 'pos', 'neg', 'trend')
    def __init__(self, *args):
        self.high = 0.0
        self.low = 0.0
        self.pos = 0.0
        self.neg = 0.0
        self.trend = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iXo.init(inpBoxSize)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XO (' + _str(inpBoxSize) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _trend = Box(0.0)
        val[i] = iXo.calculate(getPrice(inpPrice, open, high, low, close, i), _trend, i, rates_total)
        valc[i] = (1 if (_trend.v == 1) else 2 if (_trend.v == -1) else 0)
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
iXo = _alloc(CXo)
iXo.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XO(_MQL5Indicator):
    name = 'XO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBoxSize': 6.5,  # Box size
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

