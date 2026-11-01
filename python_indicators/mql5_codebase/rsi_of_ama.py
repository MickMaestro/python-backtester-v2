"""RSI of AMA — converted from MQL5: MQL5 Indicators/RSI of AMA/RSI of AMA.mq5

RSI of Adaptive Moving Average - generalized version
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'RSI of AMA'}, 'levels': [], 'description': ['RSI of Adaptive Moving Average - generalized version'], 'name': 'RSI of AMA', 'source': 'MQL5 Indicators/RSI of AMA/RSI of AMA.mq5', 'folder': 'RSI of AMA', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'AMA Period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 2, 'label': 'AMA Fast end period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 30, 'label': 'AMA Slow end period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 14)  # RSI period
inpPeriod = _input('inpPeriod', 14)  # AMA Period
inpFastPeriod = _input('inpFastPeriod', 2)  # AMA Fast end period
inpSlowPeriod = _input('inpSlowPeriod', 30)  # AMA Slow end period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
ama = Arr(0, 0.0)

class CAma(MqlObject):
    _q_fields = ('m_period', 'm_prev_i', 'm_fastEnd', 'm_slowEnd', 'm_multiplier', 'm_prev_max', 'm_prev_min')
    def __init__(self):
        self.m_period = 0
        self.m_prev_i = 0
        self.m_fastEnd = 0.0
        self.m_slowEnd = 0.0
        self.m_multiplier = 0.0
        self.m_prev_max = 0.0
        self.m_prev_min = 0.0
        self.init(1, 2.0, 30.0)
        return
    def _q_dtor(self):
        return
    def init(self, period, fastEnd, slowEnd):
        self.m_period = ((period + 1) if (period > 1) else 2)
        self.m_fastEnd = _fdiv(2.0, fastEnd + 1.0)
        self.m_slowEnd = _fdiv(2.0, slowEnd + 1.0)
        return True
    def calculate(self, value, target, arrayMax, arrayMin, i):
        if self.m_prev_i != i:
            self.m_prev_i = i
            start = i - self.m_period + 1
            if start < 0:
                start = 0
            self.m_prev_max = arrayMax[ArrayMaximum(arrayMax, start, self.m_period - 1)]
            self.m_prev_min = arrayMin[ArrayMinimum(arrayMin, start, self.m_period - 1)]
        max_ = (arrayMax[i] if (arrayMax[i] > self.m_prev_max) else self.m_prev_max)
        min_ = (arrayMin[i] if (arrayMin[i] < self.m_prev_min) else self.m_prev_min)
        mltp = (_fdiv(value - min_ - (max_ - value), max_ - min_) if (max_ != min_) else 1)
        if mltp < 0:
            mltp *= -1
        ssc = (mltp * (self.m_fastEnd - self.m_slowEnd)) + self.m_slowEnd
        _assign(target[i], ((target[i - 1] + (ssc * ssc * (value - target[i - 1]))) if (i > 0) else value))

class cRsi(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_alpha', 'm_work')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_alpha = 0.0
        self.m_work = Arr(0, 0, factory=sRsiArray)
        self.init(1)
        return
    def _q_dtor(self):
        ArrayFree(self.m_work)
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_arraySize = self.m_period + 32
        self.m_alpha = _fdiv(1.0, self.m_period)
        ArrayResize(self.m_work, self.m_arraySize)
    def calculate(self, price, i):
        _indC = _imod(i, self.m_arraySize)
        self.m_work[_indC].price = price
        if i < self.m_period:
            self.m_work[_indC].changa = 0.0
            k = 0
            while i > k:
                self.m_work[_indC].changa += ((self.m_work[_indC - k].price - self.m_work[_indC - k - 1].price) if (self.m_work[_indC - k].price > self.m_work[_indC - k - 1].price) else (self.m_work[_indC - k - 1].price - self.m_work[_indC - k].price))
                k += 1
            self.m_work[_indC].changa = _fdiv(self.m_work[_indC].changa, i + 1.0)
            self.m_work[_indC].change = _fdiv(self.m_work[_indC].price - self.m_work[0].price, i + 1.0)
        else:
            _indP = _indC - 1
            if _indP < 0:
                _indP += self.m_arraySize
            change = self.m_work[_indC].price - self.m_work[_indP].price
            changa = change
            if change < 0:
                changa = -change
            self.m_work[_indC].change = self.m_work[_indP].change + (self.m_alpha * (change - self.m_work[_indP].change))
            self.m_work[_indC].changa = self.m_work[_indP].changa + (self.m_alpha * (changa - self.m_work[_indP].changa))
        return 50.0 * (_fdiv(self.m_work[_indC].change, self.m_work[_indC].changa + DBL_MIN) + 1.0)

class sRsiArray(MqlObject):
    _q_fields = ('price', 'change', 'changa')
    def __init__(self, *args):
        self.price = 0.0
        self.change = 0.0
        self.changa = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ama, INDICATOR_CALCULATIONS)
    iAma.init(inpPeriod, inpFastPeriod, inpSlowPeriod)
    iRsi.init(inpRsiPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI (' + _str(inpRsiPeriod) + ') of AMA (' + _str(inpPeriod) + ',' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            prices[i] = close[i]
        elif _sw1 == PRICE_OPEN:
            prices[i] = open[i]
        elif _sw1 == PRICE_HIGH:
            prices[i] = high[i]
        elif _sw1 == PRICE_LOW:
            prices[i] = low[i]
        elif _sw1 == PRICE_MEDIAN:
            prices[i] = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            prices[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            prices[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            prices[i] = 0.0
        iAma.calculate(prices[i], ama, prices, prices, i)
        val[i] = iRsi.calculate(ama[i], i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iAma = _alloc(CAma)
iAma.__init__()
iRsi = _alloc(cRsi)
iRsi.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOfAMA(_MQL5Indicator):
    name = 'RSI of AMA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 14,  # RSI period
        'inpPeriod': 14,  # AMA Period
        'inpFastPeriod': 2,  # AMA Fast end period
        'inpSlowPeriod': 30,  # AMA Slow end period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

