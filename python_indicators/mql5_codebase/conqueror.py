"""Conqueror — converted from MQL5: MQL5 Indicators/Conqueror/Conqueror.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 10, 2: 5, 3: 5, 4: 5}, 'colors': {1: [32768, 255, 13882323], 2: [32768], 3: [255], 4: [13882323]}, 'widths': {1: 1, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'HIST', 2: 'To long pos', 3: 'To short pos', 4: 'Stop trade'}, 'levels': [], 'description': [], 'name': 'Conqueror', 'source': 'MQL5 Indicators/Conqueror/Conqueror.mq5', 'folder': 'Conqueror', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodRange1', 'py': 'InpPeriodRange1', 'param': 'InpPeriodRange1', 'type': 'uint', 'default': 10, 'label': 'Range 1 period', 'sinput': False}, {'mql': 'InpPeriodRange2', 'py': 'InpPeriodRange2', 'param': 'InpPeriodRange2', 'type': 'uint', 'default': 40, 'label': 'Range 2 period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 10)  # Period
InpPeriodRange1 = _input('InpPeriodRange1', 10)  # Range 1 period
InpPeriodRange2 = _input('InpPeriodRange2', 40)  # Range 2 period
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNO = Arr(0, 0.0)
BufferHIST = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ma = 0
period_rng1 = 0
period_rng2 = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma, period_rng1, period_rng2
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_rng1 = (1 if (InpPeriodRange1 < 1) else InpPeriodRange1)
    period_rng2 = (1 if (InpPeriodRange2 < 1) else InpPeriodRange2)
    SetIndexBuffer(0, BufferHIST, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(4, BufferNO, INDICATOR_DATA)
    SetIndexBuffer(5, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Conqueror(' + _str(period_ma) + ',' + _str(period_rng1) + ',' + _str(period_rng2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNO, True)
    ArraySetAsSeries(BufferHIST, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period_ma, fmax(period_rng1, period_rng2))
    if rates_total < max_:
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_ - 1
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNO, EMPTY_VALUE)
        ArrayInitialize(BufferHIST, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    copied = 0
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferNO[i] = EMPTY_VALUE
        BufferDN[i] = BufferNO[i]
        BufferUP[i] = BufferDN[i]
        MA0 = BufferMA[i]
        MA1 = BufferMA[i + period_rng1]
        BufferHIST[i] = BufferMA[i]
        if (close[i] > MA0 and MA0 > MA1) and close[i] > close[i + period_rng2]:
            BufferColors[i] = 0.0
        elif (close[i] < MA0 and MA0 < MA1) and close[i] < close[i + period_rng2]:
            BufferColors[i] = 1.0
        else:
            BufferColors[i] = 2.0
        if BufferColors[i] == 0 and BufferColors[i + 1] != 0:
            BufferUP[i] = BufferHIST[i]
        if BufferColors[i] == 1 and BufferColors[i + 1] != 1:
            BufferDN[i] = BufferHIST[i]
        if BufferColors[i] == 2 and BufferColors[i + 1] != 2:
            BufferNO[i] = BufferHIST[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Conqueror(_MQL5Indicator):
    name = 'Conqueror'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 10,  # Period
        'InpPeriodRange1': 10,  # Range 1 period
        'InpPeriodRange2': 40,  # Range 2 period
    }

