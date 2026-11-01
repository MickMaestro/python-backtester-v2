"""Vortex_Difference — converted from MQL5: MQL5 Indicators/Vortex_Difference/Vortex_Difference.mq5

\\"VORTEX\\" difference indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 3329330, 255, 36095, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Diff'}, 'levels': [], 'description': ['\\"VORTEX\\" difference indicator'], 'name': 'Vortex_Difference', 'source': 'MQL5 Indicators/Vortex_Difference/Vortex_Difference.mq5', 'folder': 'Vortex_Difference', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferDiff = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferVIP = Arr(0, 0.0)
BufferVIM = Arr(0, 0.0)
BufferVipRAW = Arr(0, 0.0)
BufferVimRAW = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferVipAVG = Arr(0, 0.0)
BufferVimAVG = Arr(0, 0.0)
BufferAtrAVG = Arr(0, 0.0)
period_ind = 0
handle_atr = 0

def OnInit():
    global handle_atr, period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferDiff, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferVIP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferVIM, INDICATOR_DATA)
    SetIndexBuffer(4, BufferVipRAW, INDICATOR_DATA)
    SetIndexBuffer(5, BufferVimRAW, INDICATOR_DATA)
    SetIndexBuffer(6, BufferATR, INDICATOR_DATA)
    SetIndexBuffer(7, BufferVipAVG, INDICATOR_DATA)
    SetIndexBuffer(8, BufferVimAVG, INDICATOR_DATA)
    SetIndexBuffer(9, BufferAtrAVG, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VORTEX difference (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferVIP, True)
    ArraySetAsSeries(BufferVIM, True)
    ArraySetAsSeries(BufferVipRAW, True)
    ArraySetAsSeries(BufferVimRAW, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferVipAVG, True)
    ArraySetAsSeries(BufferVimAVG, True)
    ArraySetAsSeries(BufferAtrAVG, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, 1)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVIP, EMPTY_VALUE)
        ArrayInitialize(BufferVIM, EMPTY_VALUE)
        ArrayInitialize(BufferVipRAW, 0)
        ArrayInitialize(BufferVimRAW, 0)
        ArrayInitialize(BufferATR, 0)
        ArrayInitialize(BufferVipAVG, 0)
        ArrayInitialize(BufferVimAVG, 0)
        ArrayInitialize(BufferAtrAVG, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferVipRAW[i] = fabs(high[i] - low[i + 1])
        BufferVimRAW[i] = fabs(low[i] - high[i + 1])
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVipRAW, BufferVipAVG) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferVimRAW, BufferVimAVG) == 0:
        return 0
    if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferATR, BufferAtrAVG) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        if BufferAtrAVG[i] != 0:
            BufferVIP[i] = _fdiv(100.0 * BufferVipAVG[i], BufferAtrAVG[i])
            BufferVIM[i] = _fdiv(100.0 * BufferVimAVG[i], BufferAtrAVG[i])
        else:
            BufferVIP[i] = 0.0
            BufferVIM[i] = 0.0
        BufferDiff[i] = BufferVIP[i] - BufferVIM[i]
        BufferColors[i] = ((0 if (BufferDiff[i] > BufferDiff[i + 1]) else 1) if (BufferDiff[i] > 0) else (2 if (BufferDiff[i] < BufferDiff[i + 1]) else 3) if (BufferDiff[i] < 0) else 4)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VortexDifference(_MQL5Indicator):
    name = 'Vortex_Difference'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

