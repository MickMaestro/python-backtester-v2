"""Correlation phasor — converted from MQL5: MQL5 Indicators/Correlation phasor/Correlation phasor.mq5

Copyright: copyright© mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'copyright© mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 8}, 'colors': {1: [9498256, 42495], 2: [7451452, 17919]}, 'widths': {2: 2}, 'styles': {}, 'labels': {1: 'Trend', 2: 'Phasor'}, 'levels': [], 'description': [], 'name': 'Correlation phasor', 'source': 'MQL5 Indicators/Correlation phasor/Correlation phasor.mq5', 'folder': 'Correlation phasor', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 35, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 35)  # Period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
tcos = Arr(0, 0.0)
tsin = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    ArrayResize(tcos, inpPeriod)
    for i in range(0, inpPeriod):
        tcos[i] = MathCos((i * 2 * M_PI) / float(inpPeriod))
    ArrayResize(tsin, inpPeriod)
    for i in range(0, inpPeriod):
        tsin[i] = -MathSin((i * 2 * M_PI) / float(inpPeriod))
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Correlation phasor (%i)', inpPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    for i in range(limit, rates_total):
        filld[i] = 0.0
        val[i] = filld[i]
        real = 0.0
        imag = 0.0
        cSx = 0.0
        sSx = 0.0
        cSy = 0.0
        sSy = 0.0
        cSxx = 0.0
        sSxx = 0.0
        cSxy = 0.0
        sSxy = 0.0
        cSyy = 0.0
        sSyy = 0.0
        k = 0
        while k < inpPeriod and i >= k:
            X = close[i - k]
            cY = tcos[k]
            sY = tsin[k]
            cSx = cSx + X
            cSy = cSy + cY
            cSxx = cSxx + (X * X)
            cSxy = cSxy + (X * cY)
            cSyy = cSyy + (cY * cY)
            sSx = sSx + X
            sSy = sSy + cY
            sSxx = sSxx + (X * X)
            sSxy = sSxy + (X * sY)
            sSyy = sSyy + (sY * sY)
            k += 1
        if ((inpPeriod * cSxx) - (cSx * cSx)) > 0 and ((inpPeriod * cSyy) - (cSy * cSy)) > 0:
            real = _fdiv((inpPeriod * cSxy) - (cSx * cSy), MathSqrt(((inpPeriod * cSxx) - (cSx * cSx)) * ((inpPeriod * cSyy) - (cSy * cSy))))
        if ((inpPeriod * sSxx) - (sSx * sSx)) > 0 and ((inpPeriod * sSyy) - (sSy * sSy)) > 0:
            imag = _fdiv((inpPeriod * sSxy) - (sSx * sSy), MathSqrt(((inpPeriod * sSxx) - (sSx * sSx)) * ((inpPeriod * sSyy) - (sSy * sSy))))
        if imag != 0:
            val[i] = 90.0 + (90.0 * MathArctan(_fdiv(real, imag)))
        if imag > 0:
            val[i] = val[i] - 180.0
        if i > 0 and ((val[i - 1] - val[i]) < 270 and val[i] < val[i - 1]):
            val[i] = val[i - 1]
        fillu[i] = val[i]
        valc[i] = (0 if (val[i] > 0) else 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrelationPhasor(_MQL5Indicator):
    name = 'Correlation phasor'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 35,  # Period
    }

