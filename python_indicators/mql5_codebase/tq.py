"""TQ — converted from MQL5: MQL5 Indicators/TQ/TQ.mq5

Trend Quality oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [32768, 255], 2: [16711680]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TQuality', 2: 'TCorrection'}, 'levels': [], 'description': ['Trend Quality oscillator'], 'name': 'TQ', 'source': 'MQL5 Indicators/TQ/TQ.mq5', 'folder': 'TQ', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 7, 'label': 'Period fast', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 14, 'label': 'Period slow', 'sinput': False}, {'mql': 'InpPeriodST', 'py': 'InpPeriodST', 'param': 'InpPeriodST', 'type': 'uint', 'default': 5, 'label': 'Scalar trend period', 'sinput': False}, {'mql': 'InpPeriodSN', 'py': 'InpPeriodSN', 'param': 'InpPeriodSN', 'type': 'uint', 'default': 250, 'label': 'Scalar noise period', 'sinput': False}, {'mql': 'InpCorrection', 'py': 'InpCorrection', 'param': 'InpCorrection', 'type': 'uint', 'default': 2, 'label': 'Scalar correction factor', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 7)  # Period fast
InpPeriodSlow = _input('InpPeriodSlow', 14)  # Period slow
InpPeriodST = _input('InpPeriodST', 5)  # Scalar trend period
InpPeriodSN = _input('InpPeriodSN', 250)  # Scalar noise period
InpCorrection = _input('InpCorrection', 2)  # Scalar correction factor
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTQ = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferT = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferFEMA = Arr(0, 0.0)
BufferSEMA = Arr(0, 0.0)
BufferReversals = Arr(0, 0.0)
BufferCPC = Arr(0, 0.0)
BufferTrend = Arr(0, 0.0)
BufferDT = Arr(0, 0.0)
BufferAVG = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_st = 0
period_sn = 0
correction = 0
handle_fema = 0
handle_sema = 0
handle_sma = 0

def OnInit():
    global correction, handle_fema, handle_sema, handle_sma, period_fast, period_slow, period_sn, period_st
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_st = (1 if (InpPeriodST < 1) else InpPeriodST)
    period_sn = (2 if (InpPeriodSN < 2) else InpPeriodSN)
    correction = (1 if (InpCorrection < 1) else InpCorrection)
    SetIndexBuffer(0, BufferTQ, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferT, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferFEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferReversals, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferCPC, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferTrend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferDT, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferAVG, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Quality (' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_st) + ',' + _str(period_sn) + ',' + _str(correction) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferTQ, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferT, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferFEMA, True)
    ArraySetAsSeries(BufferSEMA, True)
    ArraySetAsSeries(BufferReversals, True)
    ArraySetAsSeries(BufferCPC, True)
    ArraySetAsSeries(BufferTrend, True)
    ArraySetAsSeries(BufferDT, True)
    ArraySetAsSeries(BufferAVG, True)
    ResetLastError()
    handle_fema = iMA(None, PERIOD_CURRENT, period_fast, 0, MODE_EMA, InpAppliedPrice)
    if handle_fema == INVALID_HANDLE:
        Print('The Fast iMA(', _str(period_fast), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sema = iMA(None, PERIOD_CURRENT, period_slow, 0, MODE_EMA, InpAppliedPrice)
    if handle_sema == INVALID_HANDLE:
        Print('The Slow iMA(', _str(period_slow), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTQ, EMPTY_VALUE)
        ArrayInitialize(BufferT, EMPTY_VALUE)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferFEMA, 0)
        ArrayInitialize(BufferSEMA, 0)
        ArrayInitialize(BufferReversals, 0)
        ArrayInitialize(BufferCPC, 0)
        ArrayInitialize(BufferTrend, 0)
        ArrayInitialize(BufferDT, 0)
        ArrayInitialize(BufferAVG, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_fema, 0, 0, count, BufferFEMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sema, 0, 0, count, BufferSEMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferT[i] = (1 if (BufferFEMA[i] > BufferSEMA[i]) else -1)
        BufferReversals[i] = BufferFEMA[i] - BufferSEMA[i]
        if (BufferReversals[i] * BufferReversals[i + 1]) <= 0:
            BufferTrend[i] = 0.0
            BufferCPC[i] = BufferTrend[i]
        else:
            BufferCPC[i] = BufferCPC[i + 1] + (BufferSMA[i] - BufferSMA[i + 1])
            BufferTrend[i] = _fdiv(BufferCPC[i], period_st) + (BufferTrend[i + 1] * (1.0 - _fdiv(1.0, period_st)))
        BufferDT[i] = (BufferCPC[i] - BufferTrend[i]) * (BufferCPC[i] - BufferTrend[i])
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sn, BufferDT, BufferAVG)
    for i in range(limit, 0 - 1, -1):
        Noise = sqrt(BufferAVG[i])
        BufferTQ[i] = (_fdiv(correction * BufferTrend[i], Noise) if (Noise != 0.0) else 0)
        BufferColors[i] = (1 if (BufferTQ[i] < BufferTQ[i + 1]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TQ(_MQL5Indicator):
    name = 'TQ'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 7,  # Period fast
        'InpPeriodSlow': 14,  # Period slow
        'InpPeriodST': 5,  # Scalar trend period
        'InpPeriodSN': 250,  # Scalar noise period
        'InpCorrection': 2,  # Scalar correction factor
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

