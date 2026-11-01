"""Coral — converted from MQL5: MQL5 Indicators/Coral/Coral.mq5

Coral indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Coral'}, 'levels': [], 'description': ['Coral indicator'], 'name': 'Coral', 'source': 'MQL5 Indicators/Coral/Coral.mq5', 'folder': 'Coral', 'inputs': [{'mql': 'InpCoeff', 'py': 'InpCoeff', 'param': 'InpCoeff', 'type': 'double', 'default': 0.063492063492, 'label': 'Coefficient', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpCoeff = _input('InpCoeff', 0.063492063492)  # Coefficient
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferC = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferB1 = Arr(0, 0.0)
BufferB2 = Arr(0, 0.0)
BufferB3 = Arr(0, 0.0)
BufferB4 = Arr(0, 0.0)
BufferB5 = Arr(0, 0.0)
BufferB6 = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
coeff1 = 0.0
coeff2 = 0.0
handle_ma = 0

def OnInit():
    global coeff1, coeff2, handle_ma
    coeff1 = (0.0086 if (InpCoeff <= 0.0086) else 1 if (InpCoeff > 1) else InpCoeff)
    coeff2 = 1.0 - coeff1
    SetIndexBuffer(0, BufferC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferB1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferB2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferB3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferB4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferB5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferB6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Coral')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferC, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferB1, True)
    ArraySetAsSeries(BufferB2, True)
    ArraySetAsSeries(BufferB3, True)
    ArraySetAsSeries(BufferB4, True)
    ArraySetAsSeries(BufferB5, True)
    ArraySetAsSeries(BufferB6, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferC, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferB1, 0)
        ArrayInitialize(BufferB2, 0)
        ArrayInitialize(BufferB3, 0)
        ArrayInitialize(BufferB4, 0)
        ArrayInitialize(BufferB5, 0)
        ArrayInitialize(BufferB6, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferB6[i] = BufferMA[i]
            BufferB5[i] = BufferB6[i]
            BufferB4[i] = BufferB5[i]
            BufferB3[i] = BufferB4[i]
            BufferB2[i] = BufferB3[i]
            BufferB1[i] = BufferB2[i]
        else:
            BufferB1[i] = (coeff1 * BufferMA[i]) + (coeff2 * BufferB1[i + 1])
            BufferB2[i] = (coeff1 * BufferB1[i]) + (coeff2 * BufferB2[i + 1])
            BufferB3[i] = (coeff1 * BufferB2[i]) + (coeff2 * BufferB3[i + 1])
            BufferB4[i] = (coeff1 * BufferB3[i]) + (coeff2 * BufferB4[i + 1])
            BufferB5[i] = (coeff1 * BufferB4[i]) + (coeff2 * BufferB5[i + 1])
            BufferB6[i] = (coeff1 * BufferB5[i]) + (coeff2 * BufferB6[i + 1])
            BufferC[i] = (-0.064 * BufferB6[i]) + (0.672 * BufferB5[i]) - (2.352 * BufferB4[i]) + (2.744 * BufferB3[i])
            BufferColors[i] = (0 if (BufferC[i] > BufferC[i + 1]) else 1 if (BufferC[i] < BufferC[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Coral(_MQL5Indicator):
    name = 'Coral'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpCoeff': 0.063492063492,  # Coefficient
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

