"""lsma_angle — converted from MQL5: MQL5 Indicators/LSMA_Angle/lsma_angle.mq5

Copyright: Copyright © 2005, Robert L. Hill aka MrPip; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Robert L. Hill aka MrPip', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 15631086, 8421504, 16748574, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LSMA_Angle'}, 'levels': [], 'description': [], 'name': 'lsma_angle', 'source': 'MQL5 Indicators/LSMA_Angle/lsma_angle.mq5', 'folder': 'LSMA_Angle', 'inputs': [{'mql': 'LSMAPeriod', 'py': 'LSMAPeriod', 'param': 'LSMAPeriod', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'AngleTreshold', 'py': 'AngleTreshold', 'param': 'AngleTreshold', 'type': 'int', 'default': 15, 'label': 'Trigger threshold', 'sinput': False}, {'mql': 'StartLSMAShift', 'py': 'StartLSMAShift', 'param': 'StartLSMAShift', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'EndLSMAShift', 'py': 'EndLSMAShift', 'param': 'EndLSMAShift', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LSMAPeriod = _input('LSMAPeriod', 25)
AngleTreshold = _input('AngleTreshold', _int(15.0))  # Trigger threshold
StartLSMAShift = _input('StartLSMAShift', 4)
EndLSMAShift = _input('EndLSMAShift', 0)
mFactor = 0.0
dFactor = 0.0
ShiftDif = 0.0
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def LSMA(Rperiod, Close, shift):
    iii = 0
    sum_ = 0.0
    length = 0
    lengthvar = 0.0
    tmp = 0.0
    wt = 0.0
    length = Rperiod
    sum_ = 0.0
    iii = length
    for iii in range(iii, 1 - 1, -1):
        lengthvar = length + 1
        lengthvar = lengthvar / 3
        tmp = (iii - lengthvar) * Close[length - iii + shift]
        sum_ += tmp
    else:
        iii = _range_end(iii, 1 - 1, -1)
    wt = _fdiv(sum_ * 6, length * (length + 1))
    return wt

def OnInit():
    global ShiftDif, dFactor, mFactor, min_rates_total
    min_rates_total = _int(MathMax(LSMAPeriod + StartLSMAShift, LSMAPeriod + EndLSMAShift))
    dFactor = (2 * 3.14159) / 180.0
    mFactor = 100000.0
    Sym = StringSubstr(Symbol(), 3, 3)
    if Sym == 'JPY':
        mFactor = 1000.0
    ShiftDif = StartLSMAShift - EndLSMAShift
    mFactor = _fdiv(mFactor, ShiftDif)
    if EndLSMAShift >= StartLSMAShift:
        Print('Error: EndLSMAShift >= StartLSMAShift')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LSMA_Angle')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, AngleTreshold)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, -AngleTreshold)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    clr = 0
    fEndMA = 0.0
    fStartMA = 0.0
    fAngle = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        fEndMA = LSMA(LSMAPeriod, close, bar + EndLSMAShift)
        fStartMA = LSMA(LSMAPeriod, close, bar + StartLSMAShift)
        fAngle = (mFactor * (fEndMA - fStartMA)) / 2
        IndBuffer[bar] = fAngle
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if IndBuffer[bar] > AngleTreshold:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 3
        if IndBuffer[bar] < (-AngleTreshold):
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LsmaAngle(_MQL5Indicator):
    name = 'lsma_angle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LSMAPeriod': 25,
        'AngleTreshold': 15,  # Trigger threshold
        'StartLSMAShift': 4,
        'EndLSMAShift': 0,
    }

