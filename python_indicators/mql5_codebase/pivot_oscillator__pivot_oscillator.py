"""Pivot_Oscillator — converted from MQL5: MQL5 Indicators/Pivot_Oscillator/Pivot_Oscillator.mq5

Pivot Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [32768, 255, 11119017], 2: [15453831]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Pivot Osc', 2: 'Line'}, 'levels': [], 'description': ['Pivot Oscillator'], 'name': 'Pivot_Oscillator', 'source': 'MQL5 Indicators/Pivot_Oscillator/Pivot_Oscillator.mq5', 'folder': 'Pivot_Oscillator', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 13, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodMedium', 'py': 'InpPeriodMedium', 'param': 'InpPeriodMedium', 'type': 'uint', 'default': 21, 'label': 'Medium MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 34, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 13)  # Fast MA period
InpPeriodMedium = _input('InpPeriodMedium', 21)  # Medium MA period
InpPeriodSlow = _input('InpPeriodSlow', 34)  # Slow MA period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
BufferOSC = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferLine = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferMMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
period_fma = 0
period_mma = 0
period_sma = 0
period_max = 0
handle_fma = 0
handle_mma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_mma, handle_sma, period_fma, period_max, period_mma, period_sma
    period_fma = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_sma = ((period_fma + 1) if (InpPeriodSlow == period_fma) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_mma = ((period_sma + 1) if (InpPeriodMedium == period_sma) else 1 if (InpPeriodMedium < 1) else InpPeriodMedium)
    period_max = fmax(period_fma, fmax(period_mma, period_sma))
    SetIndexBuffer(0, BufferOSC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferLine, INDICATOR_DATA)
    SetIndexBuffer(3, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Pivot Osc (' + _str(period_fma) + ',' + _str(period_mma) + ',' + _str(period_sma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferOSC, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferLine, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferMMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fma, 0, InpMethod, PRICE_TYPICAL)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mma = iMA(None, PERIOD_CURRENT, period_mma, 0, InpMethod, PRICE_TYPICAL)
    if handle_mma == INVALID_HANDLE:
        Print('The iMA(', _str(period_mma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sma, 0, InpMethod, PRICE_TYPICAL)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_sma), ') by object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferOSC, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferLine, EMPTY_VALUE)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferMMA, 0)
        ArrayInitialize(BufferSMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mma, 0, 0, count, BufferMMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        D1 = BufferFMA[i] - BufferSMA[i]
        D2 = BufferFMA[i] - BufferSMA[i]
        D3 = BufferFMA[i] - BufferFMA[i]
        TP = (close[i] + high[i] + low[i]) / 3.0
        BufferLine[i] = (_fdiv(D1 + D2 + D3, TP) if (TP != 0) else 0)
        BufferOSC[i] = BufferLine[i]
        BufferColors[i] = (0 if (BufferOSC[i] > BufferOSC[i + 1]) else 1 if (BufferOSC[i] < BufferOSC[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PivotOscillator(_MQL5Indicator):
    name = 'Pivot_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 13,  # Fast MA period
        'InpPeriodMedium': 21,  # Medium MA period
        'InpPeriodSlow': 34,  # Slow MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
    }

