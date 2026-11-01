"""asi — converted from MQL5: MQL5 Indicators/Accumulation Swing Index (ASI)/asi.mq5

Accumulation Swing Index
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ASI'}, 'levels': [], 'description': ['Accumulation Swing Index'], 'name': 'asi', 'source': 'MQL5 Indicators/Accumulation Swing Index (ASI)/asi.mq5', 'folder': 'Accumulation Swing Index (ASI)', 'inputs': [{'mql': 'InpT', 'py': 'InpT', 'param': 'InpT', 'type': 'double', 'default': 300.0, 'label': 'T (maximum price changing)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpT = _input('InpT', 300.0)  # T (maximum price changing)
ExtASIBuffer = Arr(0, 0.0)
ExtSIBuffer = Arr(0, 0.0)
ExtTRBuffer = Arr(0, 0.0)
ExtTpoints = 0.0
ExtT = 0.0

def OnInit():
    global ExtT, ExtTpoints
    if fabs(InpT) > 1e-07:
        ExtT = InpT
    else:
        ExtT = 300.0
        printf('Input parameter T has wrong value. Indicator will use T = %f.', ExtT)
    SetIndexBuffer(0, ExtASIBuffer)
    SetIndexBuffer(1, ExtSIBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtTRBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    if fabs(Point()) > 1e-07:
        ExtTpoints = ExtT * Point()
    else:
        ExtTpoints = ExtT * pow(10, -Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < 2:
        return 0
    pos = 0
    pos = prev_calculated - 1
    if pos <= 0:
        pos = 1
        ExtASIBuffer[0] = 0.0
        ExtSIBuffer[0] = 0.0
        ExtTRBuffer[0] = High[0] - Low[0]
    for i in range(pos, rates_total):
        dPrevClose = Close[i - 1]
        dPrevOpen = Open[i - 1]
        dClose = Close[i]
        dHigh = High[i]
        dLow = Low[i]
        ExtTRBuffer[i] = MathMax(dHigh, dPrevClose) - MathMin(dLow, dPrevClose)
        ER = 0.0
        if not (dPrevClose >= dLow and dPrevClose <= dHigh):
            if dPrevClose > dHigh:
                ER = MathAbs(dHigh - dPrevClose)
            if dPrevClose < dLow:
                ER = MathAbs(dLow - dPrevClose)
        K = MathMax(MathAbs(dHigh - dPrevClose), MathAbs(dLow - dPrevClose))
        SH = MathAbs(dPrevClose - dPrevOpen)
        R = ExtTRBuffer[i] - (0.5 * ER) + (0.25 * SH)
        if R == 0.0 or ExtTpoints == 0.0:
            ExtSIBuffer[i] = 0.0
        else:
            ExtSIBuffer[i] = _fdiv(50 * (dClose - dPrevClose + (0.5 * (dClose - Open[i])) + (0.25 * (dPrevClose - dPrevOpen))) * _fdiv(K, ExtTpoints), R)
        ExtASIBuffer[i] = ExtASIBuffer[i - 1] + ExtSIBuffer[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Asi(_MQL5Indicator):
    name = 'asi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpT': 300.0,  # T (maximum price changing)
    }

