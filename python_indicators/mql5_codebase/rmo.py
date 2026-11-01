"""RMO — converted from MQL5: MQL5 Indicators/RMO/RMO.mq5

Rahul Mohindar Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [32768], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'RMO', 2: 'Signal first', 3: 'Signal second'}, 'levels': [], 'description': ['Rahul Mohindar Oscillator'], 'name': 'RMO', 'source': 'MQL5 Indicators/RMO/RMO.mq5', 'folder': 'RMO', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 30, 'label': 'Period 1', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 30, 'label': 'Period 2', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 2, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_PRICE
OPEN = 2
HIGH = 3
LOW = 4
CLOSE = 1
_enum('ENUM_PRICE', {2: 'OPEN', 3: 'HIGH', 4: 'LOW', 1: 'CLOSE'})

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 30)  # Period 1
InpPeriod2 = _input('InpPeriod2', 30)  # Period 2
InpPrice = _input('InpPrice', OPEN)  # Applied price
BufferRMO = Arr(0, 0.0)
BufferSig1 = Arr(0, 0.0)
BufferSig2 = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_1 = 0
period_2 = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_1, period_2
    period_1 = (2 if (InpPeriod1 < 2) else InpPeriod1)
    period_2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    SetIndexBuffer(0, BufferRMO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSig1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSig2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RMO(' + _str(period_1) + ',' + _str(period_2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRMO, True)
    ArraySetAsSeries(BufferSig1, True)
    ArraySetAsSeries(BufferSig2, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, AppliedPrice())
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(AppliedPrice(), 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    period_max = fmax(10, fmax(period_1, period_2))
    if rates_total < period_max:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 11
        ArrayInitialize(BufferRMO, 0)
        ArrayInitialize(BufferSig1, 0)
        ArrayInitialize(BufferSig2, 0)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        x = BufferMA[i] - (((10 * BufferMA[i]) + (55 * BufferMA[i + 1]) + (165 * BufferMA[i + 2]) + (330 * BufferMA[i + 3]) + (462 * BufferMA[i + 4]) + (462 * BufferMA[i + 5]) + (330 * BufferMA[i + 6]) + (165 * BufferMA[i + 7]) + (55 * BufferMA[i + 8]) + (11 * BufferMA[i + 9]) + BufferMA[i + 10]) / 2046)
        bl = Lowest("", PERIOD_CURRENT, AppliedPrice(), 10, i)
        bh = Highest("", PERIOD_CURRENT, AppliedPrice(), 10, i)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            return 0
        MinPr = BufferMA[bl]
        MaxPr = BufferMA[bh]
        BufferRMO[i] = (_fdiv(100 * x, MaxPr - MinPr) if (MinPr != MaxPr) else 0)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_1, BufferRMO, BufferSig1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_2, BufferSig1, BufferSig2)
    return rates_total

def AppliedPrice():
    return InpPrice

def Highest(symbol_name, timeframe, price_type, count, start):
    if symbol_name == '' or symbol_name == "":
        symbol_name = Symbol()
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    _sw1 = price_type
    if _sw1 == PRICE_CLOSE:
        if CopyClose(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_OPEN:
        if CopyOpen(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_HIGH:
        if CopyHigh(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    elif _sw1 == PRICE_LOW:
        if CopyLow(symbol_name, timeframe, start, count, array) == count:
            return ArrayMaximum(array) + start
        return WRONG_VALUE
    else:
        return WRONG_VALUE
    return WRONG_VALUE

def Lowest(symbol_name, timeframe, price_type, count, start):
    if symbol_name == '' or symbol_name == "":
        symbol_name = Symbol()
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    _sw2 = price_type
    if _sw2 == PRICE_CLOSE:
        if CopyClose(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_OPEN:
        if CopyOpen(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_HIGH:
        if CopyHigh(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    elif _sw2 == PRICE_LOW:
        if CopyLow(symbol_name, timeframe, start, count, array) == count:
            return ArrayMinimum(array) + start
        return WRONG_VALUE
    else:
        return WRONG_VALUE
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RMO(_MQL5Indicator):
    name = 'RMO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 30,  # Period 1
        'InpPeriod2': 30,  # Period 2
        'InpPrice': _Choice({2: 'Open', 3: 'High', 4: 'Low', 1: 'Close'}, default=2),  # Applied price
    }

