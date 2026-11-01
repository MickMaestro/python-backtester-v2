"""AMA to KAMA crosses (histogram) — converted from MQL5: MQL5 Indicators/AMA to KAMA crossover - histogram version/AMA to KAMA crosses (histogram).mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1, 'indicator_minimum': 0.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'AMA to KAMA state'}, 'levels': [], 'description': [], 'name': 'AMA to KAMA crosses (histogram)', 'source': 'MQL5 Indicators/AMA to KAMA crossover - histogram version/AMA to KAMA crosses (histogram).mq5', 'folder': 'AMA to KAMA crossover - histogram version', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 2, 'label': 'Fast end period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 30, 'label': 'Slow end period', 'sinput': False}, {'mql': 'inpPower', 'py': 'inpPower', 'param': 'inpPower', 'type': 'double', 'default': 2.0, 'label': 'KAMA smoothing power', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpFastPeriod = _input('inpFastPeriod', 2)  # Fast end period
inpSlowPeriod = _input('inpSlowPeriod', 30)  # Slow end period
inpPower = _input('inpPower', 2.0)  # KAMA smoothing power
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valf = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
g_fastEnd = 0.0
g_slowEnd = 0.0
g_hlPeriod = 0

class CKama(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_fastEnd', 'm_slowEnd', 'm_power', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_fastEnd = 0.0
        self.m_slowEnd = 0.0
        self.m_power = 0.0
        self.m_array = Arr(0, 0, factory=sKamaStruct)
        self.init(1, 2.0, 30.0, 2.0)
        return
    def _q_dtor(self):
        ArrayFree(self.m_array)
        return
    def init(self, period, fastEnd, slowEnd, power):
        self.m_period = (period if (period > 1) else 1)
        self.m_arraySize = self.m_period + 32
        self.m_fastEnd = _fdiv(2.0, fastEnd + 1.0)
        self.m_slowEnd = _fdiv(2.0, slowEnd + 1.0)
        self.m_power = power
        if ArrayResize(self.m_array, self.m_arraySize) != self.m_arraySize:
            return False
        return True
    def calculate(self, value, i):
        _indC = _imod(i, self.m_arraySize)
        _indP = _imod(i - 1, self.m_arraySize)
        self.m_array[_indC].price = value
        self.m_array[_indC].difference = ((value - self.m_array[_indP].price) if (i > 0) else 0)
        if self.m_array[_indC].difference < 0:
            self.m_array[_indC].difference *= -1.0
        signal = 0.0
        if i > self.m_period:
            _indF = _imod(i - self.m_period, self.m_arraySize)
            signal = value - self.m_array[_indF].price
            if signal < 0:
                signal *= -1.0
            self.m_array[_indC].noise = self.m_array[_indP].noise + self.m_array[_indC].difference - self.m_array[_indF].difference
        else:
            self.m_array[_indC].noise = self.m_array[_indC].difference
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[_indC].noise += self.m_array[i - k].difference
                k += 1
        efratio = (_fdiv(signal, self.m_array[_indC].noise) if (self.m_array[_indC].noise != 0) else 1)
        self.m_array[_indC].kama = ((self.m_array[_indP].kama + (MathPow((efratio * (self.m_fastEnd - self.m_slowEnd)) + self.m_slowEnd, self.m_power) * (value - self.m_array[_indP].kama))) if (i > 0) else value)
        return self.m_array[_indC].kama

class sKamaStruct(MqlObject):
    _q_fields = ('difference', 'noise', 'price', 'kama')
    def __init__(self, *args):
        self.difference = 0.0
        self.noise = 0.0
        self.price = 0.0
        self.kama = 0.0

def OnInit():
    global g_fastEnd, g_hlPeriod, g_slowEnd
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, valf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, vals, INDICATOR_CALCULATIONS)
    iKama.init(inpPeriod, inpFastPeriod, inpSlowPeriod, inpPower)
    g_fastEnd = _fdiv(2.0, inpFastPeriod + 1.0)
    g_slowEnd = _fdiv(2.0, inpSlowPeriod + 1.0)
    g_hlPeriod = inpPeriod + 1
    IndicatorSetString(INDICATOR_SHORTNAME, 'AMA to KAMA crosses (' + _str(inpPeriod) + ')')
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
        valf[i] = ((valf[i - 1] + (ssc * ssc * (_price - valf[i - 1]))) if (i > 0) else _price)
        vals[i] = iKama.calculate(_price, i)
        valc[i] = (1 if (valf[i] > vals[i]) else 2 if (valf[i] < vals[i]) else valc[i - 1] if (i > 0) else 0)
        val[i] = 1.0
        i += 1
    return i

# ---- global variables initialised from expressions
iKama = _alloc(CKama)
iKama.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AMAToKAMACrossesHistogram(_MQL5Indicator):
    name = 'AMA to KAMA crosses (histogram)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpFastPeriod': 2,  # Fast end period
        'inpSlowPeriod': 30,  # Slow end period
        'inpPower': 2.0,  # KAMA smoothing power
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }
    y_range = (0.0, 1.0)

