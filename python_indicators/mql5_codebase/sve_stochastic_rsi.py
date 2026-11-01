"""SVE Stochastic RSI — converted from MQL5: MQL5 Indicators/SVE Stochastic RSI/SVE Stochastic RSI.mq5

SVE Stochastic RSI
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'SVE Stochastic Rsi'}, 'levels': [], 'description': ['SVE Stochastic RSI'], 'name': 'SVE Stochastic RSI', 'source': 'MQL5 Indicators/SVE Stochastic RSI/SVE Stochastic RSI.mq5', 'folder': 'SVE Stochastic RSI', 'inputs': [{'mql': 'inpRsiPeriod', 'py': 'inpRsiPeriod', 'param': 'inpRsiPeriod', 'type': 'int', 'default': 21, 'label': 'RSI period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpStoPeriod', 'py': 'inpStoPeriod', 'param': 'inpStoPeriod', 'type': 'int', 'default': 8, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpAvgPeriod', 'py': 'inpAvgPeriod', 'param': 'inpAvgPeriod', 'type': 'int', 'default': 5, 'label': 'Average period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpRsiPeriod = _input('inpRsiPeriod', 21)  # RSI period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpStoPeriod = _input('inpStoPeriod', 8)  # Stochastic period
inpAvgPeriod = _input('inpAvgPeriod', 5)  # Average period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
rsi = Arr(0, 0.0)

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

class CSma(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sSmaArrayStruct)
        self.m_period = 1
        self.m_arraySize = -1
        return
    def _q_dtor(self):
        ArrayFree(self.m_array)
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].value = value
        if i > self.m_period:
            self.m_array[i].summ = self.m_array[i - 1].summ + value - self.m_array[i - self.m_period].value
        else:
            self.m_array[i].summ = 0.0
            k = 0
            while k < self.m_period and i >= k:
                self.m_array[i].summ += self.m_array[i - k].value
                k += 1
            return _fdiv(self.m_array[i].summ, float(k))
        return _fdiv(self.m_array[i].summ, float(self.m_period))

class sSmaArrayStruct(MqlObject):
    _q_fields = ('value', 'summ')
    def __init__(self, *args):
        self.value = 0.0
        self.summ = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, rsi, INDICATOR_CALCULATIONS)
    iRsi.init(inpRsiPeriod)
    avgRsiLow.init(inpAvgPeriod)
    avgHighLow.init(inpAvgPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic RSI (' + _str(inpRsiPeriod) + ',' + _str(inpStoPeriod) + ',' + _str(inpAvgPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
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
        rsi[i] = iRsi.calculate(_price, i)
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpStoPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = rsi[ArrayMaximum(rsi, start, inpStoPeriod - 1)]
            _s_OnCalculate_prev_min = rsi[ArrayMinimum(rsi, start, inpStoPeriod - 1)]
        max_ = (rsi[i] if (rsi[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (rsi[i] if (rsi[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        _avgRsiLow = avgRsiLow.calculate(rsi[i] - min_, i, rates_total)
        _avgHighLow = avgHighLow.calculate(max_ - min_, i, rates_total)
        val[i] = (_fdiv(100 * _avgRsiLow, _avgHighLow) if (_avgHighLow != 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iRsi = _alloc(cRsi)
iRsi.__init__()
avgRsiLow = _alloc(CSma)
avgRsiLow.__init__()
avgHighLow = _alloc(CSma)
avgHighLow.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SVEStochasticRSI(_MQL5Indicator):
    name = 'SVE Stochastic RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpRsiPeriod': 21,  # RSI period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpStoPeriod': 8,  # Stochastic period
        'inpAvgPeriod': 5,  # Average period
    }

