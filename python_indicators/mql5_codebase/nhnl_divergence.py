"""NHNL_Divergence — converted from MQL5: MQL5 Indicators/NHNL_Divergence/NHNL_Divergence.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16711680], 2: [255], 3: [32768], 4: [255], 5: [32768]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Long signal', 2: 'Short signal', 3: 'Line to up', 4: 'Line to down', 5: 'NHNL'}, 'levels': [], 'description': [], 'name': 'NHNL_Divergence', 'source': 'MQL5 Indicators/NHNL_Divergence/NHNL_Divergence.mq5', 'folder': 'NHNL_Divergence', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpColorBullish', 'py': 'InpColorBullish', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'Bullish color', 'sinput': False}, {'mql': 'InpColorBearish', 'py': 'InpColorBearish', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Bearish color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpColorBullish = _input('InpColorBullish', clrMediumSeaGreen)  # Bullish color
InpColorBearish = _input('InpColorBearish', clrOrange)  # Bearish color
BufferArrowToUP = Arr(0, 0.0)
BufferLineToUP = Arr(0, 0.0)
BufferArrowToDN = Arr(0, 0.0)
BufferLineToDN = Arr(0, 0.0)
BufferNHNL = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
prefix = ""
period = 0
handle_atr = 0

def OnInit():
    global handle_atr, period, prefix
    period = (1 if (InpPeriod < 1) else InpPeriod)
    prefix = 'nhnldiv'
    SetIndexBuffer(0, BufferArrowToUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferArrowToDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLineToUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLineToDN, INDICATOR_DATA)
    SetIndexBuffer(4, BufferNHNL, INDICATOR_DATA)
    SetIndexBuffer(5, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'NHNL Divergence')
    ArraySetAsSeries(BufferArrowToUP, True)
    ArraySetAsSeries(BufferArrowToDN, True)
    ArraySetAsSeries(BufferLineToUP, True)
    ArraySetAsSeries(BufferLineToDN, True)
    ArraySetAsSeries(BufferNHNL, True)
    ArraySetAsSeries(BufferATR, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, InpColorBullish)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, InpColorBearish)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, InpColorBullish)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, InpColorBearish)
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
    if rates_total < (period + 9) or Point() == 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - fmax(period + 2, 11)
        ArrayInitialize(BufferArrowToUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrowToDN, EMPTY_VALUE)
        ArrayInitialize(BufferLineToUP, EMPTY_VALUE)
        ArrayInitialize(BufferLineToDN, EMPTY_VALUE)
        ArrayInitialize(BufferNHNL, EMPTY_VALUE)
        ArrayInitialize(BufferATR, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferArrowToDN[i] = EMPTY_VALUE
        BufferArrowToUP[i] = BufferArrowToDN[i]
        BufferLineToDN[i] = BufferArrowToUP[i]
        BufferLineToUP[i] = BufferLineToDN[i]
        count_h = 0
        count_l = 0
        for n in range(0, period):
            if high[i + n] > high[i + n + 1]:
                count_h += 1
            if low[i + n] < low[i + n + 1]:
                count_l -= 1
        BufferNHNL[i] = count_h + count_l
        ProcessBullish(rates_total, high, low, time, i + 2)
        ProcessBearish(rates_total, high, low, time, i + 2)
    return rates_total

def IsTrough(rates_total, index):
    if (BufferNHNL[index] < 0 and BufferNHNL[index] < BufferNHNL[index + 1]) and BufferNHNL[index] < BufferNHNL[index - 1]:
        for n in range(index + 1, rates_total - 2):
            if BufferNHNL[n] > 0:
                return True
            elif BufferNHNL[index] > BufferNHNL[n]:
                return False
    return False

def PrevTrough(rates_total, index):
    for n in range(index + 5, rates_total - 3):
        if ((BufferNHNL[n] <= BufferNHNL[n + 1] and BufferNHNL[n] < BufferNHNL[n + 2]) and BufferNHNL[n] <= BufferNHNL[n - 1]) and BufferNHNL[n] < BufferNHNL[n - 2]:
            return n
    return WRONG_VALUE

def ProcessBullish(rates_total, high, low, time, index):
    if IsTrough(rates_total, index):
        curr = index
        prev = PrevTrough(rates_total, index)
        if prev != WRONG_VALUE:
            if BufferNHNL[curr] > BufferNHNL[prev] and low[curr] < low[prev]:
                DrawDivergence(high, low, time, prev, curr, True)
            elif BufferNHNL[curr] < BufferNHNL[prev] and low[curr] > low[prev]:
                DrawDivergence(high, low, time, prev, curr, True)

def IsPeak(rates_total, index):
    if (BufferNHNL[index] > 0 and BufferNHNL[index] > BufferNHNL[index + 1]) and BufferNHNL[index] > BufferNHNL[index - 1]:
        for n in range(index + 1, rates_total - 2):
            if BufferNHNL[n] < 0:
                return True
            elif BufferNHNL[index] < BufferNHNL[n]:
                return False
    return False

def PrevPeak(rates_total, index):
    for n in range(index + 5, rates_total - 3):
        if ((BufferNHNL[n] >= BufferNHNL[n + 1] and BufferNHNL[n] > BufferNHNL[n + 2]) and BufferNHNL[n] >= BufferNHNL[n - 1]) and BufferNHNL[n] > BufferNHNL[n - 2]:
            return n
    return WRONG_VALUE

def ProcessBearish(rates_total, high, low, time, index):
    if IsPeak(rates_total, index):
        curr = index
        prev = PrevPeak(rates_total, index)
        if prev != WRONG_VALUE:
            if BufferNHNL[curr] < BufferNHNL[prev] and high[curr] > high[prev]:
                DrawDivergence(high, low, time, prev, curr, False)
            elif BufferNHNL[curr] > BufferNHNL[prev] and high[curr] < high[prev]:
                DrawDivergence(high, low, time, prev, curr, False)

def DrawDivergence(high, low, time, first, second, bull_flag):
    obj_name = prefix + _str(time[first]) + '_' + _str(time[second])
    wnd = 0
    if ObjectFind(0, obj_name) < 0:
        wnd = ChartWindowFind()
        if wnd != WRONG_VALUE:
            if bull_flag:
                BufferArrowToUP[second] = BufferNHNL[second]
                for j in range(first, second - 1, -1):
                    BufferLineToUP[j] = EquationDirect(first, BufferNHNL[first], second, BufferNHNL[second], j)
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
                BufferArrowToDN[second] = BufferNHNL[second]
                for j in range(first, second - 1, -1):
                    BufferLineToDN[j] = EquationDirect(first, BufferNHNL[first], second, BufferNHNL[second], j)
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


class NHNLDivergence(_MQL5Indicator):
    name = 'NHNL_Divergence'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
    }

