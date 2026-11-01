"""Dinapoli_Preferred_Stochastic — converted from MQL5: MQL5 Indicators/Dinapoli_Preferred_Stochastic/Dinapoli_Preferred_Stochastic.mq5

Dinapoli Preferred Stochastic oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'DPS %K', 2: 'DPS %D'}, 'levels': [], 'description': ['Dinapoli Preferred Stochastic oscillator'], 'name': 'Dinapoli_Preferred_Stochastic', 'source': 'MQL5 Indicators/Dinapoli_Preferred_Stochastic/Dinapoli_Preferred_Stochastic.mq5', 'folder': 'Dinapoli_Preferred_Stochastic', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 10, 'label': '%K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 5, 'label': '%D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 5, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 10)  # %K period
InpPeriodD = _input('InpPeriodD', 5)  # %D period
InpSlowing = _input('InpSlowing', 5)  # Slowing
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_k = 0
period_d = 0
slowing = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_d, period_k, slowing
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    period_d = (1 if (InpPeriodD < 1) else InpPeriodD)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dinapoli Preferred Stochastic (' + _str(period_k) + ',' + _str(period_d) + ',' + _str(slowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_k, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_k - 2
        ArrayInitialize(BufferK, 0)
        ArrayInitialize(BufferD, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferMA, i, period_k)
        bh = ArrayMaximum(BufferMA, i, period_k)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferMA[bl]
        max_ = BufferMA[bh]
        if max_ != min_:
            fast_k = _fdiv(100.0 * (BufferMA[i] - min_), max_ - min_)
            BufferK[i] = BufferK[i + 1] + _fdiv(fast_k - BufferK[i + 1], slowing)
            BufferD[i] = BufferD[i + 1] + _fdiv(BufferK[i] - BufferD[i + 1], period_d)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DinapoliPreferredStochastic(_MQL5Indicator):
    name = 'Dinapoli_Preferred_Stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 10,  # %K period
        'InpPeriodD': 5,  # %D period
        'InpSlowing': 5,  # Slowing
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

