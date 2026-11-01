"""Frama (fl) — converted from MQL5: MQL5 Indicators/Frama - floating levels/Frama (fl).mq5

Frama (Ehlers) with floating levels
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 16760576, 8036607]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'Frama'}, 'levels': [], 'description': ['Frama (Ehlers) with floating levels'], 'name': 'Frama (fl)', 'source': 'MQL5 Indicators/Frama - floating levels/Frama (fl).mq5', 'folder': 'Frama - floating levels', 'inputs': [{'mql': 'inpFdiPeriod', 'py': 'inpFdiPeriod', 'param': 'inpFdiPeriod', 'type': 'int', 'default': 30, 'label': 'Frama period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpHlMode', 'py': 'inpHlMode', 'param': 'inpHlMode', 'type': 'int', 'default': 0, 'label': 'High/low mode', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color changing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enUseHighLow
hl_useHighLow = 0
hl_usePrices = 1
_enum('enUseHighLow', {0: 'hl_useHighLow', 1: 'hl_usePrices'})

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
inpFdiPeriod = _input('inpFdiPeriod', 30)  # Frama period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpHlMode = _input('inpHlMode', hl_useHighLow)  # High/low mode
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up %
inpFlLevelDn = _input('inpFlLevelDn', 10.0)  # Floating levels down %
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color changing method
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
prices = Arr(0, 0.0)
_fullSize = 0
_halfSize = 0
_halfSizem = 0

class cMinMax(MqlObject):
    _q_fields = ('originalPeriod', 'period', 'prevbar', 'currmin', 'currmax', 'prevmax', 'prevmin', 'minArray', 'maxArray')
    def __init__(self):
        self.originalPeriod = 0
        self.period = 0
        self.prevbar = 0
        self.currmin = 0.0
        self.currmax = 0.0
        self.prevmax = 0.0
        self.prevmin = 0.0
        self.minArray = Arr(0, 0.0)
        self.maxArray = Arr(0, 0.0)
        self.prevbar = INT_MIN
        self.originalPeriod = self.prevbar
        return
    def _q_dtor(self):
        ArrayFree(self.minArray)
        ArrayFree(self.maxArray)
        return
    def calculate(self, valueMin, valueMax, forPeriod, min_, max_, i):
        if self.prevbar != i:
            self.prevbar = i
            if self.originalPeriod != forPeriod:
                self.originalPeriod = forPeriod
                self.period = (forPeriod if (forPeriod > 0) else 1)
                self.prevmin = valueMin
                self.prevmax = valueMax
                self.currmin = valueMin
                self.currmax = valueMax
                ArrayResize(self.minArray, self.period - 1)
                ArrayInitialize(self.minArray, valueMin)
                ArrayResize(self.maxArray, self.period - 1)
                ArrayInitialize(self.maxArray, valueMax)
            if self.period > 1:
                _pos = _imod(i, self.period - 1)
                self.minArray[_pos] = self.currmin
                self.maxArray[_pos] = self.currmax
                self.prevmin = self.minArray[ArrayMinimum(self.minArray)]
                self.prevmax = self.maxArray[ArrayMaximum(self.maxArray)]
            else:
                self.prevmin = valueMin
                self.prevmax = valueMax
        self.currmin = valueMin
        self.currmax = valueMax
        max_.v = (self.prevmax if (self.prevmax > valueMax) else valueMax)
        min_.v = (self.prevmin if (self.prevmin < valueMin) else valueMin)
        return

def OnInit():
    global _fullSize, _halfSize, _halfSizem
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, prices, INDICATOR_CALCULATIONS)
    _fullSize = MathMax(inpFdiPeriod, 2)
    _halfSize = MathMax(_idiv(_fullSize, 2), 1)
    _halfSizem = ((_halfSize - 1) if (_halfSize > 1) else 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Frama (Ehlers) fl (' + _str(_fullSize) + ')')
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
        val[i] = (((_s_OnCalculate_alpha * prices[i]) + ((1.0 - _s_OnCalculate_alpha) * val[i - 1])) if (i > 0) else prices[i])
        _min = Box(0.0)
        _max = Box(0.0)
        _framaMinMax.calculate(val[i], val[i], inpFlPeriod, _min, _max, i)
        range_ = (_max.v - _min.v) / 100.0
        levu[i] = _min.v + (inpFlLevelUp * range_)
        levd[i] = _min.v + (inpFlLevelDn * range_)
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
_framaMinMax = _alloc(cMinMax)
_framaMinMax.__init__()

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


class FramaFl(_MQL5Indicator):
    name = 'Frama (fl)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFdiPeriod': 30,  # Frama period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpHlMode': _Choice({0: 'Use high/lows for extremes', 1: 'Use selected price for extremes'}, default=0),  # High/low mode
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on levels crossing', 2: 'Change color on middle level crossing'}, default=1),  # Color changing method
    }

