"""TMAGi — converted from MQL5: MQL5 Indicators/TMAGi/TMAGi.mq5

TMAGi oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TSMAGi', 2: 'TLWMAGi'}, 'levels': [], 'description': ['TMAGi oscillator'], 'name': 'TMAGi', 'source': 'MQL5 Indicators/TMAGi/TMAGi.mq5', 'folder': 'TMAGi', 'inputs': [{'mql': 'InpPeriodADX', 'py': 'InpPeriodADX', 'param': 'InpPeriodADX', 'type': 'uint', 'default': 14, 'label': 'ADX period', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 8, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodMiddle', 'py': 'InpPeriodMiddle', 'param': 'InpPeriodMiddle', 'type': 'uint', 'default': 16, 'label': 'Middle MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 25, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpSlowingSMA', 'py': 'InpSlowingSMA', 'param': 'InpSlowingSMA', 'type': 'uint', 'default': 3, 'label': 'SMA slowing', 'sinput': False}, {'mql': 'InpSlowingLWMA', 'py': 'InpSlowingLWMA', 'param': 'InpSlowingLWMA', 'type': 'uint', 'default': 8, 'label': 'LWMA slowing', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodADX = _input('InpPeriodADX', 14)  # ADX period
InpPeriodFast = _input('InpPeriodFast', 8)  # Fast MA period
InpPeriodMiddle = _input('InpPeriodMiddle', 16)  # Middle MA period
InpPeriodSlow = _input('InpPeriodSlow', 25)  # Slow MA period
InpSlowingSMA = _input('InpSlowingSMA', 3)  # SMA slowing
InpSlowingLWMA = _input('InpSlowingLWMA', 8)  # LWMA slowing
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferB1 = Arr(0, 0.0)
BufferB2 = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferADXP = Arr(0, 0.0)
BufferADXM = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferMMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
period_adx = 0
period_fma = 0
period_mma = 0
period_sma = 0
smooth_sma = 0
smooth_lwma = 0
period_max = 0
weight_sum = 0
handle_fma = 0
handle_mma = 0
handle_sma = 0
handle_adx = 0

def OnInit():
    global handle_adx, handle_fma, handle_mma, handle_sma, period_adx, period_fma, period_max, period_mma, period_sma, smooth_lwma, smooth_sma
    period_adx = (1 if (InpPeriodADX < 1) else InpPeriodADX)
    period_fma = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_mma = (1 if (InpPeriodMiddle < 1) else InpPeriodMiddle)
    period_sma = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    smooth_sma = (1 if (InpSlowingSMA < 1) else InpSlowingSMA)
    smooth_lwma = (1 if (InpSlowingLWMA < 1) else InpSlowingLWMA)
    period_max = fmax(period_fma, fmax(period_mma, fmax(period_sma, fmax(smooth_sma, smooth_lwma))))
    SetIndexBuffer(0, BufferB1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferB2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRAW, INDICATOR_DATA)
    SetIndexBuffer(3, BufferADXP, INDICATOR_DATA)
    SetIndexBuffer(4, BufferADXM, INDICATOR_DATA)
    SetIndexBuffer(5, BufferFMA, INDICATOR_DATA)
    SetIndexBuffer(6, BufferMMA, INDICATOR_DATA)
    SetIndexBuffer(7, BufferSMA, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TMAGi (' + _str(period_adx) + ',' + _str(period_fma) + ',' + _str(period_mma) + ',' + _str(period_sma) + ',' + _str(smooth_sma) + ',' + _str(smooth_lwma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferB1, True)
    ArraySetAsSeries(BufferB2, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferADXP, True)
    ArraySetAsSeries(BufferADXM, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferMMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fma, 0, MODE_SMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mma = iMA(None, PERIOD_CURRENT, period_mma, 0, MODE_SMA, InpAppliedPrice)
    if handle_mma == INVALID_HANDLE:
        Print('The iMA(', _str(period_mma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sma, 0, MODE_SMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_sma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_adx = iADX(None, PERIOD_CURRENT, period_adx)
    if handle_adx == INVALID_HANDLE:
        Print('The iADX(', _str(period_adx), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferB1, EMPTY_VALUE)
        ArrayInitialize(BufferB2, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferADXP, 0)
        ArrayInitialize(BufferADXM, 0)
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
    copied = CopyBuffer(handle_adx, PLUSDI_LINE, 0, count, BufferADXP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, MINUSDI_LINE, 0, count, BufferADXM)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        di = BufferADXP[i] - BufferADXM[i]
        BufferRAW[i] = (fabs(BufferFMA[i] - BufferMMA[i]) + fabs(BufferFMA[i] - BufferSMA[i]) + fabs(BufferMMA[i] - BufferSMA[i])) * di
    if SimpleMAOnBuffer(rates_total, prev_calculated, period_max, smooth_sma, BufferRAW, BufferB1) == 0:
        return 0
    if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_max, smooth_lwma, BufferRAW, BufferB2, _GlobRef(globals(), 'weight_sum')) == 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TMAGi(_MQL5Indicator):
    name = 'TMAGi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodADX': 14,  # ADX period
        'InpPeriodFast': 8,  # Fast MA period
        'InpPeriodMiddle': 16,  # Middle MA period
        'InpPeriodSlow': 25,  # Slow MA period
        'InpSlowingSMA': 3,  # SMA slowing
        'InpSlowingLWMA': 8,  # LWMA slowing
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

