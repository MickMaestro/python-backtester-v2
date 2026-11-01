"""StdDev_Cross — converted from MQL5: MQL5 Indicators/StdDev_Cross/StdDev_Cross.mq5

StdDev Cross indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [32768], 2: [255], 3: [16711680], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'StdDev1', 2: 'StdDev2', 3: 'Cross up', 4: 'Cross down'}, 'levels': [], 'description': ['StdDev Cross indicator'], 'name': 'StdDev_Cross', 'source': 'MQL5 Indicators/StdDev_Cross/StdDev_Cross.mq5', 'folder': 'StdDev_Cross', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 10, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 0, 'label': 'First MA method', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 20, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 0, 'label': 'Second MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 10)  # First MA period
InpMethod1 = _input('InpMethod1', MODE_SMA)  # First MA method
InpPeriod2 = _input('InpPeriod2', 20)  # Second MA period
InpMethod2 = _input('InpMethod2', MODE_SMA)  # Second MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferDev1 = Arr(0, 0.0)
BufferDev2 = Arr(0, 0.0)
BufferCrossUP = Arr(0, 0.0)
BufferCrossDN = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
period_ma1 = 0
period_ma2 = 0
period_max = 0
handle_ma1 = 0
handle_ma2 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_ma2, handle_maP, period_ma1, period_ma2, period_max
    period_ma1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period_ma2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    period_max = fmax(period_ma1, period_ma2)
    SetIndexBuffer(0, BufferDev1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDev2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCrossUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCrossDN, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMAP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMA2, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StdDev Cross (' + _str(period_ma1) + ',' + _str(period_ma2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDev1, True)
    ArraySetAsSeries(BufferDev2, True)
    ArraySetAsSeries(BufferCrossUP, True)
    ArraySetAsSeries(BufferCrossDN, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period_ma1, 0, InpMethod1, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, period_ma2, 0, InpMethod2, InpAppliedPrice)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferDev1, EMPTY_VALUE)
        ArrayInitialize(BufferDev2, EMPTY_VALUE)
        ArrayInitialize(BufferCrossUP, EMPTY_VALUE)
        ArrayInitialize(BufferCrossDN, EMPTY_VALUE)
        ArrayInitialize(BufferMAP, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferMA2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        MA1 = BufferMA1[i]
        MA2 = BufferMA2[i]
        dAmount = 0.0
        for j in range(0, period_ma1 + 1):
            Pr = BufferMAP[i + j]
            dAmount += (Pr - MA1) * (Pr - MA1)
        BufferDev1[i] = sqrt(_fdiv(dAmount, float(period_ma1)))
        dAmount = 0.0
        for j in range(0, period_ma2 + 1):
            Pr = BufferMAP[i + j]
            dAmount += (Pr - MA2) * (Pr - MA2)
        BufferDev2[i] = sqrt(_fdiv(dAmount, float(period_ma2)))
        BufferCrossDN[i] = EMPTY_VALUE
        BufferCrossUP[i] = BufferCrossDN[i]
        if BufferDev1[i + 1] < BufferDev2[i + 1] and BufferDev1[i] >= BufferDev2[i]:
            BufferCrossUP[i] = (BufferDev1[i] + BufferDev2[i]) / 2.0
        elif BufferDev1[i + 1] > BufferDev2[i + 1] and BufferDev1[i] <= BufferDev2[i]:
            BufferCrossDN[i] = (BufferDev1[i] + BufferDev2[i]) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StdDevCross(_MQL5Indicator):
    name = 'StdDev_Cross'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 10,  # First MA period
        'InpMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # First MA method
        'InpPeriod2': 20,  # Second MA period
        'InpMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Second MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

