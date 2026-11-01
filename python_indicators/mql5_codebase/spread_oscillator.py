"""Spread_Oscillator — converted from MQL5: MQL5 Indicators/Spread_Oscillator/Spread_Oscillator.mq5

Spread Oscillator
Shows the spread between two instruments
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Spread Osc'}, 'levels': [], 'description': ['Spread Oscillator', 'Shows the spread between two instruments'], 'name': 'Spread_Oscillator', 'source': 'MQL5 Indicators/Spread_Oscillator/Spread_Oscillator.mq5', 'folder': 'Spread_Oscillator', 'inputs': [{'mql': 'InpSymbol1', 'py': 'InpSymbol1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'First symbol', 'sinput': False}, {'mql': 'InpSymbol2', 'py': 'InpSymbol2', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Second symbol', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 5, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 15, 'label': 'Slow MA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSymbol1 = _input('InpSymbol1', 'EURUSD')  # First symbol
InpSymbol2 = _input('InpSymbol2', 'GBPUSD')  # Second symbol
InpPeriodFast = _input('InpPeriodFast', 5)  # Fast MA period
InpPeriodSlow = _input('InpPeriodSlow', 15)  # Slow MA period
BufferSO = Arr(0, 0.0)
BufferRatio = Arr(0, 0.0)
BufferAvgFMA = Arr(0, 0.0)
BufferAvgSMA = Arr(0, 0.0)
BufferSymbol1 = Arr(0, 0.0)
BufferSymbol2 = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_max = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_ma1, handle_ma2, period_fast, period_max, period_slow
    period_fast = (2 if (InpPeriodFast < 2) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 2 if (InpPeriodSlow < 2) else InpPeriodSlow)
    period_max = fmax(period_fast, period_slow)
    if not SymbolCheck(InpSymbol1):
        return INIT_FAILED
    if not SymbolCheck(InpSymbol2):
        return INIT_FAILED
    Time(InpSymbol1, PERIOD_CURRENT, 1)
    Time(InpSymbol2, PERIOD_CURRENT, 1)
    SetIndexBuffer(0, BufferSO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRatio, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferAvgFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAvgSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSymbol1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSymbol2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, InpSymbol1 + '/' + InpSymbol2 + ' spread (' + _str(period_fast) + ', ' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSO, True)
    ArraySetAsSeries(BufferRatio, True)
    ArraySetAsSeries(BufferAvgFMA, True)
    ArraySetAsSeries(BufferAvgSMA, True)
    ArraySetAsSeries(BufferSymbol1, True)
    ArraySetAsSeries(BufferSymbol2, True)
    ResetLastError()
    handle_ma1 = iMA(InpSymbol1, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma1 == INVALID_HANDLE:
        Print('The ', InpSymbol1, ' iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(InpSymbol2, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_CLOSE)
    if handle_ma2 == INVALID_HANDLE:
        Print('The ', InpSymbol2, ' iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferSO, 0)
        ArrayInitialize(BufferRatio, 0)
        ArrayInitialize(BufferAvgFMA, 0)
        ArrayInitialize(BufferAvgSMA, 0)
        ArrayInitialize(BufferSymbol1, 0)
        ArrayInitialize(BufferSymbol2, 0)
    if Time(InpSymbol1, PERIOD_CURRENT, 1) == 0:
        return 0
    if Time(InpSymbol2, PERIOD_CURRENT, 1) == 0:
        return 0
    bars1 = (rates_total if (InpSymbol1 == Symbol()) else Bars(InpSymbol1, PERIOD_CURRENT))
    bars2 = (rates_total if (InpSymbol2 == Symbol()) else Bars(InpSymbol2, PERIOD_CURRENT))
    if bars1 == 0 or bars2 == 0:
        return 0
    count1 = (fmin(bars1, rates_total) if (limit > 1) else 1)
    copied = 0
    count2 = (fmin(bars2, rates_total) if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma1, 0, 0, count1, BufferSymbol1)
    if copied != count1:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count2, BufferSymbol2)
    if copied != count2:
        return 0
    for i in range(limit, 0 - 1, -1):
        if BufferSymbol1[i] == 0 or BufferSymbol2[i] == 0:
            continue
        res = (_fdiv(BufferSymbol1[i], BufferSymbol2[i]) if (BufferSymbol1[i] > BufferSymbol2[i]) else _fdiv(BufferSymbol2[i], BufferSymbol1[i]))
        BufferRatio[i] = res * 100.0
        BufferAvgFMA[i] = EMA(bars1, BufferRatio[i], BufferAvgFMA[i + 1], period_fast, i)
        BufferAvgSMA[i] = EMA(bars2, BufferRatio[i], BufferAvgSMA[i + 1], period_slow, i)
        BufferSO[i] = ((BufferAvgSMA[i] - BufferAvgFMA[i]) if (BufferSymbol1[i] > BufferSymbol2[i]) else (BufferAvgFMA[i] - BufferAvgSMA[i]))
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

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def EMA(rates_total, price, prev, period, shift):
    return (price if (shift >= (rates_total - 2) or period < 1) else (prev + (_fdiv(2.0, 1 + period) * (price - prev))))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpreadOscillator(_MQL5Indicator):
    name = 'Spread_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 5,  # Fast MA period
        'InpPeriodSlow': 15,  # Slow MA period
    }

