"""CorrelationCoefficient — converted from MQL5: MQL5 Indicators/Correlation Coefficient/CorrelationCoefficient.mq5

Copyright: Copyright 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Correlation'}, 'levels': [], 'description': [], 'name': 'CorrelationCoefficient', 'source': 'MQL5 Indicators/Correlation Coefficient/CorrelationCoefficient.mq5', 'folder': 'Correlation Coefficient', 'inputs': [{'mql': 'InpSymbol', 'py': 'InpSymbol', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Symbol', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 1, 'label': 'Source', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSymbol = _input('InpSymbol', 'GBPUSD')  # Symbol
InpPrice = _input('InpPrice', PRICE_CLOSE)  # Source
InpPeriod = _input('InpPeriod', 20)  # Length
ExtBufferCorrelation = Arr(0, 0.0)
ExtBufferMA1 = Arr(0, 0.0)
ExtBufferMA2 = Arr(0, 0.0)
ExtHandleMA1 = 0
ExtHandleMA2 = 0
ExtPeriod = 0
ExtSymbol = ""

def OnInit():
    global ExtHandleMA1, ExtHandleMA2, ExtPeriod, ExtSymbol
    SetIndexBuffer(0, ExtBufferCorrelation, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtBufferMA2, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtBufferCorrelation, True)
    ArraySetAsSeries(ExtBufferMA1, True)
    ArraySetAsSeries(ExtBufferMA2, True)
    ExtPeriod = (1 if (InpPeriod < 1) else InpPeriod)
    ExtSymbol = InpSymbol
    if not CheckSymbol(ExtSymbol):
        PrintFormat("Since the symbol '%s' was not found, use current symbol '%s'", ExtSymbol, Symbol())
        ExtSymbol = Symbol()
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Correlation Coefficient (%s vs %s)', Symbol(), ExtSymbol))
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 1.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, -1.0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1.2)
    IndicatorSetDouble(INDICATOR_MINIMUM, -1.2)
    ResetLastError()
    ExtHandleMA1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpPrice)
    if ExtHandleMA1 == INVALID_HANDLE:
        PrintFormat('The First iMA(%s, %s) object was not created: Error %d', Symbol(), StringSubstr(EnumToString(InpPrice, 'ENUM_APPLIED_PRICE'), 6), GetLastError())
        return INIT_FAILED
    ExtHandleMA2 = iMA(ExtSymbol, PERIOD_CURRENT, 1, 0, MODE_SMA, InpPrice)
    if ExtHandleMA2 == INVALID_HANDLE:
        PrintFormat('The Second iMA(%s, %s) object was not created: Error %d', ExtSymbol, StringSubstr(EnumToString(InpPrice, 'ENUM_APPLIED_PRICE'), 6), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < ExtPeriod:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(ExtBufferCorrelation, EMPTY_VALUE)
        ArrayInitialize(ExtBufferMA1, 0)
        ArrayInitialize(ExtBufferMA2, 0)
    to_copy = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(ExtHandleMA1, 0, 0, to_copy, ExtBufferMA1)
    if copied != to_copy:
        return 0
    bars = (Bars(ExtSymbol, PERIOD_CURRENT) if (ExtSymbol != Symbol()) else rates_total)
    to_copy = (fmin(bars, limit) if (limit > 1) else 1)
    copied = CopyBuffer(ExtHandleMA2, 0, 0, to_copy, ExtBufferMA2)
    if copied < 1:
        return 0
    array_a = Arr(0, 0.0)
    array_b = Arr(0, 0.0)
    a = 0
    b = 0
    for i in range(limit, 0 - 1, -1):
        count = ExtPeriod
        if limit > 1 and (i + count) > limit:
            count = limit - i + 1
        if ArrayCopy(array_a, ExtBufferMA1, 0, i, count) != count or ArrayCopy(array_b, ExtBufferMA2, 0, i, count) != count:
            continue
        a.Swap(array_a)
        b.Swap(array_b)
        ExtBufferCorrelation[i] = a.CorrCoef(b)
    return rates_total

def CheckSymbol(symbol):
    is_custom = Box(False)
    if not SymbolExist(symbol, is_custom):
        return False
    if is_custom.v:
        PrintFormat("The symbol '%s' is custom", symbol)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrelationCoefficient(_MQL5Indicator):
    name = 'CorrelationCoefficient'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Source
        'InpPeriod': 20,  # Length
    }

