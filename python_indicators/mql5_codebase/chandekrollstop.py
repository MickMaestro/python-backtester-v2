"""ChandeKrollStop — converted from MQL5: MQL5 Indicators/Chande Kroll Stop/ChandeKrollStop.mq5

Copyright: Copyright 2023, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Stop Long', 2: 'Stop Short'}, 'levels': [], 'description': [], 'name': 'ChandeKrollStop', 'source': 'MQL5 Indicators/Chande Kroll Stop/ChandeKrollStop.mq5', 'folder': 'Chande Kroll Stop', 'inputs': [{'mql': 'InpAtrLength', 'py': 'InpAtrLength', 'param': 'InpAtrLength', 'type': 'uint', 'default': 10, 'label': 'ATR Length', 'sinput': False}, {'mql': 'InpAtrCoeff', 'py': 'InpAtrCoeff', 'param': 'InpAtrCoeff', 'type': 'uint', 'default': 1, 'label': 'ATR Coefficient', 'sinput': False}, {'mql': 'InpStopLength', 'py': 'InpStopLength', 'param': 'InpStopLength', 'type': 'uint', 'default': 9, 'label': 'Stop Length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpAtrLength = _input('InpAtrLength', 10)  # ATR Length
InpAtrCoeff = _input('InpAtrCoeff', 1)  # ATR Coefficient
InpStopLength = _input('InpStopLength', 9)  # Stop Length
ExtBufferStopLong = Arr(0, 0.0)
ExtBufferStopShort = Arr(0, 0.0)
ExtBufferATR = Arr(0, 0.0)
ExtBufferFirstHighStop = Arr(0, 0.0)
ExtBufferFirstLowStop = Arr(0, 0.0)
ExtHandleATR = 0
ExtAtrLength = 0
ExtAtrCoeff = 0
ExtStopLength = 0

def OnInit():
    global ExtAtrCoeff, ExtAtrLength, ExtHandleATR, ExtStopLength
    SetIndexBuffer(0, ExtBufferStopLong, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferStopShort, INDICATOR_DATA)
    SetIndexBuffer(2, ExtBufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtBufferFirstHighStop, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtBufferFirstLowStop, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBufferStopLong, True)
    ArraySetAsSeries(ExtBufferStopShort, True)
    ArraySetAsSeries(ExtBufferATR, True)
    ArraySetAsSeries(ExtBufferFirstHighStop, True)
    ArraySetAsSeries(ExtBufferFirstLowStop, True)
    ExtAtrLength = (1 if (InpAtrLength < 1) else InpAtrLength)
    ExtAtrCoeff = (1 if (InpAtrCoeff < 1) else InpAtrCoeff)
    ExtStopLength = (1 if (InpStopLength < 1) else InpStopLength)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Chande Kroll Stop (%lu, %lu, %lu)', ExtAtrLength, ExtAtrCoeff, ExtStopLength))
    ResetLastError()
    ExtHandleATR = iATR(None, PERIOD_CURRENT, ExtAtrLength)
    if ExtHandleATR == INVALID_HANDLE:
        PrintFormat('The iATR(%lu) object was not created: Error %ld', ExtAtrLength, GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(ExtAtrLength, ExtStopLength):
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(ExtBufferStopLong, EMPTY_VALUE)
        ArrayInitialize(ExtBufferStopShort, EMPTY_VALUE)
        ArrayInitialize(ExtBufferATR, 0)
        ArrayInitialize(ExtBufferFirstHighStop, 0)
        ArrayInitialize(ExtBufferFirstLowStop, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(ExtHandleATR, 0, 0, count, ExtBufferATR)
    if copied != count:
        return 0
    array_h = Arr(0, 0.0)
    array_l = Arr(0, 0.0)
    for i in range(limit, 0 - 1, -1):
        count_2 = ExtAtrLength
        if (i + count_2) > (rates_total - 1):
            count_2 = rates_total - 1 - i
        if count_2 == 0:
            continue
        if ArrayCopy(array_h, high, 0, i, count_2) != count_2 or ArrayCopy(array_l, low, 0, i, count_2) != count_2:
            continue
        vh = 0
        vl = 0
        vh.Swap(array_h)
        vl.Swap(array_l)
        ExtBufferFirstHighStop[i] = vh.Max() - (ExtAtrCoeff * ExtBufferATR[i])
        ExtBufferFirstLowStop[i] = vl.Min() + (ExtAtrCoeff * ExtBufferATR[i])
    for i in range(limit, 0 - 1, -1):
        count_2 = ExtStopLength
        if (i + count_2) > (rates_total - 1):
            count_2 = rates_total - 1 - i
        if count_2 == 0:
            continue
        if ArrayCopy(array_h, ExtBufferFirstHighStop, 0, i, count_2) != count_2 or ArrayCopy(array_l, ExtBufferFirstLowStop, 0, i, count_2) != count_2:
            continue
        vh = 0
        vl = 0
        vh.Swap(array_h)
        vl.Swap(array_l)
        ExtBufferStopShort[i] = vh.Max()
        ExtBufferStopLong[i] = vl.Min()
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChandeKrollStop(_MQL5Indicator):
    name = 'ChandeKrollStop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAtrLength': 10,  # ATR Length
        'InpAtrCoeff': 1,  # ATR Coefficient
        'InpStopLength': 9,  # Stop Length
    }

