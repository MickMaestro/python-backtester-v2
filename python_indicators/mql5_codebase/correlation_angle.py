"""Correlation angle — converted from MQL5: MQL5 Indicators/Correlation angle/Correlation angle.mq5

Copyright: copyright© mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'copyright© mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [9498256, 42495], 2: [7451452], 3: [17919]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {1: 'Trend', 2: 'Real', 3: 'Imaginary'}, 'levels': [], 'description': [], 'name': 'Correlation angle', 'source': 'MQL5 Indicators/Correlation angle/Correlation angle.mq5', 'folder': 'Correlation angle', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 35, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 35)  # Period
valr = Arr(0, 0.0)
vali = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
tcos = Arr(0, 0.0)
tsin = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valr, INDICATOR_DATA)
    SetIndexBuffer(3, vali, INDICATOR_DATA)
    ArrayResize(tcos, inpPeriod)
    for i in range(0, inpPeriod):
        tcos[i] = MathCos((i * 2 * M_PI) / float(inpPeriod))
    ArrayResize(tsin, inpPeriod)
    for i in range(0, inpPeriod):
        tsin[i] = -MathSin((i * 2 * M_PI) / float(inpPeriod))
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Correlation angle (%i)', inpPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    for i in range(limit, rates_total):
        filld[i] = 0.0
        vali[i] = filld[i]
        fillu[i] = 0.0
        valr[i] = fillu[i]
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
            fillu[i] = _fdiv((inpPeriod * cSxy) - (cSx * cSy), MathSqrt(((inpPeriod * cSxx) - (cSx * cSx)) * ((inpPeriod * cSyy) - (cSy * cSy))))
            valr[i] = fillu[i]
        if ((inpPeriod * sSxx) - (sSx * sSx)) > 0 and ((inpPeriod * sSyy) - (sSy * sSy)) > 0:
            filld[i] = _fdiv((inpPeriod * sSxy) - (sSx * sSy), MathSqrt(((inpPeriod * sSxx) - (sSx * sSx)) * ((inpPeriod * sSyy) - (sSy * sSy))))
            vali[i] = filld[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrelationAngle(_MQL5Indicator):
    name = 'Correlation angle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 35,  # Period
    }

