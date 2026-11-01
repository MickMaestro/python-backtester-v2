"""Performance_Index — converted from MQL5: MQL5 Indicators/Performance_Index/Performance_Index.mq5

Performance Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Performance Idx'}, 'levels': [], 'description': ['Performance Index'], 'name': 'Performance_Index', 'source': 'MQL5 Indicators/Performance_Index/Performance_Index.mq5', 'folder': 'Performance_Index', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpSymbol', 'py': 'InpSymbol', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Instrument', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpSymbol = _input('InpSymbol', 'GBPUSD')  # Instrument
BufferPI = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferPr1 = Arr(0, 0.0)
BufferPr2 = Arr(0, 0.0)
period = 0
handle_ma1 = 0
handle_ma2 = 0
handle_pr1 = 0
handle_pr2 = 0

def OnInit():
    global handle_ma1, handle_ma2, handle_pr1, handle_pr2, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferPI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferPr1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferPr2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PIndex/' + InpSymbol + '(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPI, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferPr1, True)
    ArraySetAsSeries(BufferPr2, True)
    if not SymbolCheck(InpSymbol):
        return INIT_FAILED
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The ', Symbol(), ' iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(InpSymbol, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma2 == INVALID_HANDLE:
        Print('The ', InpSymbol, ' iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_pr1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_pr1 == INVALID_HANDLE:
        Print('The ', Symbol(), ' iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_pr2 = iMA(InpSymbol, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_pr2 == INVALID_HANDLE:
        Print('The ', InpSymbol, ' iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    bars2 = (rates_total if (InpSymbol == Symbol()) else Bars(InpSymbol, PERIOD_CURRENT))
    if rates_total < 4 or bars2 < 4:
        return 0
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferPI, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferPr1, 0)
        ArrayInitialize(BufferPr2, 0)
    limit_min = fmin(rates_total, bars2) - 1
    copied = 0
    count = (1 if (limit == 0) else limit_min)
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferMA2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_pr1, 0, 0, count, BufferPr1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_pr2, 0, 0, count, BufferPr2)
    if copied != count:
        return 0
    count = (limit if (limit == 0) else limit_min)
    for i in range(count, 0 - 1, -1):
        index = BarShift(InpSymbol, PERIOD_CURRENT, time[i], False)
        if index == WRONG_VALUE:
            continue
        MA1 = BufferMA1[i]
        MA2 = BufferMA2[i]
        Pr1 = BufferPr1[i]
        Pr2 = BufferPr2[i]
        BufferPI[i] = (_fdiv(Pr1 * MA2, Pr2 * MA1) if (MA2 != 0 and Pr2 != 0) else EMPTY_VALUE)
    return rates_total

def SymbolCheck(symbol_name):
    select = Box(0)
    ResetLastError()
    if not SymbolInfoInteger(symbol_name, SYMBOL_SELECT, select):
        err = GetLastError()
        Print('Error: ', err, ' Symbol ', symbol_name, ' does not exist')
        return False
    else:
        if select.v:
            return True
        ResetLastError()
        if not SymbolSelect(symbol_name, True):
            err = GetLastError()
            Print('Error selected ', symbol_name, ': ', err)
    return False

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PerformanceIndex(_MQL5Indicator):
    name = 'Performance_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

