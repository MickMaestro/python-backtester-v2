"""Trend direction and force - DSEMA smoothed — converted from MQL5: MQL5 Indicators/Trend direction and force - DSEMA smoothed/Trend direction and force - DSEMA smoothed.mq5

Trend direction and force
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 6333684, 16760576]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Trend direction and force'}, 'levels': [], 'description': ['Trend direction and force'], 'name': 'Trend direction and force - DSEMA smoothed', 'source': 'MQL5 Indicators/Trend direction and force - DSEMA smoothed/Trend direction and force - DSEMA smoothed.mq5', 'folder': 'Trend direction and force - DSEMA smoothed', 'inputs': [{'mql': 'inpTrendPeriod', 'py': 'inpTrendPeriod', 'param': 'inpTrendPeriod', 'type': 'int', 'default': 20, 'label': 'Trend period', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'double', 'default': 3.0, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'inpTriggerUp', 'py': 'inpTriggerUp', 'param': 'inpTriggerUp', 'type': 'double', 'default': 0.05, 'label': 'Trigger up level', 'sinput': False}, {'mql': 'inpTriggerDown', 'py': 'inpTriggerDown', 'param': 'inpTriggerDown', 'type': 'double', 'default': -0.05, 'label': 'Trigger down level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpTrendPeriod = _input('inpTrendPeriod', 20)  # Trend period
inpSmooth = _input('inpSmooth', 3.0)  # Smoothing period
inpTriggerUp = _input('inpTriggerUp', 0.05)  # Trigger up level
inpTriggerDown = _input('inpTriggerDown', -0.05)  # Trigger down level
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levup = Arr(0, 0.0)
levdn = Arr(0, 0.0)
mma = Arr(0, 0.0)
smma = Arr(0, 0.0)
tdf = Arr(0, 0.0)
tdfa = Arr(0, 0.0)
val1 = Arr(0, 0.0)
ª_alpha = 0.0
ª_alpha2 = 0.0
ª_maxPeriod = 0

def OnInit():
    global ª_alpha, ª_alpha2, ª_maxPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, mma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, smma, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, tdf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, tdfa, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, val1, INDICATOR_CALCULATIONS)
    ª_alpha = _fdiv(2.0, 1.0 + inpTrendPeriod)
    ª_alpha2 = _fdiv(2.0, 1.0 + MathSqrt((inpSmooth if (inpSmooth > 1) else 1)))
    ª_maxPeriod = 3 * inpTrendPeriod
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpTriggerUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpTriggerDown)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend direction and force (' + _str(inpTrendPeriod) + ',' + _str((inpSmooth if (inpSmooth > 1) else 1)) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        mma[i] = ((mma[i - 1] + (ª_alpha * (close[i] - mma[i - 1]))) if (i > 0) else close[i])
        smma[i] = ((smma[i - 1] + (ª_alpha * (mma[i] - smma[i - 1]))) if (i > 0) else mma[i])
        impetmma = ((mma[i] - mma[i - 1]) if (i > 0) else 0)
        impetsmma = ((smma[i] - smma[i - 1]) if (i > 0) else 0)
        divma = mma[i] - smma[i]
        if divma < 0:
            divma = -divma
        averimpet = (impetmma + impetsmma) / 2.0
        tdf[i] = divma * averimpet * averimpet * averimpet
        tdfa[i] = (tdf[i] if (tdf[i] > 0) else (-tdf[i]))
        _start = i - ª_maxPeriod + 1
        if _start < 0:
            _start = 0
        _absValue = tdfa[ArrayMaximum(tdfa, _start, ª_maxPeriod)]
        _val1 = (_fdiv(tdf[i], _absValue) if (_absValue > 0) else 0)
        val1[i] = ((val1[i - 1] + (ª_alpha2 * (_val1 - val1[i - 1]))) if (i > 0) else 0)
        val[i] = ((val[i - 1] + (ª_alpha2 * (val1[i] - val[i - 1]))) if (i > 0) else 0)
        valc[i] = (2 if (val[i] > inpTriggerUp) else 1 if (val[i] < inpTriggerDown) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendDirectionAndForceDSEMASmoothed(_MQL5Indicator):
    name = 'Trend direction and force - DSEMA smoothed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTrendPeriod': 20,  # Trend period
        'inpSmooth': 3.0,  # Smoothing period
        'inpTriggerUp': 0.05,  # Trigger up level
        'inpTriggerDown': -0.05,  # Trigger down level
    }

