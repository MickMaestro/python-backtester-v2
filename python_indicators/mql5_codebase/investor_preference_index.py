"""Investor_Preference_Index — converted from MQL5: MQL5 Indicators/Investor_Preference_Index/Investor_Preference_Index.mq5

Investor preference index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'IPref Idx'}, 'levels': [], 'description': ['Investor preference index indicator'], 'name': 'Investor_Preference_Index', 'source': 'MQL5 Indicators/Investor_Preference_Index/Investor_Preference_Index.mq5', 'folder': 'Investor_Preference_Index', 'inputs': [{'mql': 'InpInstrument', 'py': 'InpInstrument', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': 'Instrument', 'sinput': False}, {'mql': 'InpPeriodROC', 'py': 'InpPeriodROC', 'param': 'InpPeriodROC', 'type': 'uint', 'default': 24, 'label': 'ROC period', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 15, 'label': 'Fast smoothing period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 38, 'label': 'Slow smoothing period', 'sinput': False}, {'mql': 'InpPeriodRes', 'py': 'InpPeriodRes', 'param': 'InpPeriodRes', 'type': 'uint', 'default': 54, 'label': 'Result smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpInstrument = _input('InpInstrument', 'USDJPY')  # Instrument
InpPeriodROC = _input('InpPeriodROC', 24)  # ROC period
InpPeriodFast = _input('InpPeriodFast', 15)  # Fast smoothing period
InpPeriodSlow = _input('InpPeriodSlow', 38)  # Slow smoothing period
InpPeriodRes = _input('InpPeriodRes', 54)  # Result smoothing period
BufferIPI = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferB1 = Arr(0, 0.0)
BufferB2 = Arr(0, 0.0)
BufferCloseI = Arr(0, 0.0)
period_roc = 0
period_fast = 0
period_slow = 0
period_res = 0
period_max = 0

def OnInit():
    global period_fast, period_max, period_res, period_roc, period_slow
    EventSetTimer(90)
    if not SymbolCheck(InpInstrument):
        return INIT_FAILED
    if InpInstrument == Symbol():
        Print('Error. The Instrument must not be the same as the current symbol.')
        return INIT_FAILED
    period_roc = (1 if (InpPeriodROC < 1) else InpPeriodROC)
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_res = (1 if (InpPeriodRes < 1) else InpPeriodRes)
    period_max = fmax(period_roc, fmax(period_fast, fmax(period_slow, period_res)))
    SetIndexBuffer(0, BufferIPI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferB1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferB2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferCloseI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Investor preference index (' + InpInstrument + ',' + _str(period_roc) + ',' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_res) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period_max)
    PlotIndexSetString(0, PLOT_LABEL, 'IPIdx(' + InpInstrument + ')')
    ArraySetAsSeries(BufferIPI, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferB1, True)
    ArraySetAsSeries(BufferB2, True)
    ArraySetAsSeries(BufferCloseI, True)
    Time(InpInstrument, 0)
    return INIT_SUCCEEDED

def OnTimer():
    Time(InpInstrument, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_roc - 1
        ArrayInitialize(BufferIPI, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferB1, 0)
        ArrayInitialize(BufferB2, 0)
        ArrayInitialize(BufferCloseI, 0)
    count = (Bars(InpInstrument, PERIOD_CURRENT) if (limit > 1) else 1)
    copied = 0
    copied = CopyClose(InpInstrument, PERIOD_CURRENT, 0, count, BufferCloseI)
    if copied < 1:
        return 0
    for i in range(limit, 0 - 1, -1):
        index1 = BarShift(InpInstrument, PERIOD_CURRENT, time[i])
        index2 = BarShift(InpInstrument, PERIOD_CURRENT, time[i + period_roc - 1])
        if index1 == WRONG_VALUE or index2 == WRONG_VALUE:
            continue
        roc1 = ROC(Symbol(), i, i + period_roc - 1)
        roc2 = ROC(InpInstrument, index1, index2)
        if roc1 == 0 or roc2 == 0:
            continue
        BufferB1[i] = roc1 - roc2
        BufferB2[i] = GetSMA(rates_total, i, period_fast, BufferB1) - GetSMA(rates_total, i, period_slow, BufferB1)
        BufferIPI[i] = 100.0 * ((period_res * GetSMA(rates_total, i, period_res, BufferB2)) + 1.0)
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
    return (array[0] if (CopyTime(symbol_name, PERIOD_CURRENT, shift, 1, array) == 1) else 0)

def Close(symbol_name, shift):
    array = Arr(0, 0.0)
    return (array[0] if (CopyClose(symbol_name, PERIOD_CURRENT, shift, 1, array) == 1) else WRONG_VALUE)

def ROC(symbol_name, index_1, index_2):
    pr1 = Close(symbol_name, index_1)
    pr2 = Close(symbol_name, index_2)
    if pr1 == WRONG_VALUE or pr2 == WRONG_VALUE:
        return 0.0
    Log2 = log(pr2)
    return (_fdiv(100.0 * log(pr1 - Log2), Log2) if (Log2 != 0) else 0)

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InvestorPreferenceIndex(_MQL5Indicator):
    name = 'Investor_Preference_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodROC': 24,  # ROC period
        'InpPeriodFast': 15,  # Fast smoothing period
        'InpPeriodSlow': 38,  # Slow smoothing period
        'InpPeriodRes': 54,  # Result smoothing period
    }

