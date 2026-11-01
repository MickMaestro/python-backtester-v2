"""AO_Divergence — converted from MQL5: MQL5 Indicators/AO_Divergence/AO_Divergence.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768], 4: [255], 5: [32768]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Long signal', 2: 'Short signal', 3: 'Line to up', 4: 'Line to down', 5: 'AO'}, 'levels': [], 'description': [], 'name': 'AO_Divergence', 'source': 'MQL5 Indicators/AO_Divergence/AO_Divergence.mq5', 'folder': 'AO_Divergence', 'inputs': [{'mql': 'InpPeriodFastMA', 'py': 'InpPeriodFastMA', 'param': 'InpPeriodFastMA', 'type': 'uint', 'default': 5, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlowMA', 'py': 'InpPeriodSlowMA', 'param': 'InpPeriodSlowMA', 'type': 'uint', 'default': 34, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpColorBullish', 'py': 'InpColorBullish', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'Bullish color', 'sinput': False}, {'mql': 'InpColorBearish', 'py': 'InpColorBearish', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Bearish color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFastMA = _input('InpPeriodFastMA', 5)  # Fast MA period
InpPeriodSlowMA = _input('InpPeriodSlowMA', 34)  # Slow MA period
InpColorBullish = _input('InpColorBullish', clrMediumSeaGreen)  # Bullish color
InpColorBearish = _input('InpColorBearish', clrOrange)  # Bearish color
BufferArrowToUP = Arr(0, 0.0)
BufferLineToUP = Arr(0, 0.0)
BufferArrowToDN = Arr(0, 0.0)
BufferLineToDN = Arr(0, 0.0)
BufferAO = Arr(0, 0.0)
BufferFastMA = Arr(0, 0.0)
BufferSlowMA = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
prefix = ""
period_fast_ma = 0
period_slow_ma = 0
handle_fast_ma = 0
handle_slow_ma = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_fast_ma, handle_slow_ma, period_fast_ma, period_slow_ma, prefix
    period_fast_ma = (1 if (InpPeriodFastMA < 1) else InpPeriodFastMA)
    period_slow_ma = ((period_fast_ma + 1) if (_int(InpPeriodSlowMA) <= period_fast_ma) else InpPeriodSlowMA)
    prefix = 'aodiv'
    SetIndexBuffer(0, BufferArrowToUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferArrowToDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLineToUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLineToDN, INDICATOR_DATA)
    SetIndexBuffer(4, BufferAO, INDICATOR_DATA)
    SetIndexBuffer(5, BufferFastMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferSlowMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'AO Divergence')
    ArraySetAsSeries(BufferArrowToUP, True)
    ArraySetAsSeries(BufferArrowToDN, True)
    ArraySetAsSeries(BufferLineToUP, True)
    ArraySetAsSeries(BufferLineToDN, True)
    ArraySetAsSeries(BufferAO, True)
    ArraySetAsSeries(BufferFastMA, True)
    ArraySetAsSeries(BufferSlowMA, True)
    ArraySetAsSeries(BufferATR, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, InpColorBullish)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, InpColorBearish)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, InpColorBullish)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, InpColorBearish)
    ResetLastError()
    handle_fast_ma = iMA(Symbol(), PERIOD_CURRENT, period_fast_ma, 0, MODE_SMA, PRICE_MEDIAN)
    if handle_fast_ma == INVALID_HANDLE:
        Print('The Fast iMA object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_slow_ma = iMA(Symbol(), PERIOD_CURRENT, period_slow_ma, 0, MODE_SMA, PRICE_MEDIAN)
    if handle_slow_ma == INVALID_HANDLE:
        Print('The Slow iMA object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_atr = iATR(Symbol(), PERIOD_CURRENT, 14)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (period_slow_ma + 9) or Point() == 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    limit2 = limit
    if limit > 1:
        limit = rates_total - 1
        limit2 = limit - 10
        ArrayInitialize(BufferArrowToUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrowToDN, EMPTY_VALUE)
        ArrayInitialize(BufferLineToUP, EMPTY_VALUE)
        ArrayInitialize(BufferLineToDN, EMPTY_VALUE)
        ArrayInitialize(BufferAO, EMPTY_VALUE)
        ArrayInitialize(BufferFastMA, EMPTY_VALUE)
        ArrayInitialize(BufferSlowMA, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_fast_ma, 0, 0, count, BufferFastMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_slow_ma, 0, 0, count, BufferSlowMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferAO[i] = BufferFastMA[i] - BufferSlowMA[i]
    for i in range(limit2, 0 - 1, -1):
        BufferArrowToDN[i] = EMPTY_VALUE
        BufferArrowToUP[i] = BufferArrowToDN[i]
        BufferLineToDN[i] = BufferArrowToUP[i]
        BufferLineToUP[i] = BufferLineToDN[i]
        ProcessBullish(rates_total, high, low, time, i + 2)
        ProcessBearish(rates_total, high, low, time, i + 2)
    return rates_total

def IsTrough(rates_total, index):
    if (BufferAO[index] < 0 and BufferAO[index] < BufferAO[index + 1]) and BufferAO[index] < BufferAO[index - 1]:
        for n in range(index + 1, rates_total - 2):
            if BufferAO[n] > 0:
                return True
            elif BufferAO[index] > BufferAO[n]:
                return False
    return False

def PrevTrough(rates_total, index):
    for n in range(index + 5, rates_total - 3):
        if ((BufferAO[n] <= BufferAO[n + 1] and BufferAO[n] < BufferAO[n + 2]) and BufferAO[n] <= BufferAO[n - 1]) and BufferAO[n] < BufferAO[n - 2]:
            return n
    return WRONG_VALUE

def ProcessBullish(rates_total, high, low, time, index):
    if IsTrough(rates_total, index):
        curr = index
        prev = PrevTrough(rates_total, index)
        if prev != WRONG_VALUE:
            if BufferAO[curr] > BufferAO[prev] and low[curr] < low[prev]:
                DrawDivergence(high, low, time, prev, curr, True)
            elif BufferAO[curr] < BufferAO[prev] and low[curr] > low[prev]:
                DrawDivergence(high, low, time, prev, curr, True)

def IsPeak(rates_total, index):
    if (BufferAO[index] > 0 and BufferAO[index] > BufferAO[index + 1]) and BufferAO[index] > BufferAO[index - 1]:
        for n in range(index + 1, rates_total - 2):
            if BufferAO[n] < 0:
                return True
            elif BufferAO[index] < BufferAO[n]:
                return False
    return False

def PrevPeak(rates_total, index):
    for n in range(index + 5, rates_total - 3):
        if ((BufferAO[n] >= BufferAO[n + 1] and BufferAO[n] > BufferAO[n + 2]) and BufferAO[n] >= BufferAO[n - 1]) and BufferAO[n] > BufferAO[n - 2]:
            return n
    return WRONG_VALUE

def ProcessBearish(rates_total, high, low, time, index):
    if IsPeak(rates_total, index):
        curr = index
        prev = PrevPeak(rates_total, index)
        if prev != WRONG_VALUE:
            if BufferAO[curr] < BufferAO[prev] and high[curr] > high[prev]:
                DrawDivergence(high, low, time, prev, curr, False)
            elif BufferAO[curr] > BufferAO[prev] and high[curr] < high[prev]:
                DrawDivergence(high, low, time, prev, curr, False)

def DrawDivergence(high, low, time, first, second, bull_flag):
    obj_name = prefix + _str(time[first]) + '_' + _str(time[second])
    wnd = 0
    if ObjectFind(0, obj_name) < 0:
        wnd = ChartWindowFind()
        if wnd != WRONG_VALUE:
            if bull_flag:
                BufferArrowToUP[second] = BufferAO[second]
                for j in range(first, second - 1, -1):
                    BufferLineToUP[j] = EquationDirect(first, BufferAO[first], second, BufferAO[second], j)
                ObjectCreate(0, obj_name + '~', OBJ_TREND, 0, time[first], low[first], time[second], low[second])
                ObjectSetInteger(0, obj_name + '~', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_COLOR, InpColorBullish)
                ObjectSetString(0, obj_name + '~', OBJPROP_TOOLTIP, '\n')
                ObjectCreate(0, obj_name + '~A', OBJ_ARROW, 0, time[second], low[second])
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_COLOR, InpColorBullish)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_ARROWCODE, 241)
                ObjectSetString(0, obj_name + '~A', OBJPROP_TOOLTIP, 'Bullish signal: ' + TimeToString(time[second]))
            else:
                BufferArrowToDN[second] = BufferAO[second]
                for j in range(first, second - 1, -1):
                    BufferLineToDN[j] = EquationDirect(first, BufferAO[first], second, BufferAO[second], j)
                ObjectCreate(0, obj_name + '~', OBJ_TREND, 0, time[first], high[first], time[second], high[second])
                ObjectSetInteger(0, obj_name + '~', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_COLOR, InpColorBearish)
                ObjectSetString(0, obj_name + '~', OBJPROP_TOOLTIP, '\n')
                ObjectCreate(0, obj_name + '~A', OBJ_ARROW, 0, time[second], high[second] + BufferATR[second])
                ObjectSetInteger(0, obj_name + '~', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_COLOR, InpColorBearish)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_ARROWCODE, 242)
                ObjectSetString(0, obj_name + '~A', OBJPROP_TOOLTIP, 'Bearish signal: ' + TimeToString(time[second]))
            ObjectSetInteger(0, obj_name + '~', OBJPROP_RAY, False)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AODivergence(_MQL5Indicator):
    name = 'AO_Divergence'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMA': 5,  # Fast MA period
        'InpPeriodSlowMA': 34,  # Slow MA period
    }

