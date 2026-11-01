"""Smoother momentum MACD (fl) — converted from MQL5: MQL5 Indicators/Smoother momentum MACD with floating levels/Smoother momentum MACD (fl).mq5

Smoother momentum MACD
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 7451452, 17919]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'Smoother momentum MACD'}, 'levels': [], 'description': ['Smoother momentum MACD'], 'name': 'Smoother momentum MACD (fl)', 'source': 'MQL5 Indicators/Smoother momentum MACD with floating levels/Smoother momentum MACD (fl).mq5', 'folder': 'Smoother momentum MACD with floating levels', 'inputs': [{'mql': 'inpMomPeriodFast', 'py': 'inpMomPeriodFast', 'param': 'inpMomPeriodFast', 'type': 'int', 'default': 12, 'label': 'Fast momentum period', 'sinput': False}, {'mql': 'inpMomPeriodSlow', 'py': 'inpMomPeriodSlow', 'param': 'inpMomPeriodSlow', 'type': 'int', 'default': 50, 'label': 'Slow momentum period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color change type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onMiddle = 2
cchange_onZero = 3
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onMiddle', 3: 'cchange_onZero'})

# ---- inputs and global variables
inpMomPeriodFast = _input('inpMomPeriodFast', 12)  # Fast momentum period
inpMomPeriodSlow = _input('inpMomPeriodSlow', 50)  # Slow momentum period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up %
inpFlLevelDn = _input('inpFlLevelDn', 10.0)  # Floating levels down %
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color change type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)

class cSmoothEmaMomentumCoeffs(MqlObject):
    _q_fields = ('period', 'alphaRegular', 'alphaDouble')
    def __init__(self):
        self.period = 0.0
        self.alphaRegular = 0.0
        self.alphaDouble = 0.0
        self.period = DBL_EPSILON
    def _q_dtor(self):
        pass

class sSmoothEmaMomentumArray(MqlObject):
    _q_fields = ('ema', 'ema21', 'ema22')
    def __init__(self, *args):
        self.ema = 0.0
        self.ema21 = 0.0
        self.ema22 = 0.0

def OnInit():
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoother momentum MACD (' + _str(inpMomPeriodFast) + ',' + _str(inpMomPeriodSlow) + ')(' + _str(inpFlPeriod) + ')')
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
        val[i] = iSmoothMomentum(_price, inpMomPeriodSlow, i, 0) - iSmoothMomentum(_price, inpMomPeriodFast, i, 1)
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
        levm[i] = min_ + (50 * range_)
        _sw2 = inpColorChange
        if _sw2 == cchange_onLevels:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        elif _sw2 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw2 == cchange_onMiddle:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
        elif _sw2 == cchange_onZero:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        i += 1
    return i

def iSmoothMomentum(price, period, i, instance=0):
    if _s_iSmoothMomentum_m_coeffs[instance].period != period:
        _period = (period if (period > 1) else 1)
        _s_iSmoothMomentum_m_coeffs[instance].period = period
        _s_iSmoothMomentum_m_coeffs[instance].alphaRegular = _fdiv(2.0, 1.0 + _period)
        _s_iSmoothMomentum_m_coeffs[instance].alphaDouble = _fdiv(2.0, 1.0 + MathSqrt(_period))
    _indC = _imod(i, 32)
    if i > 0:
        _indP = _indC - 1
        if _indP < 0:
            _indP += 32
        _s_iSmoothMomentum_m_array[_indC][instance].ema = _s_iSmoothMomentum_m_array[_indP][instance].ema + (_s_iSmoothMomentum_m_coeffs[instance].alphaRegular * (price - _s_iSmoothMomentum_m_array[_indP][instance].ema))
        _s_iSmoothMomentum_m_array[_indC][instance].ema21 = _s_iSmoothMomentum_m_array[_indP][instance].ema21 + (_s_iSmoothMomentum_m_coeffs[instance].alphaDouble * (price - _s_iSmoothMomentum_m_array[_indP][instance].ema21))
        _s_iSmoothMomentum_m_array[_indC][instance].ema22 = _s_iSmoothMomentum_m_array[_indP][instance].ema22 + (_s_iSmoothMomentum_m_coeffs[instance].alphaDouble * (_s_iSmoothMomentum_m_array[_indC][instance].ema21 - _s_iSmoothMomentum_m_array[_indP][instance].ema22))
    else:
        _s_iSmoothMomentum_m_array[_indC][instance].ema22 = price
        _s_iSmoothMomentum_m_array[_indC][instance].ema21 = _s_iSmoothMomentum_m_array[_indC][instance].ema22
        _s_iSmoothMomentum_m_array[_indC][instance].ema = _s_iSmoothMomentum_m_array[_indC][instance].ema21
    return _s_iSmoothMomentum_m_array[_indC][instance].ema22 - _s_iSmoothMomentum_m_array[_indC][instance].ema

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s_iSmoothMomentum_m_coeffs = Arr(2, 0, dyn=False, factory=cSmoothEmaMomentumCoeffs)
_s_iSmoothMomentum_m_array = Arr(32, 0, dyn=False, factory=sSmoothEmaMomentumArray, dims=(2,))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmootherMomentumMACDFl(_MQL5Indicator):
    name = 'Smoother momentum MACD (fl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMomPeriodFast': 12,  # Fast momentum period
        'inpMomPeriodSlow': 50,  # Slow momentum period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross', 3: 'Change color on zero cross'}, default=1),  # Color change type
    }

