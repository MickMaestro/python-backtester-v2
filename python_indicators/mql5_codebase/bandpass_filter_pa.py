"""Bandpass filter (pa) — converted from MQL5: MQL5 Indicators/Phase accumulation adaptive bandpass filter/Bandpass filter (pa).mq5

Phase accumulation adaptive Bandpass filter
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Phase accumulation adaptive Bandpass filter'], 'name': 'Bandpass filter (pa)', 'source': 'MQL5 Indicators/Phase accumulation adaptive bandpass filter/Bandpass filter (pa).mq5', 'folder': 'Phase accumulation adaptive bandpass filter', 'inputs': [{'mql': 'inpCyclesPeriod', 'py': 'inpCyclesPeriod', 'param': 'inpCyclesPeriod', 'type': 'double', 'default': 2.0, 'label': 'Cycles period', 'sinput': False}, {'mql': 'inpCyclesFilter', 'py': 'inpCyclesFilter', 'param': 'inpCyclesFilter', 'type': 'double', 'default': 0.0, 'label': 'Cycles filter (<=1 for no filtering)', 'sinput': False}, {'mql': 'inpDelta', 'py': 'inpDelta', 'param': 'inpDelta', 'type': 'double', 'default': 0.5, 'label': 'Delta', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpCyclesPeriod = _input('inpCyclesPeriod', 2.0)  # Cycles period
inpCyclesFilter = _input('inpCyclesFilter', 0.0)  # Cycles filter (<=1 for no filtering)
inpDelta = _input('inpDelta', 0.5)  # Delta
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
g_alpha = 0.0
g_alphal = 0.0
g_beta = 0.0
g_cycleFilter = 0.0

class sBandPassStruct(MqlObject):
    _q_fields = ('price', 'bandpass')
    def __init__(self, *args):
        self.price = 0.0
        self.bandpass = 0.0

class iHilbertPhaseStruct(MqlObject):
    _q_fields = ('price', 'smooth', 'detrender', 'period', 'phase', 'deltaPhase', 'Q1', 'I1')
    def __init__(self, *args):
        self.price = 0.0
        self.smooth = 0.0
        self.detrender = 0.0
        self.period = 0.0
        self.phase = 0.0
        self.deltaPhase = 0.0
        self.Q1 = 0.0
        self.I1 = 0.0

def OnInit():
    global g_cycleFilter
    SetIndexBuffer(0, val)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    g_cycleFilter = _fdiv(2.0, 1.0 + (inpCyclesFilter if (inpCyclesFilter > 1) else 1))
    IndicatorSetString(INDICATOR_SHORTNAME, 'PA adaptive Bandpass filter (' + _str(inpCyclesPeriod) + ',' + _str(inpDelta) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize, g_alpha, g_beta
    if _s_OnCalculate_m_arraySize < rates_total:
        _s_OnCalculate_m_arraySize = ArrayResize(_s_OnCalculate_m_array, rates_total + 500)
        if _s_OnCalculate_m_arraySize < rates_total:
            return 0
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _s_OnCalculate_m_array[i].price = close[i]
        elif _sw1 == PRICE_OPEN:
            _s_OnCalculate_m_array[i].price = open[i]
        elif _sw1 == PRICE_HIGH:
            _s_OnCalculate_m_array[i].price = high[i]
        elif _sw1 == PRICE_LOW:
            _s_OnCalculate_m_array[i].price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _s_OnCalculate_m_array[i].price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _s_OnCalculate_m_array[i].price = 0.0
        _phasePeriod = iHilbertPhase(_s_OnCalculate_m_array[i].price, g_cycleFilter, inpCyclesPeriod, i, rates_total)
        gamma = _fdiv(1.0, MathCos(_fdiv(4.0 * M_PI * inpDelta, _phasePeriod)))
        g_beta = MathCos(_fdiv(2.0 * M_PI, _phasePeriod))
        g_alpha = gamma - MathSqrt((gamma * gamma) - 1.0)
        _s_OnCalculate_m_array[i].bandpass = (((0.5 * (1.0 - g_alpha) * (_s_OnCalculate_m_array[i].price - _s_OnCalculate_m_array[i - 2].price)) + (g_beta * (1.0 + g_alpha) * _s_OnCalculate_m_array[i - 1].bandpass) - (g_alpha * _s_OnCalculate_m_array[i - 2].bandpass)) if (i > 1) else _s_OnCalculate_m_array[i].price)
        val[i] = _s_OnCalculate_m_array[i].bandpass
        valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        i += 1
    return i

def iHilbertPhase(price, filter_, cyclesToReach, i, bars):
    global _s_iHilbertPhase_m_arraySize
    if _s_iHilbertPhase_m_arraySize < bars:
        _s_iHilbertPhase_m_arraySize = ArrayResize(_s_iHilbertPhase_m_array, bars + 500)
        if _s_iHilbertPhase_m_arraySize < bars:
            return price
    _s_iHilbertPhase_m_array[i].price = price
    if i < 6:
        _s_iHilbertPhase_m_array[i].period = 1.0
        _s_iHilbertPhase_m_array[i].deltaPhase = 7.0
        _s_iHilbertPhase_m_array[i].I1 = price
        _s_iHilbertPhase_m_array[i].Q1 = _s_iHilbertPhase_m_array[i].I1
        _s_iHilbertPhase_m_array[i].smooth = _s_iHilbertPhase_m_array[i].Q1
        return 1.0
    cyclesToReach *= 360.0
    _s_iHilbertPhase_m_array[i].smooth = ((4.0 * _s_iHilbertPhase_m_array[i].price) + (3.0 * _s_iHilbertPhase_m_array[i - 1].price) + (2.0 * _s_iHilbertPhase_m_array[i - 2].price) + _s_iHilbertPhase_m_array[i - 3].price) / 10.0
    _s_iHilbertPhase_m_array[i].detrender = ((0.0962 * _s_iHilbertPhase_m_array[i].smooth) + (0.5769 * _s_iHilbertPhase_m_array[i - 2].smooth) - (0.5769 * _s_iHilbertPhase_m_array[i - 4].smooth) - (0.0962 * _s_iHilbertPhase_m_array[i - 6].smooth)) * ((0.075 * _s_iHilbertPhase_m_array[i - 1].period) + 0.54)
    _s_iHilbertPhase_m_array[i].Q1 = (0.15 * (((0.0962 * _s_iHilbertPhase_m_array[i].detrender) + (0.5769 * _s_iHilbertPhase_m_array[i - 2].detrender) - (0.5769 * _s_iHilbertPhase_m_array[i - 4].detrender) - (0.0962 * _s_iHilbertPhase_m_array[i - 6].detrender)) * ((0.075 * _s_iHilbertPhase_m_array[i - 1].period) + 0.54))) + (0.85 * _s_iHilbertPhase_m_array[i - 1].Q1)
    _s_iHilbertPhase_m_array[i].I1 = (0.15 * _s_iHilbertPhase_m_array[i - 3].detrender) + (0.85 * _s_iHilbertPhase_m_array[i - 1].I1)
    _s_iHilbertPhase_m_array[i].phase = (((180.0 / M_PI) * MathArctan(MathAbs(_fdiv(_s_iHilbertPhase_m_array[i].Q1, _s_iHilbertPhase_m_array[i].I1)))) if (_s_iHilbertPhase_m_array[i].I1 != 0) else _s_iHilbertPhase_m_array[i - 1].phase)
    if _s_iHilbertPhase_m_array[i].I1 < 0 and _s_iHilbertPhase_m_array[i].Q1 > 0:
        _s_iHilbertPhase_m_array[i].phase = 180.0 - _s_iHilbertPhase_m_array[i].phase
    if _s_iHilbertPhase_m_array[i].I1 < 0 and _s_iHilbertPhase_m_array[i].Q1 < 0:
        _s_iHilbertPhase_m_array[i].phase = 180.0 + _s_iHilbertPhase_m_array[i].phase
    if _s_iHilbertPhase_m_array[i].I1 > 0 and _s_iHilbertPhase_m_array[i].Q1 < 0:
        _s_iHilbertPhase_m_array[i].phase = 360.0 - _s_iHilbertPhase_m_array[i].phase
    _s_iHilbertPhase_m_array[i].deltaPhase = _s_iHilbertPhase_m_array[i - 1].phase - _s_iHilbertPhase_m_array[i].phase
    if _s_iHilbertPhase_m_array[i - 1].phase < 90.0 and _s_iHilbertPhase_m_array[i].phase > 270.0:
        _s_iHilbertPhase_m_array[i].deltaPhase = 360.0 + _s_iHilbertPhase_m_array[i - 1].phase - _s_iHilbertPhase_m_array[i].phase
    if _s_iHilbertPhase_m_array[i].deltaPhase > 60.0:
        _s_iHilbertPhase_m_array[i].deltaPhase = 60.0
    if _s_iHilbertPhase_m_array[i].deltaPhase < 7.0:
        _s_iHilbertPhase_m_array[i].deltaPhase = 7.0
    phaseSum = _s_iHilbertPhase_m_array[i].deltaPhase
    k = 1
    while phaseSum < cyclesToReach and i >= k:
        phaseSum += _s_iHilbertPhase_m_array[i - k].deltaPhase
        k += 1
    _s_iHilbertPhase_m_array[i].period = _s_iHilbertPhase_m_array[i - 1].period + (filter_ * (k - _s_iHilbertPhase_m_array[i - 1].period))
    return _s_iHilbertPhase_m_array[i].period

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sBandPassStruct)
_s_OnCalculate_m_arraySize = -1
_s_iHilbertPhase_m_array = Arr(0, 0, factory=iHilbertPhaseStruct)
_s_iHilbertPhase_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BandpassFilterPa(_MQL5Indicator):
    name = 'Bandpass filter (pa)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpCyclesPeriod': 2.0,  # Cycles period
        'inpCyclesFilter': 0.0,  # Cycles filter (<=1 for no filtering)
        'inpDelta': 0.5,  # Delta
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

