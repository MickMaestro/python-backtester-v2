"""Trix (ds Wilder ema)(fl) — converted from MQL5: MQL5 Indicators/TRIX using Wilder's double smoothed EMA - floating levels/Trix (ds Wilder ema)(fl).mq5

Triple Exponential Average using double smoothed Wilder's EMA
With an addition of floating levels
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 7451452, 17919]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'RMO'}, 'levels': [], 'description': ["Triple Exponential Average using double smoothed Wilder's EMA", 'With an addition of floating levels'], 'name': 'Trix (ds Wilder ema)(fl)', 'source': "MQL5 Indicators/TRIX using Wilder's double smoothed EMA - floating levels/Trix (ds Wilder ema)(fl).mq5", 'folder': "TRIX using Wilder's double smoothed EMA - floating levels", 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'TRIX period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # TRIX period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up %
inpFlLevelDn = _input('inpFlLevelDn', 10.0)  # Floating levels down %
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color changing mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
prices = Arr(0, 0.0)

class CTrixDsWilders(MqlObject):
    _q_fields = ('m_period', 'm_alpha', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0.0
        self.m_alpha = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sTrixDsWildersStruct)
        self.m_arraySize = -1
        self.m_alpha = 1.0
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_alpha = _fdiv(2.0, 1.0 + MathSqrt(self.m_period))
        return True
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if i > 0:
            self.m_array[i].ema10 = self.m_array[i - 1].ema10 + (self.m_alpha * (price - self.m_array[i - 1].ema10))
            self.m_array[i].ema11 = self.m_array[i - 1].ema11 + (self.m_alpha * (self.m_array[i].ema10 - self.m_array[i - 1].ema11))
            self.m_array[i].ema20 = self.m_array[i - 1].ema20 + (self.m_alpha * (self.m_array[i].ema11 - self.m_array[i - 1].ema20))
            self.m_array[i].ema21 = self.m_array[i - 1].ema21 + (self.m_alpha * (self.m_array[i].ema20 - self.m_array[i - 1].ema21))
            self.m_array[i].ema30 = self.m_array[i - 1].ema30 + (self.m_alpha * (self.m_array[i].ema21 - self.m_array[i - 1].ema30))
            self.m_array[i].ema31 = self.m_array[i - 1].ema31 + (self.m_alpha * (self.m_array[i].ema30 - self.m_array[i - 1].ema31))
            return _fdiv(self.m_array[i].ema31 - self.m_array[i - 1].ema31, self.m_array[i].ema31)
        else:
            self.m_array[i].ema31 = price
            self.m_array[i].ema30 = self.m_array[i].ema31
            self.m_array[i].ema21 = self.m_array[i].ema30
            self.m_array[i].ema20 = self.m_array[i].ema21
            self.m_array[i].ema11 = self.m_array[i].ema20
            self.m_array[i].ema10 = self.m_array[i].ema11
        return 0.0

class sTrixDsWildersStruct(MqlObject):
    _q_fields = ('price', 'ema10', 'ema11', 'ema20', 'ema21', 'ema30', 'ema31')
    def __init__(self, *args):
        self.price = 0.0
        self.ema10 = 0.0
        self.ema11 = 0.0
        self.ema20 = 0.0
        self.ema21 = 0.0
        self.ema30 = 0.0
        self.ema31 = 0.0

def OnInit():
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, prices, INDICATOR_CALCULATIONS)
    iTrix.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, "TRIX (ds Wilder's ema)(" + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
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
        val[i] = iTrix.calculate(prices[i], i, rates_total)
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpFlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = val[ArrayMaximum(val, start, inpFlPeriod - 1)]
            _s_OnCalculate_prev_min = val[ArrayMinimum(val, start, inpFlPeriod - 1)]
        max_ = (val[i] if (val[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (val[i] if (val[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        levu[i] = min_ + (inpFlLevelUp * range_)
        levd[i] = min_ + (inpFlLevelDn * range_)
        levm[i] = (levu[i] + levd[i]) / 2
        _sw2 = inpColorChange
        if _sw2 == cchange_onLevels:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        elif _sw2 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw2 == cchange_onZero:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iTrix = _alloc(CTrixDsWilders)
iTrix.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrixDsWilderEmaFl(_MQL5Indicator):
    name = 'Trix (ds Wilder ema)(fl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # TRIX period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color changing mode
    }

