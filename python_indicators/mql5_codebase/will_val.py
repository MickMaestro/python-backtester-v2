"""WILL_VAL — converted from MQL5: MQL5 Indicators/WILL_VAL/WILL_VAL.mq5

Larry Williams' WILL VAL oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13458026]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'WV'}, 'levels': [], 'description': ["Larry Williams' WILL VAL oscillator"], 'name': 'WILL_VAL', 'source': 'MQL5 Indicators/WILL_VAL/WILL_VAL.mq5', 'folder': 'WILL_VAL', 'inputs': [{'mql': 'InpInstrument', 'py': 'InpInstrument', 'param': None, 'type': 'string', 'default': 'EURJPY', 'label': 'Instrument', 'sinput': False}, {'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 22, 'label': 'First EMA period', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 2, 'label': 'Second EMA period', 'sinput': False}, {'mql': 'InpPeriod3', 'py': 'InpPeriod3', 'param': 'InpPeriod3', 'type': 'uint', 'default': 365, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 75.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 25.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpInstrument = _input('InpInstrument', 'EURJPY')  # Instrument
InpPeriod1 = _input('InpPeriod1', 22)  # First EMA period
InpPeriod2 = _input('InpPeriod2', 2)  # Second EMA period
InpPeriod3 = _input('InpPeriod3', 365)  # Period
InpOverbought = _input('InpOverbought', 75.0)  # Overbought
InpOversold = _input('InpOversold', 25.0)  # Oversold
BufferWV = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
BufferValue = Arr(0, 0.0)
BufferAvgPrice1 = Arr(0, 0.0)
BufferAvgPrice2 = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_1 = 0
period_2 = 0
period_3 = 0
period_max = 0

def OnInit():
    global overbought, oversold, period_1, period_2, period_3, period_max
    EventSetTimer(90)
    if not SymbolCheck(InpInstrument):
        return INIT_FAILED
    if InpInstrument == Symbol():
        Print('Error. The Instrument must not be the same as the current symbol.')
        return INIT_FAILED
    period_1 = (2 if (InpPeriod1 < 2) else InpPeriod1)
    period_2 = ((period_1 + 1) if (InpPeriod2 == period_1) else 2 if (InpPeriod2 < 2) else InpPeriod2)
    period_3 = (1 if (InpPeriod3 < 1) else InpPeriod3)
    period_max = fmax(period_1, fmax(period_2, period_3))
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferWV, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferAvgPrice1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAvgPrice2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferValue, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WILL VAL (' + InpInstrument + ',' + _str(period_1) + ',' + _str(period_2) + ',' + _str(period_3) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetString(0, PLOT_LABEL, 'WV(' + InpInstrument + ')')
    ArraySetAsSeries(BufferWV, True)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferAvgPrice1, True)
    ArraySetAsSeries(BufferAvgPrice2, True)
    ArraySetAsSeries(BufferValue, True)
    Time(InpInstrument, 0)
    return INIT_SUCCEEDED

def OnTimer():
    Time(InpInstrument, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferWV, EMPTY_VALUE)
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferAvgPrice1, 0)
        ArrayInitialize(BufferAvgPrice2, 0)
        ArrayInitialize(BufferValue, 0)
    for i in range(limit, 0 - 1, -1):
        j = BarShift(InpInstrument, PERIOD_CURRENT, time[i])
        if j == WRONG_VALUE:
            continue
        price = Close(InpInstrument, j)
        BufferPrice[i] = _fdiv(close[i], (price if (price != WRONG_VALUE) else 1.0))
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_1, BufferPrice, BufferAvgPrice1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_2, BufferPrice, BufferAvgPrice2) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferValue[i] = BufferAvgPrice1[i] - BufferAvgPrice2[i]
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferValue, i, period_3)
        bh = ArrayMaximum(BufferValue, i, period_3)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferValue[bl]
        max_ = BufferValue[bh]
        BufferWV[i] = (_fdiv(100.0 * (BufferValue[i] - min_), max_ - min_) if (max_ != min_) else 0)
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

def Time(symbol_name, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, PERIOD_CURRENT, shift, 1, array) == 1) else 0)

def Close(symbol_name, shift):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyClose(symbol_name, PERIOD_CURRENT, shift, 1, array) == 1) else WRONG_VALUE)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WILLVAL(_MQL5Indicator):
    name = 'WILL_VAL'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 22,  # First EMA period
        'InpPeriod2': 2,  # Second EMA period
        'InpPeriod3': 365,  # Period
        'InpOverbought': 75.0,  # Overbought
        'InpOversold': 25.0,  # Oversold
    }

