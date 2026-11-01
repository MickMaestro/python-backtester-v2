"""Cercos_Chaos_vs_Movement — converted from MQL5: MQL5 Indicators/Cercós Chaos vs Movement/Cercos_Chaos_vs_Movement.mq5

Copyright: Copyright 2021, Manuel Alejandro Cercós Pérez; Link: https://www.mql5.com/en/users/alexcercos; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Manuel Alejandro Cercós Pérez', 'link': 'https://www.mql5.com/en/users/alexcercos', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Move', 2: 'Chaos'}, 'levels': [], 'description': [], 'name': 'Cercos_Chaos_vs_Movement', 'source': 'MQL5 Indicators/Cercós Chaos vs Movement/Cercos_Chaos_vs_Movement.mq5', 'folder': 'Cercós Chaos vs Movement', 'inputs': [{'mql': 'Inp_period', 'py': 'Inp_period', 'param': 'Inp_period', 'type': 'int', 'default': 6, 'label': 'Period', 'sinput': False}, {'mql': 'Inp_chaosStrength', 'py': 'Inp_chaosStrength', 'param': 'Inp_chaosStrength', 'type': 'double', 'default': 2.0, 'label': 'Chaos Strength', 'sinput': False}, {'mql': 'Inp_chaosWidth', 'py': 'Inp_chaosWidth', 'param': 'Inp_chaosWidth', 'type': 'double', 'default': 1.5, 'label': 'Chaos Width', 'sinput': False}, {'mql': 'Inp_moveStrength', 'py': 'Inp_moveStrength', 'param': 'Inp_moveStrength', 'type': 'double', 'default': 1.0, 'label': 'Movement Strength', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_period = _input('Inp_period', 6)  # Period
Inp_chaosStrength = _input('Inp_chaosStrength', 2.0)  # Chaos Strength
Inp_chaosWidth = _input('Inp_chaosWidth', 1.5)  # Chaos Width
Inp_moveStrength = _input('Inp_moveStrength', 1.0)  # Movement Strength
BufferMoveRes = Arr(0, 0.0)
BufferChaosRes = Arr(0, 0.0)
BufferMove = Arr(0, 0.0)
BufferChaos = Arr(0, 0.0)
BufferWicks = Arr(0, 0.0)
highOC = Arr(0, 0.0)
lowOC = Arr(0, 0.0)
highestHigh = Arr(0, 0.0)
lowestLow = Arr(0, 0.0)
period = 0
chaosStrength = 0.0
chaosWidth = 0.0
moveStrength = 0.0

def OnInit():
    global chaosStrength, chaosWidth, moveStrength, period
    period = (Inp_period if (Inp_period >= 2) else 2)
    chaosStrength = (Inp_chaosStrength if (Inp_chaosStrength > 0) else 1.0)
    chaosWidth = (Inp_chaosWidth if (Inp_chaosWidth > 0) else 1.0)
    moveStrength = (Inp_moveStrength if (Inp_moveStrength > 0) else 1.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Cercós Chaos vs Movement (' + _str(period) + ')')
    SetIndexBuffer(0, BufferMoveRes, INDICATOR_DATA)
    SetIndexBuffer(1, BufferChaosRes, INDICATOR_DATA)
    SetIndexBuffer(2, BufferWicks, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, highestHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, lowestLow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, highOC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, lowOC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMove, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferChaos, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BufferMoveRes, True)
    ArraySetAsSeries(BufferChaosRes, True)
    ArraySetAsSeries(BufferWicks, True)
    ArraySetAsSeries(highestHigh, True)
    ArraySetAsSeries(lowestLow, True)
    ArraySetAsSeries(highOC, True)
    ArraySetAsSeries(lowOC, True)
    ArraySetAsSeries(BufferMove, True)
    ArraySetAsSeries(BufferChaos, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = MathMin(rates_total - prev_calculated, rates_total - 1)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    for i in range(limit, 0 - 1, -1):
        BufferWicks[i] = high[i] - low[i] - MathAbs(open[i] - close[i])
        highOC[i] = MathMax(close[i], open[i])
        lowOC[i] = MathMin(close[i], open[i])
    limit = MathMin(rates_total - prev_calculated, rates_total - period)
    if limit > 1:
        ArrayInitialize(BufferMoveRes, EMPTY_VALUE)
        ArrayInitialize(BufferChaosRes, EMPTY_VALUE)
        ArrayInitialize(BufferMove, EMPTY_VALUE)
        ArrayInitialize(BufferChaos, EMPTY_VALUE)
        ArrayInitialize(highestHigh, EMPTY_VALUE)
        ArrayInitialize(lowestLow, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        if highestHigh[i + 1] == EMPTY_VALUE:
            highestHigh[i] = ArrayMaximum(highOC, i, period) - i
            lowestLow[i] = ArrayMinimum(lowOC, i, period) - i
        else:
            if (highestHigh[i + 1] + 1) >= period:
                highestHigh[i] = ArrayMaximum(highOC, i, period) - i
            else:
                highestHigh[i] = ((highestHigh[i + 1] + 1) if (highOC[_int(highestHigh[i + 1]) + i + 1] > highOC[i]) else 0)
            if (lowestLow[i + 1] + 1) >= period:
                lowestLow[i] = ArrayMinimum(lowOC, i, period) - i
            else:
                lowestLow[i] = ((lowestLow[i + 1] + 1) if (lowOC[_int(lowestLow[i + 1]) + i + 1] < lowOC[i]) else 0)
        if BufferMove[i + 1] == EMPTY_VALUE:
            BufferMove[i] = 0.0
            for j in range(i, i + period):
                BufferMove[i] += highOC[j] - lowOC[j]
        else:
            BufferMove[i] = BufferMove[i + 1] + (highOC[i] - lowOC[i]) - (highOC[i + period] - lowOC[i + period])
        if BufferChaos[i + 1] == EMPTY_VALUE:
            BufferChaos[i] = 0.0
            for j in range(i, i + period):
                BufferChaos[i] += BufferWicks[j]
        else:
            BufferChaos[i] = BufferChaos[i + 1] - BufferWicks[i + period] + BufferWicks[i]
        totalMove = highOC[_int(highestHigh[i]) + i] - lowOC[_int(lowestLow[i]) + i]
        if totalMove == 0.0:
            BufferMoveRes[i] = 0.0
            BufferChaosRes[i] = 1.0
        else:
            if BufferMove[i] != 0.0:
                BufferMoveRes[i] = MathPow(MathMin(_fdiv(totalMove, BufferMove[i]), 1.0), _fdiv(1.0, moveStrength))
            else:
                BufferMoveRes[i] = 1.0
            BufferChaosRes[i] = MathPow(Sigmoid(_fdiv(BufferChaos[i], chaosWidth * totalMove)), chaosStrength)
    return rates_total

def Sigmoid(num, zeroLimit=False):
    expP = MathExp(num)
    expN = MathExp(-num)
    if expN == 0:
        return 1.0
    res = _fdiv(expP - expN, expP + expN)
    if zeroLimit:
        return (res + 1.0) / 2.0
    else:
        return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CercosChaosVsMovement(_MQL5Indicator):
    name = 'Cercos_Chaos_vs_Movement'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_period': 6,  # Period
        'Inp_chaosStrength': 2.0,  # Chaos Strength
        'Inp_chaosWidth': 1.5,  # Chaos Width
        'Inp_moveStrength': 1.0,  # Movement Strength
    }

