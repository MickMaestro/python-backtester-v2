"""Elders Safe Zone  — converted from MQL5: MQL5 Indicators/Elders Safe Zone/Elders Safe Zone .mq5

Copyright: Cubesteak; Link: www.cubesteak.net; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Cubesteak', 'link': 'www.cubesteak.net', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Elders Safe Zone ', 'source': 'MQL5 Indicators/Elders Safe Zone/Elders Safe Zone .mq5', 'folder': 'Elders Safe Zone', 'inputs': [{'mql': 'LookBack', 'py': 'LookBack', 'param': 'LookBack', 'type': 'int', 'default': 10, 'label': 'LookBack', 'sinput': False}, {'mql': 'StopFactor', 'py': 'StopFactor', 'param': 'StopFactor', 'type': 'int', 'default': 3, 'label': 'StopFactor', 'sinput': False}, {'mql': 'EMALength', 'py': 'EMALength', 'param': 'EMALength', 'type': 'int', 'default': 13, 'label': 'EMALength', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LookBack = _input('LookBack', 10)  # LookBack
StopFactor = _input('StopFactor', 3)  # StopFactor
EMALength = _input('EMALength', 13)  # EMALength
ExtBuffer = Arr(0, 0.0)
ExtMaBuffer = Arr(0, 0.0)
ExtMaHandle = 0

def OnInit():
    global ExtMaHandle
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMaBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, EMALength)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ExtMaHandle = iMA(Symbol(), Period(), EMALength, 0, MODE_EMA, PRICE_CLOSE)
    if ExtMaHandle == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < EMALength:
        return 0
    calculated = BarsCalculated(ExtMaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtMaHandle is calculated (', calculated, ' bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtMaHandle, 0, 0, to_copy, ExtMaBuffer) <= 0:
        Print('Getting fast EMA is failed! Error', GetLastError())
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = LookBack + 1
        ArrayInitialize(ExtBuffer, 0.0)
    else:
        limit = prev_calculated - 1
    SafeStop = 0.0
    for i in range(limit, rates_total):
        EMA0 = ExtMaBuffer[i]
        EMA1 = ExtMaBuffer[i - 1]
        EMA2 = ExtMaBuffer[i - 2]
        PreSafeStop = ExtBuffer[i - 1]
        Pen = 0.0
        Counter = 0
        if EMA0 > EMA1:
            for value1 in range(0, LookBack + 1):
                if low[i - value1] < low[i - value1 - 1]:
                    Pen = low[i - value1 - 1] - low[i - value1] + Pen
                    Counter = Counter + 1
            if Counter != 0:
                SafeStop = close[i] - (float(StopFactor) * _fdiv(Pen, float(Counter)))
            else:
                SafeStop = close[i] - (float(StopFactor) * Pen)
            if SafeStop < PreSafeStop and EMA1 > EMA2:
                SafeStop = PreSafeStop
        if EMA0 < EMA1:
            for value1 in range(0, LookBack + 1):
                if high[i - value1] > high[i - value1 - 1]:
                    Pen = high[i - value1] - high[i - value1 - 1] + Pen
                    Counter = Counter + 1
            if Counter != 0:
                SafeStop = close[i] + (float(StopFactor) * _fdiv(Pen, float(Counter)))
            else:
                SafeStop = close[i] + (float(StopFactor) * Pen)
            if SafeStop > PreSafeStop and EMA1 < EMA2:
                SafeStop = PreSafeStop
        PreSafeStop = SafeStop
        ExtBuffer[i] = SafeStop
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EldersSafeZone(_MQL5Indicator):
    name = 'Elders Safe Zone '
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LookBack': 10,  # LookBack
        'StopFactor': 3,  # StopFactor
        'EMALength': 13,  # EMALength
    }

