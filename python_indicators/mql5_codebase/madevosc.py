"""MaDevOsc — converted from MQL5: MQL5 Indicators/MaDevOsc/MaDevOsc.mq5

Deviation from MA oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 16711680, 11119017]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'MaDevOsc'}, 'levels': [], 'description': ['Deviation from MA oscillator'], 'name': 'MaDevOsc', 'source': 'MQL5 Indicators/MaDevOsc/MaDevOsc.mq5', 'folder': 'MaDevOsc', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpFrame', 'py': 'InpFrame', 'param': 'InpFrame', 'type': 'uint', 'default': 3, 'label': 'Frames', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpMethod = _input('InpMethod', MODE_EMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpFrame = _input('InpFrame', 3)  # Frames
BufferMDO = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
period = 0
shift = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_maP, period, shift
    period = (1 if (InpPeriod < 1) else InpPeriod)
    shift = _int((InpFrame - 1.0) / 2.0)
    SetIndexBuffer(0, BufferMDO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferPrice, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MaDevOsc (' + _str(period) + ',' + _str(InpFrame) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMDO, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferPrice, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(shift, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - (2 * shift) - 2
        ArrayInitialize(BufferMDO, 0)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferPrice, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMDO[i] = BufferPrice[i] - BufferMA[i]
        min_ = True
        max_ = True
        for j in range(1, shift + 1):
            if BufferMDO[i + shift + 1] >= BufferMDO[i + j + shift + 1] or BufferMDO[i + shift + 1] >= BufferMDO[i - j + shift + 1]:
                min_ = False
            if BufferMDO[i + shift + 1] <= BufferMDO[i + j + shift + 1] or BufferMDO[i + shift + 1] <= BufferMDO[i - j + shift + 1]:
                max_ = False
        BufferColors[i + shift + 1] = (1 if (min_ and BufferMDO[i + shift + 1] < 0) else 0 if (max_ and BufferMDO[i + shift + 1] > 0) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaDevOsc(_MQL5Indicator):
    name = 'MaDevOsc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpFrame': 3,  # Frames
    }

