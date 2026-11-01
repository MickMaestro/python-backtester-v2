"""Frama (filtered) — converted from MQL5: MQL5 Indicators/Filtered frama/Frama (filtered).mq5

Frama (Ehlers) filtered
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 16760576, 8036607]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Frama'}, 'levels': [], 'description': ['Frama (Ehlers) filtered'], 'name': 'Frama (filtered)', 'source': 'MQL5 Indicators/Filtered frama/Frama (filtered).mq5', 'folder': 'Filtered frama', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 30, 'label': 'Frama period', 'sinput': False}, {'mql': 'inpFilter', 'py': 'inpFilter', 'param': 'inpFilter', 'type': 'double', 'default': 1.0, 'label': 'Filter size', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpHlMode', 'py': 'inpHlMode', 'param': 'inpHlMode', 'type': 'int', 'default': 0, 'label': 'High/low mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enUseHighLow
hl_useHighLow = 0
hl_usePrices = 1
_enum('enUseHighLow', {0: 'hl_useHighLow', 1: 'hl_usePrices'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 30)  # Frama period
inpFilter = _input('inpFilter', 1.0)  # Filter size
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpHlMode = _input('inpHlMode', hl_useHighLow)  # High/low mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)
_fullSize = 0
_halfSize = 0
_halfSizem = 0

class CFilter(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_filter', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_filter = 0.0
        self.m_array = Arr(0, 0, factory=sFilterArrayStruct)
        self.init(1, 0.0)
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period, filter_):
        self.m_period = (period if (period > 1) else 1)
        self.m_filter = (filter_ if (filter_ >= 0) else 0)
        self.m_arraySize = self.m_period + 32
        if ArrayResize(self.m_array, self.m_arraySize) != self.m_arraySize:
            return False
        return True
    def calculate(self, value, i):
        _indC = _imod(i, self.m_arraySize)
        _indP = _imod(i - 1, self.m_arraySize)
        self.m_array[_indC].value = value
        _change = ((self.m_array[_indC].value - self.m_array[_indP].value) if (i > 0) else 0)
        self.m_array[_indC].change = (_change if (_change > 0) else (-_change))
        if i > self.m_period:
            _indF = _imod(i - self.m_period, self.m_arraySize)
            self.m_array[_indC].summc = self.m_array[_indP].summc + self.m_array[_indC].change - self.m_array[_indF].change
            self.m_array[_indC].power = (self.m_array[_indC].change - _fdiv(self.m_array[_indC].summc, float(self.m_period))) * (self.m_array[_indC].change - _fdiv(self.m_array[_indC].summc, float(self.m_period)))
            self.m_array[_indC].summp = self.m_array[_indP].summp + self.m_array[_indC].power - self.m_array[_indF].power
        else:
            self.m_array[_indC].summp = 0.0
            self.m_array[_indC].summc = self.m_array[_indC].summp
            k = 0
            while k < self.m_period and i >= k:
                self.m_array[_indC].summc += self.m_array[_indC - k].change
                k += 1
            self.m_array[_indC].power = (self.m_array[_indC].change - _fdiv(self.m_array[_indC].summc, float(self.m_period))) * (self.m_array[_indC].change - _fdiv(self.m_array[_indC].summc, float(self.m_period)))
            k = 0
            while k < self.m_period and i >= k:
                self.m_array[_indC].summp += self.m_array[_indC - k].power
                k += 1
        if (i > 0 and self.m_filter > 0) and self.m_array[_indC].change < (self.m_filter * MathSqrt(_fdiv(self.m_array[_indC].summp, float(self.m_period)))):
            self.m_array[_indC].value = self.m_array[_indP].value
        return self.m_array[_indC].value

class sFilterArrayStruct(MqlObject):
    _q_fields = ('value', 'change', 'power', 'summc', 'summp')
    def __init__(self, *args):
        self.value = 0.0
        self.change = 0.0
        self.power = 0.0
        self.summc = 0.0
        self.summp = 0.0

def OnInit():
    global _fullSize, _halfSize, _halfSizem
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    _fullSize = MathMax(inpPeriod, 2)
    _halfSize = MathMax(_idiv(_fullSize, 2), 1)
    _halfSizem = ((_halfSize - 1) if (_halfSize > 1) else 1)
    iFilter.init(inpPeriod, inpFilter)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Frama (Ehlers) (' + _str(_fullSize) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_alpha, _s_OnCalculate_hh_curr, _s_OnCalculate_hh_prev, _s_OnCalculate_ll_curr, _s_OnCalculate_ll_prev, _s_OnCalculate_n1, _s_OnCalculate_n2, _s_OnCalculate_n3, _s_OnCalculate_prev_i, _s_OnCalculate_save_n1, _s_OnCalculate_save_n2, _s_OnCalculate_save_n3
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
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = 0
            if inpHlMode == hl_useHighLow:
                start = i - _fullSize + 1
                if start < 0:
                    start = 0
                _s_OnCalculate_hh_prev = high[ArrayMaximum(high, start, _halfSize)]
                _s_OnCalculate_ll_prev = low[ArrayMinimum(low, start, _halfSize)]
                start = i - _halfSize + 1
                if start < 0:
                    start = 0
                _s_OnCalculate_hh_curr = high[ArrayMaximum(high, start, _halfSizem)]
                _s_OnCalculate_ll_curr = low[ArrayMinimum(low, start, _halfSizem)]
            else:
                start = i - _fullSize + 1
                if start < 0:
                    start = 0
                _s_OnCalculate_hh_prev = prices[ArrayMaximum(prices, start, _halfSize)]
                _s_OnCalculate_ll_prev = prices[ArrayMinimum(prices, start, _halfSize)]
                start = i - _halfSize + 1
                if start < 0:
                    start = 0
                _s_OnCalculate_hh_curr = prices[ArrayMaximum(prices, start, _halfSizem)]
                _s_OnCalculate_ll_curr = prices[ArrayMinimum(prices, start, _halfSizem)]
            _s_OnCalculate_n1 = _fdiv(_s_OnCalculate_hh_prev - _s_OnCalculate_ll_prev, float(_halfSize))
        hh = MathMax((high[i] if (inpHlMode == hl_useHighLow) else prices[i]), _s_OnCalculate_hh_curr)
        ll = MathMin((low[i] if (inpHlMode == hl_useHighLow) else prices[i]), _s_OnCalculate_ll_curr)
        _s_OnCalculate_n2 = _fdiv(hh - ll, float(_halfSize))
        if _s_OnCalculate_hh_prev > hh:
            hh = _s_OnCalculate_hh_prev
        if _s_OnCalculate_ll_prev < ll:
            ll = _s_OnCalculate_ll_prev
        _s_OnCalculate_n3 = _fdiv(hh - ll, float(_fullSize))
        if (_s_OnCalculate_save_n1 != _s_OnCalculate_n1 or _s_OnCalculate_save_n2 != _s_OnCalculate_n2) or _s_OnCalculate_save_n3 != _s_OnCalculate_n3:
            _s_OnCalculate_save_n1 = _s_OnCalculate_n1
            _s_OnCalculate_save_n2 = _s_OnCalculate_n2
            _s_OnCalculate_save_n3 = _s_OnCalculate_n3
            dimen = (MathLog(_s_OnCalculate_n1 + _s_OnCalculate_n2) - MathLog(_s_OnCalculate_n3)) / M_LN2
            _s_OnCalculate_alpha = MathMin(MathMax(MathExp(-4.6 * (dimen - 1.0)), DBL_MIN), 1.0)
        _frama = (((_s_OnCalculate_alpha * prices[i]) + ((1.0 - _s_OnCalculate_alpha) * val[i - 1])) if (i > 0) else prices[i])
        val[i] = iFilter.calculate(_frama, i)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iFilter = _alloc(CFilter)
iFilter.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_hh_prev = 0.0
_s_OnCalculate_ll_prev = 0.0
_s_OnCalculate_hh_curr = 0.0
_s_OnCalculate_ll_curr = 0.0
_s_OnCalculate_save_n1 = 0.0
_s_OnCalculate_save_n2 = 0.0
_s_OnCalculate_save_n3 = 0.0
_s_OnCalculate_n1 = 0.0
_s_OnCalculate_n2 = 0.0
_s_OnCalculate_n3 = 0.0
_s_OnCalculate_alpha = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FramaFiltered(_MQL5Indicator):
    name = 'Frama (filtered)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 30,  # Frama period
        'inpFilter': 1.0,  # Filter size
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpHlMode': _Choice({0: 'Use high/lows for extremes', 1: 'Use selected price for extremes'}, default=0),  # High/low mode
    }

