"""Premium stochastic — converted from MQL5: MQL5 Indicators/Premium stochastic oscillator/Premium stochastic.mq5

Premium stochastic
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [14474460, 14474460], 2: [11119017, 3329330, 32768, 6333684, 255]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Stochastic'}, 'levels': [], 'description': ['Premium stochastic'], 'name': 'Premium stochastic', 'source': 'MQL5 Indicators/Premium stochastic oscillator/Premium stochastic.mq5', 'folder': 'Premium stochastic oscillator', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Stochastic period', 'sinput': False}, {'mql': 'inpSmoothPeriod', 'py': 'inpSmoothPeriod', 'param': 'inpSmoothPeriod', 'type': 'int', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpLevel1', 'py': 'inpLevel1', 'param': 'inpLevel1', 'type': 'double', 'default': 0.9, 'label': 'Level 1', 'sinput': False}, {'mql': 'inpLevel2', 'py': 'inpLevel2', 'param': 'inpLevel2', 'type': 'double', 'default': 0.2, 'label': 'Level 2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Stochastic period
inpSmoothPeriod = _input('inpSmoothPeriod', 5)  # Smoothing period
inpLevel1 = _input('inpLevel1', 0.9)  # Level 1
inpLevel2 = _input('inpLevel2', 0.2)  # Level 2
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
ema0 = Arr(0, 0.0)
ema1 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, ema0, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ema1, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevel1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevel2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -inpLevel1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, -inpLevel2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Premium stochastic (' + _str(inpPeriod) + ',' + _str(inpSmoothPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _alpha = _fdiv(2.0, 1.0 + inpSmoothPeriod)
    _minLevel = MathMin(inpLevel1, inpLevel2)
    _maxLevel = MathMax(inpLevel1, inpLevel2)
    i = MathMax(prev_calculated - 1, 0)
    while i < rates_total:
        _start = MathMax(i - inpPeriod, 0)
        _min = low[ArrayMinimum(low, _start, inpPeriod)]
        _max = high[ArrayMaximum(high, _start, inpPeriod)]
        _sto = ((10.0 * (_fdiv(close[i] - _min, _max - _min) - 0.5)) if (_min != _max) else 0)
        ema0[i] = ((ema0[i - 1] + (_alpha * (_sto - ema0[i - 1]))) if (i > 0) else 0)
        ema1[i] = ((ema1[i - 1] + (_alpha * (ema0[i] - ema1[i - 1]))) if (i > 0) else 0)
        _exp = MathExp(ema1[i])
        val[i] = _fdiv(_exp - 1.0, _exp + 1.0)
        valc[i] = 0.0
        if val[i] > _minLevel:
            valc[i] = (2 if (val[i] > _maxLevel) else 1)
        if val[i] < (-_minLevel):
            valc[i] = (4 if (val[i] < (-_maxLevel)) else 3)
        fillu[i] = val[i]
        filld[i] = (MathMin(_minLevel, val[i]) if (val[i] > 0) else MathMax(-_minLevel, val[i]) if (val[i] < 0) else val[i])
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PremiumStochastic(_MQL5Indicator):
    name = 'Premium stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Stochastic period
        'inpSmoothPeriod': 5,  # Smoothing period
        'inpLevel1': 0.9,  # Level 1
        'inpLevel2': 0.2,  # Level 2
    }

