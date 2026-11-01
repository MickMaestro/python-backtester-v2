"""Fibonacci Bollinger Bands — converted from MQL5: MQL5 Indicators/Converted from Pine Script - Fibonacci Bollinger Bands/Fibonacci Bollinger Bands.mq5

Convert Pine Script code for Fibonacci Bollinger Bands to MQL5
Copyright: Copyright 2024, Rama Destrian (vilraxq); Link: http://www.mql5.com/ru/users/vilraxq; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rama Destrian (vilraxq)', 'link': 'http://www.mql5.com/ru/users/vilraxq', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 13}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1}, 'colors': {1: [255], 2: [32768], 3: [16711680], 4: [0], 5: [0], 6: [0], 7: [0], 8: [0], 9: [0], 10: [0], 11: [0], 12: [0], 13: [0]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1}, 'styles': {}, 'labels': {1: 'Upper Band', 2: 'Lower Band', 3: 'Basis Line', 4: 'Upper Band : 0.764', 5: 'Upper Band : 0.618', 6: 'Upper Band : 0.5', 7: 'Upper Band : 0.382', 8: 'Upper Band : 0.236', 9: 'Lower Band : 0.764', 10: 'Lower Band : 0.618', 11: 'Lower Band : 0.5', 12: 'Lower Band : 0.382', 13: 'Lower Band : 0.236'}, 'levels': [], 'description': ['Convert Pine Script code for Fibonacci Bollinger Bands to MQL5'], 'name': 'Fibonacci Bollinger Bands', 'source': 'MQL5 Indicators/Converted from Pine Script - Fibonacci Bollinger Bands/Fibonacci Bollinger Bands.mq5', 'folder': 'Converted from Pine Script - Fibonacci Bollinger Bands', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 200, 'label': 'BB Period', 'sinput': False}, {'mql': 'Mult', 'py': 'Mult', 'param': 'Mult', 'type': 'double', 'default': 3.0, 'label': 'BB Multiplier', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 6, 'label': 'Stdev Source', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 200)  # BB Period
Mult = _input('Mult', 3.0)  # BB Multiplier
Applied_price = _input('Applied_price', PRICE_TYPICAL)  # Stdev Source
basisBuffer = Arr(0, 0.0)
upperBuffer = Arr(0, 0.0)
lowerBuffer = Arr(0, 0.0)
devValue = Arr(0, 0.0)
upper764 = Arr(0, 0.0)
upper618 = Arr(0, 0.0)
upper5 = Arr(0, 0.0)
upper382 = Arr(0, 0.0)
upper236 = Arr(0, 0.0)
lower764 = Arr(0, 0.0)
lower618 = Arr(0, 0.0)
lower5 = Arr(0, 0.0)
lower382 = Arr(0, 0.0)
lower236 = Arr(0, 0.0)
devHandle = 0

def OnInit():
    global devHandle
    SetIndexBuffer(0, upperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, lowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, basisBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, upper764, INDICATOR_DATA)
    SetIndexBuffer(4, upper618, INDICATOR_DATA)
    SetIndexBuffer(5, upper5, INDICATOR_DATA)
    SetIndexBuffer(6, upper382, INDICATOR_DATA)
    SetIndexBuffer(7, upper236, INDICATOR_DATA)
    SetIndexBuffer(8, lower764, INDICATOR_DATA)
    SetIndexBuffer(9, lower618, INDICATOR_DATA)
    SetIndexBuffer(10, lower5, INDICATOR_DATA)
    SetIndexBuffer(11, lower382, INDICATOR_DATA)
    SetIndexBuffer(12, lower236, INDICATOR_DATA)
    ArraySetAsSeries(basisBuffer, True)
    ArraySetAsSeries(upperBuffer, True)
    ArraySetAsSeries(lowerBuffer, True)
    ArraySetAsSeries(devValue, True)
    ArraySetAsSeries(upper764, True)
    ArraySetAsSeries(upper618, True)
    ArraySetAsSeries(upper5, True)
    ArraySetAsSeries(upper382, True)
    ArraySetAsSeries(upper236, True)
    ArraySetAsSeries(lower764, True)
    ArraySetAsSeries(lower618, True)
    ArraySetAsSeries(lower5, True)
    ArraySetAsSeries(lower382, True)
    ArraySetAsSeries(lower236, True)
    devHandle = iStdDev(Symbol(), PERIOD_CURRENT, Length, 0, MODE_SMA, Applied_price)
    if devHandle == INVALID_HANDLE:
        Print('Error creating StdDev handle')
        return INIT_FAILED
    return INIT_SUCCEEDED

def vwma(src, lengthVWMA, index):
    s1 = 0.0
    s2 = 0.0
    for i in range(index, MathMin(index + lengthVWMA, ArraySize(src))):
        vol = float(iVolume(Symbol(), PERIOD_CURRENT, i))
        if vol == 0:
            continue
        s1 += src[i] * vol
        s2 += vol
    return (0 if (s2 == 0) else _fdiv(s1, s2))

def OnCalculate(rates_total, prev_calculated, begin, price):
    ArraySetAsSeries(price, True)
    if CopyBuffer(devHandle, 0, 0, rates_total, devValue) <= 0 or ArraySize(devValue) < rates_total:
        Print('Failed to copy StdDev values or devValue array size mismatch')
        return prev_calculated
    limit = rates_total - prev_calculated
    if prev_calculated == 0:
        limit = rates_total - 2
    else:
        limit += 1
    if limit > (rates_total - 2):
        limit = rates_total - 2
    for i in range(limit, 0 - 1, -1):
        basis = vwma(price, Length, i)
        if basis == 0 or basis == EMPTY_VALUE:
            basisBuffer[i] = EMPTY_VALUE
            upperBuffer[i] = EMPTY_VALUE
            lowerBuffer[i] = EMPTY_VALUE
            upper236[i] = EMPTY_VALUE
            lower236[i] = EMPTY_VALUE
            continue
        basisBuffer[i] = basis
        dev = devValue[i]
        if dev == EMPTY_VALUE or dev <= 0:
            basisBuffer[i] = EMPTY_VALUE
            upperBuffer[i] = EMPTY_VALUE
            lowerBuffer[i] = EMPTY_VALUE
            upper236[i] = EMPTY_VALUE
            lower236[i] = EMPTY_VALUE
            continue
        upperBuffer[i] = basis + (Mult * dev)
        lowerBuffer[i] = basis - (Mult * dev)
        upper236[i] = basis + (Mult * dev * 0.236)
        upper382[i] = basis + (Mult * dev * 0.382)
        upper5[i] = basis + (Mult * dev * 0.5)
        upper618[i] = basis + (Mult * dev * 0.618)
        upper764[i] = basis + (Mult * dev * 0.764)
        lower236[i] = basis - (Mult * dev * 0.236)
        lower382[i] = basis - (Mult * dev * 0.382)
        lower5[i] = basis - (Mult * dev * 0.5)
        lower618[i] = basis - (Mult * dev * 0.618)
        lower764[i] = basis - (Mult * dev * 0.764)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FibonacciBollingerBands(_MQL5Indicator):
    name = 'Fibonacci Bollinger Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 200,  # BB Period
        'Mult': 3.0,  # BB Multiplier
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Stdev Source
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

