"""iVAR — converted from MQL5: MQL5 Indicators/iVAR_HTF/iVAR.mq5

Индекс вариации
Copyright: Copyright © 2008, Ilnur; Link: http://www.metaquotes.net; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Ilnur', 'link': 'http://www.metaquotes.net', 'version': '1.20', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'iVAR'}, 'levels': [0.5], 'description': ['Индекс вариации'], 'name': 'iVAR', 'source': 'MQL5 Indicators/iVAR_HTF/iVAR.mq5', 'folder': 'iVAR_HTF', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 5, 'label': 'период индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 5)  # период индикатора
ExtLineBuffer = Arr(0, 0.0)
Num = 0
MathLogX2 = 0.0
StartBars = 0

def OnInit():
    global MathLogX2, Num, StartBars
    StartBars = _int(MathPow(2, N))
    Num = N + 1
    MathLogX2 = MathLog(2.0)
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'iVAR(', N, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    limit = 0
    ihigh = 0
    ilow = 0
    nInterval = 0
    Delta = 0.0
    Xc = 0.0
    Yc = 0.0
    Sx = 0.0
    Sy = 0.0
    Sxx = 0.0
    Sxy = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        Sxy = 0.0
        Sxx = Sxy
        Sy = Sxx
        Sx = Sy
        for iii in range(0, N + 1):
            Delta = 0.0
            nInterval = _int(MathPow(2, N - iii))
            res = MathPow(2, iii)
            kkk = 0
            while kkk < res:
                barx = bar + (nInterval * kkk)
                ihigh = ArrayMaximum(high, barx, nInterval)
                ilow = ArrayMinimum(low, barx, nInterval)
                Delta += high[ihigh] - low[ilow]
                kkk += 1
            Xc = (N - iii) * MathLogX2
            Yc = MathLog(Delta)
            Sx += Xc
            Sy += Yc
            Sxx += Xc * Xc
            Sxy += Xc * Yc
        ExtLineBuffer[bar] = _fdiv(-((Sx * Sy) - (Num * Sxy)), (Sx * Sx) - (Num * Sxx))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IVAR(_MQL5Indicator):
    name = 'iVAR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 5,  # период индикатора
    }

