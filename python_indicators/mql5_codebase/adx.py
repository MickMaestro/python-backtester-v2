"""ADX — converted from MQL5: MQL5 Indicators/ADX Indicator (MQL5)/ADX.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: https://www.metaquotes.net; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'https://www.metaquotes.net', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [9109504], 2: [2237106], 3: [25600]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Di Plus', 2: 'Di Minus', 3: 'ADX'}, 'levels': [25.0], 'description': [], 'name': 'ADX', 'source': 'MQL5 Indicators/ADX Indicator (MQL5)/ADX.mq5', 'folder': 'ADX Indicator (MQL5)', 'inputs': [{'mql': 'per', 'py': 'per', 'param': 'per', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'alpha1', 'py': 'alpha1', 'param': 'alpha1', 'type': 'double', 'default': 0.25, 'label': 'Alpha1 Smoothing', 'sinput': False}, {'mql': 'alpha2', 'py': 'alpha2', 'param': 'alpha2', 'type': 'double', 'default': 0.33, 'label': 'Alpha2 Smoothing', 'sinput': False}, {'mql': 'PriceType', 'py': 'PriceType', 'param': 'PriceType', 'type': 'int', 'default': 1, 'label': 'Price Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
per = _input('per', 14)  # Period
alpha1 = _input('alpha1', 0.25)  # Alpha1 Smoothing
alpha2 = _input('alpha2', 0.33)  # Alpha2 Smoothing
PriceType = _input('PriceType', PRICE_CLOSE)  # Price Type
DiPlusFinal = Arr(0, 0.0)
DiMinusFinal = Arr(0, 0.0)
ADXFinal = Arr(0, 0.0)
DIPlusLead = Arr(0, 0.0)
DIMinusLead = Arr(0, 0.0)
ADXLead = Arr(0, 0.0)
adx_handle = 0

def OnInit():
    global adx_handle
    SetIndexBuffer(0, DiPlusFinal, INDICATOR_DATA)
    SetIndexBuffer(1, DiMinusFinal, INDICATOR_DATA)
    SetIndexBuffer(2, ADXFinal, INDICATOR_DATA)
    SetIndexBuffer(3, DIPlusLead, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, DIMinusLead, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ADXLead, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(DiPlusFinal, True)
    ArraySetAsSeries(DiMinusFinal, True)
    ArraySetAsSeries(ADXFinal, True)
    ArraySetAsSeries(DIPlusLead, True)
    ArraySetAsSeries(DIMinusLead, True)
    ArraySetAsSeries(ADXLead, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ADX(' + _str(per) + ') Smoothed')
    adx_handle = iADX(Symbol(), Period(), per)
    if adx_handle == INVALID_HANDLE:
        Print('Failed to create ADX handle')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if adx_handle != INVALID_HANDLE:
        IndicatorRelease(adx_handle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= (per + 1):
        return 0
    start = 0
    if prev_calculated == 0:
        ArrayInitialize(DiPlusFinal, 0.0)
        ArrayInitialize(DiMinusFinal, 0.0)
        ArrayInitialize(ADXFinal, 0.0)
        ArrayInitialize(DIPlusLead, 0.0)
        ArrayInitialize(DIMinusLead, 0.0)
        ArrayInitialize(ADXLead, 0.0)
        start = rates_total - per - 1
    else:
        start = rates_total - prev_calculated
    if start < 0:
        start = 0
    if start > (rates_total - 2):
        start = rates_total - 2
    plus_di = Arr(0, 0.0)
    minus_di = Arr(0, 0.0)
    adx = Arr(0, 0.0)
    ArrayResize(plus_di, rates_total)
    ArrayResize(minus_di, rates_total)
    ArrayResize(adx, rates_total)
    ArraySetAsSeries(plus_di, True)
    ArraySetAsSeries(minus_di, True)
    ArraySetAsSeries(adx, True)
    if CopyBuffer(adx_handle, 1, 0, rates_total, plus_di) <= 0:
        Print('Failed to copy +DI data')
        return prev_calculated
    if CopyBuffer(adx_handle, 2, 0, rates_total, minus_di) <= 0:
        Print('Failed to copy -DI data')
        return prev_calculated
    if CopyBuffer(adx_handle, 0, 0, rates_total, adx) <= 0:
        Print('Failed to copy ADX data')
        return prev_calculated
    for i in range(start, 0 - 1, -1):
        if (i + 1) >= rates_total:
            continue
        DIPlusLead[i] = (2 * plus_di[i]) + ((alpha1 - 2) * plus_di[i + 1]) + ((1 - alpha1) * DIPlusLead[i + 1])
        DIMinusLead[i] = (2 * minus_di[i]) + ((alpha1 - 2) * minus_di[i + 1]) + ((1 - alpha1) * DIMinusLead[i + 1])
        ADXLead[i] = (2 * adx[i]) + ((alpha1 - 2) * adx[i + 1]) + ((1 - alpha1) * ADXLead[i + 1])
    for i in range(start, 0 - 1, -1):
        if (i + 1) >= rates_total:
            continue
        DiPlusFinal[i] = (alpha2 * DIPlusLead[i]) + ((1 - alpha2) * DiPlusFinal[i + 1])
        DiMinusFinal[i] = (alpha2 * DIMinusLead[i]) + ((1 - alpha2) * DiMinusFinal[i + 1])
        ADXFinal[i] = (alpha2 * ADXLead[i]) + ((1 - alpha2) * ADXFinal[i + 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADX(_MQL5Indicator):
    name = 'ADX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'per': 14,  # Period
        'alpha1': 0.25,  # Alpha1 Smoothing
        'alpha2': 0.33,  # Alpha2 Smoothing
        'PriceType': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price Type
    }

