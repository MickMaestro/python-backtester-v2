"""Decycler_Oscillator — converted from MQL5: MQL5 Indicators/Decycler_Oscillator/Decycler_Oscillator.mq5

John F.Ehlers Decycler Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Decycler Osc'}, 'levels': [], 'description': ['John F.Ehlers Decycler Oscillator'], 'name': 'Decycler_Oscillator', 'source': 'MQL5 Indicators/Decycler_Oscillator/Decycler_Oscillator.mq5', 'folder': 'Decycler_Oscillator', 'inputs': [{'mql': 'InpPeriodHP', 'py': 'InpPeriodHP', 'param': 'InpPeriodHP', 'type': 'double', 'default': 125.0, 'label': 'HP period', 'sinput': False}, {'mql': 'InpCoefficient', 'py': 'InpCoefficient', 'param': 'InpCoefficient', 'type': 'double', 'default': 1.0, 'label': 'Coefficient', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodHP = _input('InpPeriodHP', 125.0)  # HP period
InpCoefficient = _input('InpCoefficient', 1.0)  # Coefficient
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferDO = Arr(0, 0.0)
BufferHP = Arr(0, 0.0)
BufferDecycle = Arr(0, 0.0)
BufferDecycleOsc = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_hp = 0.0
coefficient = 0.0
angle1 = 0.0
angle2 = 0.0
alpha1 = 0.0
alpha2 = 0.0
handle_ma = 0

def OnInit():
    global alpha1, alpha2, angle1, angle2, coefficient, handle_ma, period_hp
    period_hp = (2 if (InpPeriodHP < 2) else InpPeriodHP)
    coefficient = (Point() if (InpCoefficient == 0) else InpCoefficient)
    angle1 = _fdiv(1.414 * M_PI, period_hp)
    angle2 = 2.0 * angle1
    alpha1 = _fdiv(cos(angle1) + sin(angle1) - 1.0, cos(angle1))
    alpha2 = _fdiv(cos(angle2) + sin(angle2) - 1.0, cos(angle2))
    SetIndexBuffer(0, BufferDO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferDecycle, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferDecycleOsc, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Decycler Oscillator (' + DoubleToString(period_hp, 1) + ',' + DoubleToString(coefficient, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDO, True)
    ArraySetAsSeries(BufferHP, True)
    ArraySetAsSeries(BufferDecycle, True)
    ArraySetAsSeries(BufferDecycleOsc, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferDO, 0)
        ArrayInitialize(BufferHP, 0)
        ArrayInitialize(BufferDecycle, 0)
        ArrayInitialize(BufferDecycleOsc, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        a1 = 1.0 - alpha1
        a2 = 1.0 - (alpha1 / 2.0)
        a3 = a1 * a1
        a4 = a2 * a2
        pr2 = 2.0 * BufferMA[i + 1]
        pr3 = BufferMA[i] - pr2 + BufferMA[i + 2]
        BufferHP[i] = (a4 * pr3) + (2.0 * a1 * BufferHP[i + 1]) - (a3 * BufferHP[i + 2])
        BufferDecycle[i] = BufferMA[i] - BufferHP[i]
        b1 = 1.0 - alpha2
        b2 = 1.0 - (alpha2 / 2.0)
        b3 = b1 * b1
        b4 = b2 * b2
        pr4 = 2.0 * BufferDecycle[i + 1]
        pr5 = BufferDecycle[i] - pr4 + BufferDecycle[i + 2]
        BufferDecycleOsc[i] = (b4 * pr5) + (2.0 * b1 * BufferDecycleOsc[i + 1]) - (b3 * BufferDecycleOsc[i + 2])
        BufferDO[i] = (_fdiv(100.0 * coefficient * BufferDecycleOsc[i], BufferMA[i]) if (BufferMA[i] != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DecyclerOscillator(_MQL5Indicator):
    name = 'Decycler_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodHP': 125.0,  # HP period
        'InpCoefficient': 1.0,  # Coefficient
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

