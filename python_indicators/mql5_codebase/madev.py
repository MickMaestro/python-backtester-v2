"""MaDev — converted from MQL5: MQL5 Indicators/MaDev/MaDev.mq5

Deviation from MA indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [7451452], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'MA', 2: 'Upper max dev', 3: 'Lower max dev'}, 'levels': [], 'description': ['Deviation from MA indicator'], 'name': 'MaDev', 'source': 'MQL5 Indicators/MaDev/MaDev.mq5', 'folder': 'MaDev', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpFrame', 'py': 'InpFrame', 'param': 'InpFrame', 'type': 'uint', 'default': 3, 'label': 'Frames', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpMethod = _input('InpMethod', MODE_EMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpFrame = _input('InpFrame', 3)  # Frames
BufferMA = Arr(0, 0.0)
BufferUp = Arr(0, 0.0)
BufferDn = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
period = 0
shift = 0
frame = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global frame, handle_ma1, handle_maP, period, shift
    period = (1 if (InpPeriod < 1) else InpPeriod)
    frame = (2 if (InpFrame < 2) else InpFrame)
    shift = _int(floor((frame - 1.0) / 2.0))
    SetIndexBuffer(0, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUp, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDn, INDICATOR_DATA)
    SetIndexBuffer(3, BufferPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDev, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MaDev (' + _str(period) + ',' + _str(frame) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferUp, True)
    ArraySetAsSeries(BufferDn, True)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferDev, True)
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
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferUp, EMPTY_VALUE)
        ArrayInitialize(BufferDn, EMPTY_VALUE)
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferDev, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDev[i] = BufferPrice[i] - BufferMA[i]
        min_ = True
        max_ = True
        for j in range(1, shift + 1):
            if BufferDev[i + shift + 1] >= BufferDev[i + j + shift + 1] or BufferDev[i + shift + 1] >= BufferDev[i - j + shift + 1]:
                min_ = False
            if BufferDev[i + shift + 1] <= BufferDev[i + j + shift + 1] or BufferDev[i + shift + 1] <= BufferDev[i - j + shift + 1]:
                max_ = False
        BufferDn[i + shift + 1] = (low[i + shift + 1] if (min_ and BufferDev[i + shift + 1] < 0) else EMPTY_VALUE)
        BufferUp[i + shift + 1] = (high[i + shift + 1] if (max_ and BufferDev[i + shift + 1] > 0) else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaDev(_MQL5Indicator):
    name = 'MaDev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpFrame': 3,  # Frames
    }

