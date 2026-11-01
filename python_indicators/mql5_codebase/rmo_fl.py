"""RMO (fl) — converted from MQL5: MQL5 Indicators/Recursive Median Oscillator - with floating levels/RMO (fl).mq5

Recursive Median Oscillator
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 7451452, 17919]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'RMO'}, 'levels': [], 'description': ['Recursive Median Oscillator'], 'name': 'RMO (fl)', 'source': 'MQL5 Indicators/Recursive Median Oscillator - with floating levels/RMO (fl).mq5', 'folder': 'Recursive Median Oscillator - with floating levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 12, 'label': 'Low pass period', 'sinput': False}, {'mql': 'inpPeriod2', 'py': 'inpPeriod2', 'param': 'inpPeriod2', 'type': 'int', 'default': 30, 'label': 'High pass period', 'sinput': False}, {'mql': 'inpPeriod3', 'py': 'inpPeriod3', 'param': 'inpPeriod3', 'type': 'int', 'default': 5, 'label': 'Median period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 12)  # Low pass period
inpPeriod2 = _input('inpPeriod2', 30)  # High pass period
inpPeriod3 = _input('inpPeriod3', 5)  # Median period
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

class CRmo(MqlObject):
    _q_fields = ('m_lowPass_period', 'm_highPass_period', 'm_median_period', 'm_arraySize', 'm_1', 'm_2', 'm_alpha1', 'm_alpha2', 'm_sort', 'm_array')
    def __init__(self):
        self.m_lowPass_period = 0
        self.m_highPass_period = 0
        self.m_median_period = 0
        self.m_arraySize = 0
        self.m_1 = 0
        self.m_2 = 0
        self.m_alpha1 = 0.0
        self.m_alpha2 = 0.0
        self.m_sort = Arr(0, 0.0)
        self.m_array = Arr(0, 0, factory=sRmoStruct)
        self.init(1, 1, 1)
        return
    def _q_dtor(self):
        ArrayFree(self.m_array)
        ArrayFree(self.m_sort)
        return
    def init(self, lowPassPeriod, highPassPeriod, medianPeriod):
        self.m_lowPass_period = (lowPassPeriod if (lowPassPeriod > 1) else 1)
        self.m_highPass_period = (highPassPeriod if (highPassPeriod > 1) else 1)
        self.m_median_period = (medianPeriod if (medianPeriod > 1) else 1)
        self.m_alpha1 = _fdiv(MathCos(_fdiv(2 * M_PI, self.m_lowPass_period)) + MathSin(_fdiv(2 * M_PI, self.m_lowPass_period)) - 1.0, MathCos(_fdiv(2 * M_PI, self.m_lowPass_period)))
        self.m_alpha2 = _fdiv(MathCos(_fdiv(0.707 * 2 * M_PI, self.m_highPass_period)) + MathSin(_fdiv(0.707 * 2 * M_PI, self.m_highPass_period)) - 1.0, MathCos(_fdiv(0.707 * 2 * M_PI, self.m_highPass_period)))
        self.m_1 = _int(self.m_median_period / 2.0)
        self.m_2 = ((self.m_1 - 1) if ((2 * self.m_1) == self.m_median_period) else self.m_1)
        self.m_arraySize = 32
        if ArrayResize(self.m_array, self.m_arraySize) != self.m_arraySize:
            return False
        if ArrayResize(self.m_sort, self.m_median_period) != self.m_median_period:
            return False
        return True
    def calculate(self, values, i):
        _indC = _imod(i, self.m_arraySize)
        if i > 2:
            _indP = _imod(i - 1, self.m_arraySize)
            _indS = _imod(i - 2, self.m_arraySize)
            _start = i - self.m_median_period + 1
            if _start < 0:
                _start = 0
            ArrayCopy(self.m_sort, values, 0, _start, self.m_median_period)
            ArraySort(self.m_sort)
            self.m_array[_indC].rm = ((self.m_alpha1 * (self.m_sort[self.m_1] + self.m_sort[self.m_2])) / 2.0) + ((1 - self.m_alpha1) * self.m_array[_indP].rm)
            self.m_array[_indC].rmo = ((1 - (self.m_alpha2 / 2.0)) * (1 - (self.m_alpha2 / 2.0)) * (self.m_array[_indC].rm - (2.0 * self.m_array[_indP].rm) + self.m_array[_indS].rm)) + (2.0 * (1 - self.m_alpha2) * self.m_array[_indP].rmo) - ((1 - self.m_alpha2) * (1 - self.m_alpha2) * self.m_array[_indS].rmo)
        else:
            self.m_array[_indC].rmo = 0.0
            self.m_array[_indC].rm = self.m_array[_indC].rmo
        return self.m_array[_indC].rmo

class sRmoStruct(MqlObject):
    _q_fields = ('rm', 'rmo')
    def __init__(self, *args):
        self.rm = 0.0
        self.rmo = 0.0

def OnInit():
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, prices, INDICATOR_CALCULATIONS)
    iRmo.init(inpPeriod, inpPeriod2, inpPeriod3)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RMO (' + _str(inpPeriod) + ',' + _str(inpPeriod2) + ',' + _str(inpPeriod3) + ')')
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
        val[i] = iRmo.calculate(prices, i)
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
iRmo = _alloc(CRmo)
iRmo.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RMOFl(_MQL5Indicator):
    name = 'RMO (fl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 12,  # Low pass period
        'inpPeriod2': 30,  # High pass period
        'inpPeriod3': 5,  # Median period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color changing mode
    }

