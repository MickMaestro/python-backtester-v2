"""SSIFT — converted from MQL5: MQL5 Indicators/SSIFT/SSIFT.mq5

Smoothed Stochastic Inverse Fisher Transform
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'IFT', 2: 'RBW'}, 'levels': [], 'description': ['Smoothed Stochastic Inverse Fisher Transform'], 'name': 'SSIFT', 'source': 'MQL5 Indicators/SSIFT/SSIFT.mq5', 'folder': 'SSIFT', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 30, 'label': 'Period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 5, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 30)  # Period
InpSlowing = _input('InpSlowing', 5)  # Slowing
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferIFT = Arr(0, 0.0)
BufferRBW = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferMAA = Arr(0, 0.0)
BufferRainbow = Arr(0, 0.0)
BufferStoch = Arr(0, 0.0)
period_ind = 0
slowing = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ind, slowing
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    SetIndexBuffer(0, BufferIFT, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRBW, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRainbow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferStoch, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SSIFT(' + _str(period_ind) + ',' + _str(slowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferIFT, True)
    ArraySetAsSeries(BufferRBW, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferMAA, True)
    ArraySetAsSeries(BufferRainbow, True)
    ArraySetAsSeries(BufferStoch, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 11:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 11
        ArrayInitialize(BufferIFT, EMPTY_VALUE)
        ArrayInitialize(BufferRBW, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferMAA, 0)
        ArrayInitialize(BufferRainbow, 0)
        ArrayInitialize(BufferStoch, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRainbow[i] = ((20 * BufferMA[i]) + (75 * BufferMA[i + 1]) + (180 * BufferMA[i + 2]) + (336 * BufferMA[i + 3]) + (463 * BufferMA[i + 4]) + (462 * BufferMA[i + 5]) + (330 * BufferMA[i + 6]) + (165 * BufferMA[i + 7]) + (55 * BufferMA[i + 8]) + (11 * BufferMA[i + 9]) + BufferMA[i + 10]) / 2098
    for i in range(limit, 0 - 1, -1):
        min_ = BufferRainbow[ArrayMinimum(BufferRainbow, i, period_ind)]
        max_ = BufferRainbow[ArrayMaximum(BufferRainbow, i, period_ind)]
        val = max_ - min_
        BufferStoch[i] = _fdiv(100 * (BufferRainbow[i] - min_), (val if (val != 0) else DBL_MIN))
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, slowing, BufferStoch, BufferMAA)
    for i in range(limit, 0 - 1, -1):
        BufferRBW[i] = BufferMAA[i]
        x = (BufferRBW[i] - 50) / 5
        BufferIFT[i] = (_fdiv(exp(x) - 1, exp(x) + 1) + 1) * 50
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SSIFT(_MQL5Indicator):
    name = 'SSIFT'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 30,  # Period
        'InpSlowing': 5,  # Slowing
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

