"""Normalized_AC — converted from MQL5: MQL5 Indicators/Normalized_AC/Normalized_AC.mq5

Normalized Acceleration/Deceleration indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10526303]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'AC'}, 'levels': [], 'description': ['Normalized Acceleration/Deceleration indicator'], 'name': 'Normalized_AC', 'source': 'MQL5 Indicators/Normalized_AC/Normalized_AC.mq5', 'folder': 'Normalized_AC', 'inputs': [{'mql': 'InpPeriodFastMA', 'py': 'InpPeriodFastMA', 'param': 'InpPeriodFastMA', 'type': 'uint', 'default': 5, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlowMA', 'py': 'InpPeriodSlowMA', 'param': 'InpPeriodSlowMA', 'type': 'uint', 'default': 35, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpPeriodSM', 'py': 'InpPeriodSM', 'param': 'InpPeriodSM', 'type': 'uint', 'default': 5, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpNormLevel', 'py': 'InpNormLevel', 'param': 'InpNormLevel', 'type': 'uint', 'default': 50, 'label': 'Normalization level', 'sinput': False}, {'mql': 'InpScale', 'py': 'InpScale', 'param': 'InpScale', 'type': 'uint', 'default': 300, 'label': 'Scale', 'sinput': False}, {'mql': 'InpPeriodNorm', 'py': 'InpPeriodNorm', 'param': 'InpPeriodNorm', 'type': 'uint', 'default': 0, 'label': 'Normalization period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFastMA = _input('InpPeriodFastMA', 5)  # Fast MA period
InpPeriodSlowMA = _input('InpPeriodSlowMA', 35)  # Slow MA period
InpPeriodSM = _input('InpPeriodSM', 5)  # Smoothing period
InpNormLevel = _input('InpNormLevel', 50)  # Normalization level
InpScale = _input('InpScale', 300)  # Scale
InpPeriodNorm = _input('InpPeriodNorm', 0)  # Normalization period
BufferAC = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferAO = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferRawAC = Arr(0, 0.0)
period_fma = 0
period_sma = 0
period_sm = 0
period_max = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_sma, period_fma, period_max, period_sm, period_sma
    period_fma = (1 if (InpPeriodFastMA < 1) else InpPeriodFastMA)
    period_sma = (1 if (InpPeriodSlowMA < 1) else InpPeriodSlowMA)
    period_sm = (2 if (InpPeriodSM < 2) else InpPeriodSM)
    period_max = fmax(period_sm, fmax(period_fma, period_sma))
    SetIndexBuffer(0, BufferAC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRawAC, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Normalized Acceleration/Deceleration (' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max)
    ArraySetAsSeries(BufferAC, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferAO, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferRawAC, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fma, 0, MODE_SMA, PRICE_MEDIAN)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sma, 0, MODE_SMA, PRICE_MEDIAN)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_sma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferAC, EMPTY_VALUE)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferAO, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferRawAC, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferAO[i] = BufferFMA[i] - BufferSMA[i]
    SimpleMAOnBuffer(rates_total, prev_calculated, period_max, period_sm, BufferAO, BufferMA)
    for i in range(limit, 0 - 1, -1):
        BufferRawAC[i] = BufferAO[i] - BufferMA[i]
    bl = WRONG_VALUE
    bh = WRONG_VALUE
    scale = 0.0
    max_ = 0.0
    min_ = 0.0
    abs_min = 0.0
    for i in range(limit, 0 - 1, -1):
        num = ((rates_total - period_max - 4) if (InpPeriodNorm == 0) else InpPeriodNorm)
        bl = ArrayMinimum(BufferRawAC, 0, num)
        bh = ArrayMaximum(BufferRawAC, 0, num)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferRawAC[bl]
        max_ = BufferRawAC[bh]
        scale = ((max_ - min_) if (InpScale == 0) else InpScale)
        abs_min = fabs(max_)
        BufferAC[i] = InpNormLevel + (BufferRawAC[i] * _fdiv(scale, (abs_min if (abs_min != 0) else 1.0)))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NormalizedAC(_MQL5Indicator):
    name = 'Normalized_AC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMA': 5,  # Fast MA period
        'InpPeriodSlowMA': 35,  # Slow MA period
        'InpPeriodSM': 5,  # Smoothing period
        'InpNormLevel': 50,  # Normalization level
        'InpScale': 300,  # Scale
        'InpPeriodNorm': 0,  # Normalization period
    }

