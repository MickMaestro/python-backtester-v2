"""RSI(oma) (smoother) — converted from MQL5: MQL5 Indicators/RSI of smoother average/RSI(oma) (smoother).mq5

RSI of smoother average
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [6908265], 2: [11119017, 7451452, 17919]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'RSI(oma) of smoother shadow', 2: 'RSI(oma) of smoother'}, 'levels': [], 'description': ['RSI of smoother average'], 'name': 'RSI(oma) (smoother)', 'source': 'MQL5 Indicators/RSI of smoother average/RSI(oma) (smoother).mq5', 'folder': 'RSI of smoother average', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 32, 'label': 'Smoother period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpShadow', 'py': 'inpShadow', 'param': 'inpShadow', 'type': 'int', 'default': 7, 'label': '"Shadow" width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpMaPeriod = _input('inpMaPeriod', 32)  # Smoother period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpShadow = _input('inpShadow', 7)  # "Shadow" width
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)

class cRsi(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_alpha', 'm_work')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_alpha = 0.0
        self.m_work = Arr(0, 0, factory=sRsiArray)
        self.m_period = 1
        self.m_alpha = 1.0
        self.m_arraySize = 33
        ArrayResize(self.m_work, 33)
        return
    def _q_dtor(self):
        ArrayFree(self.m_work)
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_arraySize = self.m_period + 32
        self.m_alpha = _fdiv(1.0, MathSqrt(self.m_period))
        ArrayResize(self.m_work, self.m_arraySize)
    def calculate(self, price, i):
        _indC = _imod(i, self.m_arraySize)
        self.m_work[_indC].price = price
        if i > self.m_period:
            _indP = _indC - 1
            if _indP < 0:
                _indP += self.m_arraySize
            change = self.m_work[_indC].price - self.m_work[_indP].price
            changa = change
            if change < 0:
                changa = -change
            self.m_work[_indC].change1 = self.m_work[_indP].change1 + (self.m_alpha * (change - self.m_work[_indP].change1))
            self.m_work[_indC].change = self.m_work[_indP].change + (self.m_alpha * (self.m_work[_indC].change1 - self.m_work[_indP].change))
            self.m_work[_indC].changa1 = self.m_work[_indP].changa1 + (self.m_alpha * (changa - self.m_work[_indP].changa1))
            self.m_work[_indC].changa = self.m_work[_indP].changa + (self.m_alpha * (self.m_work[_indC].changa1 - self.m_work[_indP].changa))
        else:
            self.m_work[_indC].changa = 0.0
            k = 0
            while i > k:
                self.m_work[_indC].changa += ((self.m_work[_indC - k].price - self.m_work[_indC - k - 1].price) if (self.m_work[_indC - k].price > self.m_work[_indC - k - 1].price) else (self.m_work[_indC - k - 1].price - self.m_work[_indC - k].price))
                k += 1
            self.m_work[_indC].changa = _fdiv(self.m_work[_indC].changa, i + 1.0)
            self.m_work[_indC].changa1 = self.m_work[_indC].changa
            self.m_work[_indC].change = _fdiv(self.m_work[_indC].price - self.m_work[0].price, i + 1.0)
            self.m_work[_indC].change1 = self.m_work[_indC].change
        if self.m_work[_indC].changa != 0:
            return 50.0 * (_fdiv(self.m_work[_indC].change, self.m_work[_indC].changa) + 1.0)
        else:
            return 0.0

class sRsiArray(MqlObject):
    _q_fields = ('price', 'change1', 'changa1', 'change', 'changa')
    def __init__(self, *args):
        self.price = 0.0
        self.change1 = 0.0
        self.changa1 = 0.0
        self.change = 0.0
        self.changa = 0.0

class CSmoother(MqlObject):
    _q_fields = ('m_period', 'm_alpha', 'm_beta', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0.0
        self.m_alpha = 0.0
        self.m_beta = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=CSmootherStruct)
        self.m_arraySize = -1
        self.m_alpha = 1.0
        self.m_beta = 1.0
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_beta = _fdiv(0.45 * (self.m_period - 1.0), (0.45 * (self.m_period - 1)) + 2.0)
        self.m_alpha = self.m_beta * self.m_beta * self.m_beta
        return True
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if i > 0:
            self.m_array[i].l0 = ((1.0 - self.m_alpha) * value) + (self.m_alpha * self.m_array[i - 1].l0)
            self.m_array[i].l1 = ((value - self.m_array[i].l0) * (1 - self.m_beta)) + (self.m_beta * self.m_array[i - 1].l1)
            self.m_array[i].l2 = self.m_array[i].l0 + self.m_array[i].l1
            self.m_array[i].l3 = ((self.m_array[i].l2 - self.m_array[i - 1].l4) * (1.0 - self.m_alpha) * (1.0 - self.m_alpha)) + (self.m_alpha * self.m_alpha * self.m_array[i - 1].l3)
            self.m_array[i].l4 = self.m_array[i - 1].l4 + self.m_array[i].l3
        else:
            self.m_array[i].l4 = value
            self.m_array[i].l1 = self.m_array[i].l4
            self.m_array[i].l0 = self.m_array[i].l1
            self.m_array[i].l3 = 0.0
            self.m_array[i].l2 = self.m_array[i].l3
        return self.m_array[i].l4

class CSmootherStruct(MqlObject):
    _q_fields = ('l0', 'l1', 'l2', 'l3', 'l4')
    def __init__(self, *args):
        self.l0 = 0.0
        self.l1 = 0.0
        self.l2 = 0.0
        self.l3 = 0.0
        self.l4 = 0.0

def OnInit():
    SetIndexBuffer(0, vals, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, inpShadow)
    iRsi.init(inpRsiPeriod)
    iSmoother.init(inpMaPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI (of smoother ' + _str(inpMaPeriod) + ') (' + _str(inpRsiPeriod) + ')')
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
        vals[i] = iRsi.calculate(iSmoother.calculate(_price, i, rates_total), i)
        val[i] = vals[i]
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iRsi = _alloc(cRsi)
iRsi.__init__()
iSmoother = _alloc(CSmoother)
iSmoother.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOmaSmoother(_MQL5Indicator):
    name = 'RSI(oma) (smoother)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpMaPeriod': 32,  # Smoother period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpShadow': 7,  # "Shadow" width
    }

