"""CCI (double smoothed Wilders EMA)(fl) — converted from MQL5: MQL5 Indicators/CCI - double smoothed Wilder's EMA filtered with floating levels/CCI (double smoothed Wilders EMA)(fl).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 16760576, 8036607]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: "CCI of ds Wilder's EMA"}, 'levels': [], 'description': [], 'name': 'CCI (double smoothed Wilders EMA)(fl)', 'source': "MQL5 Indicators/CCI - double smoothed Wilder's EMA filtered with floating levels/CCI (double smoothed Wilders EMA)(fl).mq5", 'folder': "CCI - double smoothed Wilder's EMA filtered with floating levels", 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'CCI period', 'sinput': False}, {'mql': 'inpEmaPeriod', 'py': 'inpEmaPeriod', 'param': 'inpEmaPeriod', 'type': 'int', 'default': 14, 'label': "Wilder's EMA period", 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 6, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Period for finding floating levels', 'sinput': False}, {'mql': 'inpFlUp', 'py': 'inpFlUp', 'param': 'inpFlUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'inpFlDown', 'py': 'inpFlDown', 'param': 'inpFlDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum chgColor
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
_enum('chgColor', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # CCI period
inpEmaPeriod = _input('inpEmaPeriod', 14)  # Wilder's EMA period
inpPrice = _input('inpPrice', PRICE_TYPICAL)  # Price
inpFlPeriod = _input('inpFlPeriod', 25)  # Period for finding floating levels
inpFlUp = _input('inpFlUp', 90.0)  # Upper level %
inpFlDown = _input('inpFlDown', 10.0)  # Lower level %
inpColorOn = _input('inpColorOn', chg_onLevel)  # Color change on :
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
ema1 = Arr(0, 0.0)
ema2 = Arr(0, 0.0)
_alpha = 0.0

class CCci(MqlObject):
    _q_fields = ('m_work', 'm_period', 'm_period2', 'm_arraySize')
    def __init__(self):
        self.m_work = Arr(0, 0, factory=sCciWork)
        self.m_period = 0
        self.m_period2 = 0.0
        self.m_arraySize = 0
        self.m_arraySize = -1
        self.m_period = 1
    def _q_dtor(self):
        self.m_arraySize = -1
        ArrayFree(self.m_work)
    def init(self, period):
        self.m_period = period
        return
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_work, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_work[i].value = value
        self.m_work[i].value2 = value * value
        if i > self.m_period:
            self.m_work[i].summ = self.m_work[i - 1].summ + self.m_work[i].value - self.m_work[i - self.m_period].value
            self.m_work[i].summ2 = self.m_work[i - 1].summ2 + self.m_work[i].value2 - self.m_work[i - self.m_period].value2
        else:
            self.m_work[i].summ = self.m_work[i].value
            self.m_work[i].summ2 = self.m_work[i].value2
            k = 1
            while k < self.m_period and i >= k:
                self.m_work[i].summ += self.m_work[i - k].value
                self.m_work[i].summ2 += self.m_work[i - k].value2
                k += 1
        _avg = _fdiv(self.m_work[i].summ, float(self.m_period))
        _dev = MathSqrt(_fdiv(self.m_work[i].summ2 - (self.m_work[i].summ * _avg), float(self.m_period)))
        return (_fdiv(value - _avg, 0.015 * _dev) if (_dev != 0) else 0)

class sCciWork(MqlObject):
    _q_fields = ('value', 'value2', 'summ', 'summ2')
    def __init__(self, *args):
        self.value = 0.0
        self.value2 = 0.0
        self.summ = 0.0
        self.summ2 = 0.0

def OnInit():
    global _alpha
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, ema1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ema2, INDICATOR_CALCULATIONS)
    _workCci.init(inpPeriod)
    _alpha = _fdiv(1.0, MathSqrt((inpPeriod if (inpPeriod > 1) else 1)))
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI std based (' + _str(inpPeriod) + ")(ds Wilder's EMA " + _str(inpEmaPeriod) + ' smoothed)')
    return INIT_SUCCEEDED

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
        if i > 0:
            ema1[i] = ema1[i - 1] + (_alpha * (_price - ema1[i - 1]))
            ema2[i] = ema2[i - 1] + (_alpha * (ema1[i] - ema2[i - 1]))
        else:
            ema2[i] = _price
            ema1[i] = ema2[i]
        val[i] = _workCci.calculate(ema2[i], i, rates_total)
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
        levu[i] = min_ + (inpFlUp * range_)
        levd[i] = min_ + (inpFlDown * range_)
        levm[i] = min_ + (50.0 * range_)
        _sw2 = inpColorOn
        if _sw2 == chg_onLevel:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        elif _sw2 == chg_onMiddle:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return rates_total

# ---- global variables initialised from expressions
_workCci = _alloc(CCci)
_workCci.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIDoubleSmoothedWildersEMAFl(_MQL5Indicator):
    name = 'CCI (double smoothed Wilders EMA)(fl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # CCI period
        'inpEmaPeriod': 14,  # Wilder's EMA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Price
        'inpFlPeriod': 25,  # Period for finding floating levels
        'inpFlUp': 90.0,  # Upper level %
        'inpFlDown': 10.0,  # Lower level %
        'inpColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color change on :
    }

