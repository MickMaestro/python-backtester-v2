"""ChaikinMoneyFlow — converted from MQL5: MQL5 Indicators/Chaikin Money Flow/ChaikinMoneyFlow.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2263842]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CMF'}, 'levels': [], 'description': [], 'name': 'ChaikinMoneyFlow', 'source': 'MQL5 Indicators/Chaikin Money Flow/ChaikinMoneyFlow.mq5', 'folder': 'Chaikin Money Flow', 'inputs': [{'mql': 'InpLength', 'py': 'InpLength', 'param': 'InpLength', 'type': 'uint', 'default': 20, 'label': 'Length', 'sinput': False}, {'mql': 'InpVolume', 'py': 'InpVolume', 'param': 'InpVolume', 'type': 'int', 'default': 0, 'label': 'Applied Volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpLength = _input('InpLength', 20)  # Length
InpVolume = _input('InpVolume', VOLUME_TICK)  # Applied Volume
ExtBufferCMF = Arr(0, 0.0)
ExtBufferTMP = Arr(0, 0.0)
length = 0

def OnInit():
    global length
    SetIndexBuffer(0, ExtBufferCMF, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferTMP, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBufferCMF, True)
    ArraySetAsSeries(ExtBufferTMP, True)
    length = (20 if (InpLength < 1) else InpLength)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('CMF(%lu)', length))
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < length:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(volume, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(ExtBufferCMF, EMPTY_VALUE)
        ArrayInitialize(ExtBufferTMP, 0)
    array_mfm = Arr(0, 0.0)
    array_mfv = Arr(0, 0.0)
    for i in range(limit, 0 - 1, -1):
        ExtBufferTMP[i] = (0 if ((close[i] == high[i] and close[i] == low[i]) or high[i] == low[i]) else (_fdiv((2 * close[i]) - low[i] - high[i], high[i] - low[i]) * (tick_volume[i] if (InpVolume == VOLUME_TICK) else volume[i])))
        count = length
        if (i + count) > (rates_total - 1):
            count = rates_total - 1 - i
        if count == 0:
            continue
        if ArrayCopy(array_mfm, ExtBufferTMP, 0, i, count) != count:
            continue
        copied = 0
        _sw1 = InpVolume
        if _sw1 == VOLUME_TICK:
            copied = ArrayCopy(array_mfv, tick_volume, 0, i, count)
        else:
            copied = ArrayCopy(array_mfv, volume, 0, i, count)
        if copied == 0:
            continue
        vmfm = 0
        vmfv = 0
        vmfm.Swap(array_mfm)
        vmfv.Swap(array_mfv)
        sum_mfm = vmfm.Sum()
        sum_mfv = vmfv.Sum()
        ExtBufferCMF[i] = _fdiv(sum_mfm, (sum_mfv if (sum_mfv != 0) else 1.0))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChaikinMoneyFlow(_MQL5Indicator):
    name = 'ChaikinMoneyFlow'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpLength': 20,  # Length
        'InpVolume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Applied Volume
    }

