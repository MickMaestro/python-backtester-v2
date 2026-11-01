"""IdeaTrend — converted from MQL5: MQL5 Indicators/IdeaTrend/IdeaTrend.mq5

Idea Trend oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Trend'}, 'levels': [], 'description': ['Idea Trend oscillator'], 'name': 'IdeaTrend', 'source': 'MQL5 Indicators/IdeaTrend/IdeaTrend.mq5', 'folder': 'IdeaTrend', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpLevel', 'py': 'InpLevel', 'param': 'InpLevel', 'type': 'double', 'default': 1.0, 'label': 'Threshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpLevel = _input('InpLevel', 1.0)  # Threshold
BufferTrend = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
BufferMAC = Arr(0, 0.0)
period = 0
handle_mah = 0
handle_mal = 0
handle_mac = 0
level = 0.0

def OnInit():
    global handle_mac, handle_mah, handle_mal, level, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    level = InpLevel
    SetIndexBuffer(0, BufferTrend, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAC, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Idea Trend (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, level)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Direction trend threshold')
    ArraySetAsSeries(BufferTrend, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ArraySetAsSeries(BufferMAC, True)
    ResetLastError()
    handle_mah = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mal = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_LOW)
    if handle_mal == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mac = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_CLOSE)
    if handle_mac == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_CLOSE object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTrend, EMPTY_VALUE)
        ArrayInitialize(BufferMAH, 0)
        ArrayInitialize(BufferMAL, 0)
        ArrayInitialize(BufferMAC, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mac, 0, 0, count, BufferMAC)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        MAH = BufferMAH[i]
        MAL = BufferMAL[i]
        MAC = BufferMAC[i]
        BufferTrend[i] = (_fdiv(MAH - MAC, MAC - MAL) if (MAC != MAL) else 0)
        BufferColors[i] = (0 if (BufferTrend[i] < level) else 1 if (BufferTrend[i] > level) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IdeaTrend(_MQL5Indicator):
    name = 'IdeaTrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpLevel': 1.0,  # Threshold
    }

