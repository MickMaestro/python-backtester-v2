"""Trend_Force — converted from MQL5: MQL5 Indicators/Trend_Force/Trend_Force.mq5

Trend force oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 42495, 255, 36095]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TForce'}, 'levels': [], 'description': ['Trend force oscillator'], 'name': 'Trend_Force', 'source': 'MQL5 Indicators/Trend_Force/Trend_Force.mq5', 'folder': 'Trend_Force', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 12, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 7, 'label': "ATR's period", 'sinput': False}, {'mql': 'InpCoeffATR', 'py': 'InpCoeffATR', 'param': 'InpCoeffATR', 'type': 'double', 'default': 2.0, 'label': "ATR's coefficient", 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 12)  # Period
InpPeriodATR = _input('InpPeriodATR', 7)  # ATR's period
InpCoeffATR = _input('InpCoeffATR', 2.0)  # ATR's coefficient
BufferTF = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMin = Arr(0, 0.0)
BufferMax = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
coeff = 0.0
period = 0
period_atr = 0
handle_atr = 0

def OnInit():
    global coeff, handle_atr, period, period_atr
    period = (1 if (InpPeriod < 1) else InpPeriod)
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    coeff = InpCoeffATR
    SetIndexBuffer(0, BufferTF, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMin, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMax, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TForce(' + _str(period) + ',' + _str(period_atr) + ',' + DoubleToString(coeff, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTF, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMin, True)
    ArraySetAsSeries(BufferMax, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period or Point() == 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTF, EMPTY_VALUE)
        ArrayInitialize(BufferMin, 0)
        ArrayInitialize(BufferMax, 0)
        ArrayInitialize(BufferATR, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        bh = Highest(period_atr, i)
        bl = Lowest(period_atr, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        BufferMin[i] = high[bh] - (coeff * BufferATR[i])
        BufferMax[i] = low[bl] + (coeff * BufferATR[i])
    Up = 0.0
    Dn = 0.0
    for i in range(limit, 0 - 1, -1):
        bh = ArrayMaximum(BufferMin, i, period)
        bl = ArrayMinimum(BufferMax, i, period)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        Up = BufferMin[bh]
        Dn = BufferMax[bl]
        BufferTF[i] = _fdiv(Up - Dn, Point())
        if BufferTF[i] > 0:
            BufferColors[i] = (0 if (BufferTF[i] > BufferTF[i + 1]) else 1)
        else:
            BufferColors[i] = (2 if (BufferTF[i] < BufferTF[i + 1]) else 3)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendForce(_MQL5Indicator):
    name = 'Trend_Force'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 12,  # Period
        'InpPeriodATR': 7,  # ATR's period
        'InpCoeffATR': 2.0,  # ATR's coefficient
    }

