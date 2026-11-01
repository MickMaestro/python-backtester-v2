"""AMA (filtered - histo) — converted from MQL5: MQL5 Indicators/Adaptive Moving Average - AMA - with filter, histogram version/AMA (filtered - histo).mq5

AMA filtered
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [11119017, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'AMA'}, 'levels': [], 'description': ['AMA filtered'], 'name': 'AMA (filtered - histo)', 'source': 'MQL5 Indicators/Adaptive Moving Average - AMA - with filter, histogram version/AMA (filtered - histo).mq5', 'folder': 'Adaptive Moving Average - AMA - with filter, histogram version', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 2, 'label': 'Fast end period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 30, 'label': 'Slow end period', 'sinput': False}, {'mql': 'inpFilter', 'py': 'inpFilter', 'param': 'inpFilter', 'type': 'double', 'default': 1.5, 'label': 'Filter size (<=0 for no filter)', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpFastPeriod = _input('inpFastPeriod', 2)  # Fast end period
inpSlowPeriod = _input('inpSlowPeriod', 30)  # Slow end period
inpFilter = _input('inpFilter', 1.5)  # Filter size (<=0 for no filter)
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ama = Arr(0, 0.0)
amaf = Arr(0, 0.0)
g_fastEnd = 0.0
g_slowEnd = 0.0
g_hlPeriod = 0

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
    global g_fastEnd, g_hlPeriod, g_slowEnd
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ama, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, amaf, INDICATOR_CALCULATIONS)
    g_fastEnd = _fdiv(2.0, inpFastPeriod + 1.0)
    g_slowEnd = _fdiv(2.0, inpSlowPeriod + 1.0)
    g_hlPeriod = inpPeriod + 1
    iFilter.init(inpPeriod, inpFilter)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AMA (' + _str(inpPeriod) + ')')
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
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - g_hlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = high[ArrayMaximum(high, start, g_hlPeriod - 1)]
            _s_OnCalculate_prev_min = low[ArrayMinimum(low, start, g_hlPeriod - 1)]
        max_ = (high[i] if (high[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (low[i] if (low[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        mltp = (_fdiv(_price - min_ - (max_ - _price), max_ - min_) if (max_ != min_) else 1)
        if mltp < 0:
            mltp *= -1
        ssc = (mltp * (g_fastEnd - g_slowEnd)) + g_slowEnd
        ama[i] = ((ama[i - 1] + (ssc * ssc * (_price - ama[i - 1]))) if (i > 0) else _price)
        amaf[i] = iFilter.calculate(ama[i], i)
        val[i] = 1.0
        valc[i] = ((1 if (amaf[i] > amaf[i - 1]) else 2 if (amaf[i] < amaf[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iFilter = _alloc(CFilter)
iFilter.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AMAFilteredHisto(_MQL5Indicator):
    name = 'AMA (filtered - histo)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpFastPeriod': 2,  # Fast end period
        'inpSlowPeriod': 30,  # Slow end period
        'inpFilter': 1.5,  # Filter size (<=0 for no filter)
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }
    y_range = (0.0, 1.0)

