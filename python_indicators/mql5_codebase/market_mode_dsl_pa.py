"""Market mode (dsl)(pa) — converted from MQL5: MQL5 Indicators/Phase accumulation adaptive market mode - discontinues signal lines/Market mode (dsl)(pa).mq5

Phase accumumation adaptive market mode
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [12632256, 7451452, 17919]}, 'widths': {3: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Phase accumumation adaptive market mode'], 'name': 'Market mode (dsl)(pa)', 'source': 'MQL5 Indicators/Phase accumulation adaptive market mode - discontinues signal lines/Market mode (dsl)(pa).mq5', 'folder': 'Phase accumulation adaptive market mode - discontinues signal lines', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Base period', 'sinput': False}, {'mql': 'inpCyclesPeriod', 'py': 'inpCyclesPeriod', 'param': 'inpCyclesPeriod', 'type': 'double', 'default': 2.0, 'label': 'Cycles period', 'sinput': False}, {'mql': 'inpCyclesFilter', 'py': 'inpCyclesFilter', 'param': 'inpCyclesFilter', 'type': 'double', 'default': 0.0, 'label': 'Cycles filter (<=1 for no filtering)', 'sinput': False}, {'mql': 'inpLevels', 'py': 'inpLevels', 'param': 'inpLevels', 'type': 'int', 'default': 10, 'label': 'Levels period', 'sinput': False}, {'mql': 'inpDelta', 'py': 'inpDelta', 'param': 'inpDelta', 'type': 'double', 'default': 0.5, 'label': 'Delta', 'sinput': False}, {'mql': 'inpFraction', 'py': 'inpFraction', 'param': 'inpFraction', 'type': 'double', 'default': 0.8, 'label': 'Fraction', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Base period
inpCyclesPeriod = _input('inpCyclesPeriod', 2.0)  # Cycles period
inpCyclesFilter = _input('inpCyclesFilter', 0.0)  # Cycles filter (<=1 for no filtering)
inpLevels = _input('inpLevels', 10)  # Levels period
inpDelta = _input('inpDelta', 0.5)  # Delta
inpFraction = _input('inpFraction', 0.8)  # Fraction
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
mode = Arr(0, 0.0)
modec = Arr(0, 0.0)
fractionUp = Arr(0, 0.0)
fractionDn = Arr(0, 0.0)
g_alpha = 0.0
g_alphal = 0.0
g_beta = 0.0
g_cycleFilter = 0.0
g_dPeriod = 0

class sMarketModeStruct(MqlObject):
    _q_fields = ('price', 'bandpass', 'sumbp', 'apeak', 'avaley')
    def __init__(self, *args):
        self.price = 0.0
        self.bandpass = 0.0
        self.sumbp = 0.0
        self.apeak = 0.0
        self.avaley = 0.0

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
    global g_alphal, g_cycleFilter, g_dPeriod
    SetIndexBuffer(0, fractionUp)
    SetIndexBuffer(1, fractionDn)
    SetIndexBuffer(2, mode)
    SetIndexBuffer(3, modec, INDICATOR_COLOR_INDEX)
    g_cycleFilter = _fdiv(2.0, 1.0 + (inpCyclesFilter if (inpCyclesFilter > 1) else 1))
    g_alphal = _fdiv(2.0, 1.0 + inpLevels)
    g_dPeriod = 2 * inpPeriod
    IndicatorSetString(INDICATOR_SHORTNAME, 'PA adaptive Market mode (' + _str(inpPeriod) + ',' + _str(inpLevels) + ',' + _str(inpDelta) + ',' + _str(inpFraction) + ')')
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
        if i > g_dPeriod:
            _s_OnCalculate_m_array[i].sumbp = _s_OnCalculate_m_array[i - 1].sumbp + _s_OnCalculate_m_array[i].bandpass - _s_OnCalculate_m_array[i - g_dPeriod].bandpass
        else:
            _s_OnCalculate_m_array[i].sumbp = _s_OnCalculate_m_array[i].bandpass
            k = 1
            while k < g_dPeriod and i >= k:
                _s_OnCalculate_m_array[i].sumbp += _s_OnCalculate_m_array[i - k].bandpass
                k += 1
        mode[i] = _fdiv(_s_OnCalculate_m_array[i].sumbp, float(g_dPeriod))
        if i > 0:
            _s_OnCalculate_m_array[i].apeak = _s_OnCalculate_m_array[i - 1].apeak
            if mode[i] > 0:
                _s_OnCalculate_m_array[i].apeak = _s_OnCalculate_m_array[i - 1].apeak + (g_alphal * (mode[i] - _s_OnCalculate_m_array[i - 1].apeak))
            _s_OnCalculate_m_array[i].avaley = _s_OnCalculate_m_array[i - 1].avaley
            if mode[i] < 0:
                _s_OnCalculate_m_array[i].avaley = _s_OnCalculate_m_array[i - 1].avaley + (g_alphal * (mode[i] - _s_OnCalculate_m_array[i - 1].avaley))
        else:
            _s_OnCalculate_m_array[i].avaley = mode[i]
            _s_OnCalculate_m_array[i].apeak = _s_OnCalculate_m_array[i].avaley
        fractionUp[i] = inpFraction * _s_OnCalculate_m_array[i].apeak
        fractionDn[i] = inpFraction * _s_OnCalculate_m_array[i].avaley
        modec[i] = (1 if (mode[i] > fractionUp[i]) else 2 if (mode[i] < fractionDn[i]) else 0)
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
_s_OnCalculate_m_array = Arr(0, 0, factory=sMarketModeStruct)
_s_OnCalculate_m_arraySize = -1
_s_iHilbertPhase_m_array = Arr(0, 0, factory=iHilbertPhaseStruct)
_s_iHilbertPhase_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MarketModeDslPa(_MQL5Indicator):
    name = 'Market mode (dsl)(pa)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPeriod': 20,  # Base period
        'inpCyclesPeriod': 2.0,  # Cycles period
        'inpCyclesFilter': 0.0,  # Cycles filter (<=1 for no filtering)
        'inpLevels': 10,  # Levels period
        'inpDelta': 0.5,  # Delta
        'inpFraction': 0.8,  # Fraction
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

