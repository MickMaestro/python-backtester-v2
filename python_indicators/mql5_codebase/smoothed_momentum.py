"""Smoothed_Momentum — converted from MQL5: MQL5 Indicators/Smoothed_Momentum/Smoothed_Momentum.mq5

Smoothed Momentum indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SMomentum'}, 'levels': [], 'description': ['Smoothed Momentum indicator'], 'name': 'Smoothed_Momentum', 'source': 'MQL5 Indicators/Smoothed_Momentum/Smoothed_Momentum.mq5', 'folder': 'Smoothed_Momentum', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 12, 'label': 'Momentum period', 'sinput': False}, {'mql': 'InpUseSmoothing', 'py': 'InpUseSmoothing', 'param': 'InpUseSmoothing', 'type': 'int', 'default': 1, 'label': 'Use smoothing', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 20, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethodSm', 'py': 'InpMethodSm', 'param': 'InpMethodSm', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 12)  # Momentum period
InpUseSmoothing = _input('InpUseSmoothing', INPUT_YES)  # Use smoothing
InpPeriodSm = _input('InpPeriodSm', 20)  # Smoothing period
InpMethodSm = _input('InpMethodSm', MODE_SMA)  # Smoothing method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferSM = Arr(0, 0.0)
BufferMom = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_mom = 0
period_sm = 0
handle_ma = 0
weight_sum = 0

def OnInit():
    global handle_ma, period_mom, period_sm
    period_mom = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (2 if (InpPeriodSm < 2) else InpPeriodSm)
    SetIndexBuffer(0, BufferSM, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMom, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed Momentum (' + _str(period_mom) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (((2 * period_mom) + (period_sm * 2)) if InpUseSmoothing else 0))
    ArraySetAsSeries(BufferSM, True)
    ArraySetAsSeries(BufferMom, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_mom, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_mom - 1
        ArrayInitialize(BufferSM, 0)
        ArrayInitialize(BufferMom, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    if not InpUseSmoothing:
        for i in range(limit, 0 - 1, -1):
            BufferSM[i] = (_fdiv(100.0 * BufferMA[i], BufferMA[i + period_mom]) if (BufferMA[i] != 0) else 0)
        return rates_total
    for i in range(limit, 0 - 1, -1):
        BufferMom[i] = (_fdiv(100.0 * BufferMA[i], BufferMA[i + period_mom]) if (BufferMA[i] != 0) else 0)
    if InpUseSmoothing:
        _sw1 = InpMethodSm
        if _sw1 == MODE_EMA:
            return ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferMom, BufferSM)
        elif _sw1 == MODE_SMMA:
            return SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferMom, BufferSM)
        elif _sw1 == MODE_LWMA:
            return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferMom, BufferSM, _GlobRef(globals(), 'weight_sum'))
        else:
            return SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferMom, BufferSM)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothedMomentum(_MQL5Indicator):
    name = 'Smoothed_Momentum'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 12,  # Momentum period
        'InpUseSmoothing': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use smoothing
        'InpPeriodSm': 20,  # Smoothing period
        'InpMethodSm': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

