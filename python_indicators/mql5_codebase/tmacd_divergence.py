"""TMACD_Divergence — converted from MQL5: MQL5 Indicators/TMACD_Divergence/TMACD_Divergence.mq5

TMACD Divergence indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 5}, 'types': {1: 10, 2: 5, 3: 5, 4: 1, 5: 1}, 'colors': {1: [32768, 255, 11119017], 2: [255], 3: [32768], 4: [32768], 5: [255]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'TMACD', 2: 'Short signal', 3: 'Long signal', 4: 'Line to up', 5: 'Line to down'}, 'levels': [], 'description': ['TMACD Divergence indicator'], 'name': 'TMACD_Divergence', 'source': 'MQL5 Indicators/TMACD_Divergence/TMACD_Divergence.mq5', 'folder': 'TMACD_Divergence', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 7, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 14, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color2 = 255  # #property indicator_color2
indicator_color3 = 32768  # #property indicator_color3

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 7)  # Fast MA period
InpPeriodSlow = _input('InpPeriodSlow', 14)  # Slow MA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTMACD = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferArrowToDN = Arr(0, 0.0)
BufferArrowToUP = Arr(0, 0.0)
BufferLineToUP = Arr(0, 0.0)
BufferLineToDN = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
prefix = ""
period_fast = 0
period_slow = 0
len_f = 0
len_s = 0
period_max = 0
handle_fma = 0
handle_sma = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_fma, handle_sma, len_f, len_s, period_fast, period_max, period_slow, prefix
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (_int(InpPeriodSlow) == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    prefix = 'tmacdiv'
    len_f = _int(floor(_idiv(period_fast, 2))) + 1
    len_s = _int(floor(_idiv(period_slow, 2))) + 1
    period_max = fmax(len_f, len_s)
    SetIndexBuffer(0, BufferTMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferArrowToDN, INDICATOR_DATA)
    SetIndexBuffer(3, BufferArrowToUP, INDICATOR_DATA)
    SetIndexBuffer(4, BufferLineToUP, INDICATOR_DATA)
    SetIndexBuffer(5, BufferLineToDN, INDICATOR_DATA)
    SetIndexBuffer(6, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferATR, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    PlotIndexSetInteger(2, PLOT_ARROW, 241)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TMACD Divergence (' + _str(period_fast) + ',' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferTMACD, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferArrowToDN, True)
    ArraySetAsSeries(BufferArrowToUP, True)
    ArraySetAsSeries(BufferLineToUP, True)
    ArraySetAsSeries(BufferLineToDN, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, len_f, 0, MODE_SMA, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(len_f), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, len_s, 0, MODE_SMA, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(len_s), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atr = iATR(None, PERIOD_CURRENT, 14)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < fmax(period_max, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 5
        ArrayInitialize(BufferTMACD, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferArrowToDN, EMPTY_VALUE)
        ArrayInitialize(BufferArrowToUP, EMPTY_VALUE)
        ArrayInitialize(BufferLineToUP, EMPTY_VALUE)
        ArrayInitialize(BufferLineToDN, EMPTY_VALUE)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferATR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        F_TMA = GetSMA(rates_total, i, len_f, BufferFMA)
        S_TMA = GetSMA(rates_total, i, len_s, BufferSMA)
        BufferTMACD[i] = _fdiv(F_TMA - S_TMA, Point())
    for i in range(limit, 0 - 1, -1):
        BufferArrowToDN[i] = EMPTY_VALUE
        BufferArrowToUP[i] = BufferArrowToDN[i]
        BufferLineToDN[i] = BufferArrowToUP[i]
        BufferLineToUP[i] = BufferLineToDN[i]
        ProcessBullish(rates_total, high, low, time, i + 2)
        ProcessBearish(rates_total, high, low, time, i + 2)
        BufferColors[i] = (0 if (BufferTMACD[i] > BufferTMACD[i + 1]) else 1 if (BufferTMACD[i] < BufferTMACD[i + 1]) else 2)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)

def IsTrough(rates_total, index):
    if (BufferTMACD[index] < 0 and BufferTMACD[index] < BufferTMACD[index + 1]) and BufferTMACD[index] < BufferTMACD[index - 1]:
        for n in range(index + 1, rates_total - 2):
            if BufferTMACD[n] > 0:
                return True
            elif BufferTMACD[index] > BufferTMACD[n]:
                return False
    return False

def PrevTrough(rates_total, index):
    for n in range(index + 5, rates_total - 3):
        if ((BufferTMACD[n] <= BufferTMACD[n + 1] and BufferTMACD[n] < BufferTMACD[n + 2]) and BufferTMACD[n] <= BufferTMACD[n - 1]) and BufferTMACD[n] < BufferTMACD[n - 2]:
            return n
    return WRONG_VALUE

def ProcessBullish(rates_total, high, low, time, index):
    if IsTrough(rates_total, index):
        curr = index
        prev = PrevTrough(rates_total, index)
        if prev != WRONG_VALUE:
            if BufferTMACD[curr] > BufferTMACD[prev] and low[curr] < low[prev]:
                DrawDivergence(high, low, time, prev, curr, True)
            elif BufferTMACD[curr] < BufferTMACD[prev] and low[curr] > low[prev]:
                DrawDivergence(high, low, time, prev, curr, True)

def IsPeak(rates_total, index):
    if (BufferTMACD[index] > 0 and BufferTMACD[index] > BufferTMACD[index + 1]) and BufferTMACD[index] > BufferTMACD[index - 1]:
        for n in range(index + 1, rates_total - 2):
            if BufferTMACD[n] < 0:
                return True
            elif BufferTMACD[index] < BufferTMACD[n]:
                return False
    return False

def PrevPeak(rates_total, index):
    for n in range(index + 5, rates_total - 3):
        if ((BufferTMACD[n] >= BufferTMACD[n + 1] and BufferTMACD[n] > BufferTMACD[n + 2]) and BufferTMACD[n] >= BufferTMACD[n - 1]) and BufferTMACD[n] > BufferTMACD[n - 2]:
            return n
    return WRONG_VALUE

def ProcessBearish(rates_total, high, low, time, index):
    if IsPeak(rates_total, index):
        curr = index
        prev = PrevPeak(rates_total, index)
        if prev != WRONG_VALUE:
            if BufferTMACD[curr] < BufferTMACD[prev] and high[curr] > high[prev]:
                DrawDivergence(high, low, time, prev, curr, False)
            elif BufferTMACD[curr] > BufferTMACD[prev] and high[curr] < high[prev]:
                DrawDivergence(high, low, time, prev, curr, False)

def DrawDivergence(high, low, time, first, second, bull_flag):
    obj_name = prefix + _str(time[first]) + '_' + _str(time[second])
    wnd = 0
    if ObjectFind(0, obj_name) < 0:
        wnd = ChartWindowFind()
        if wnd != WRONG_VALUE:
            if bull_flag:
                BufferArrowToUP[second] = BufferTMACD[second]
                for j in range(first, second - 1, -1):
                    BufferLineToUP[j] = EquationDirect(first, BufferTMACD[first], second, BufferTMACD[second], j)
                ObjectCreate(0, obj_name + '~', OBJ_TREND, 0, time[first], low[first], time[second], low[second])
                ObjectSetInteger(0, obj_name + '~', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_COLOR, indicator_color3)
                ObjectSetString(0, obj_name + '~', OBJPROP_TOOLTIP, '\n')
                ObjectCreate(0, obj_name + '~A', OBJ_ARROW, 0, time[second], low[second])
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_COLOR, indicator_color3)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_ARROWCODE, 241)
                ObjectSetString(0, obj_name + '~A', OBJPROP_TOOLTIP, 'Bullish signal: ' + TimeToString(time[second]))
            else:
                BufferArrowToDN[second] = BufferTMACD[second]
                for j in range(first, second - 1, -1):
                    BufferLineToDN[j] = EquationDirect(first, BufferTMACD[first], second, BufferTMACD[second], j)
                ObjectCreate(0, obj_name + '~', OBJ_TREND, 0, time[first], high[first], time[second], high[second])
                ObjectSetInteger(0, obj_name + '~', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_COLOR, indicator_color2)
                ObjectSetString(0, obj_name + '~', OBJPROP_TOOLTIP, '\n')
                ObjectCreate(0, obj_name + '~A', OBJ_ARROW, 0, time[second], high[second] + BufferATR[second])
                ObjectSetInteger(0, obj_name + '~', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_COLOR, indicator_color2)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_ARROWCODE, 242)
                ObjectSetString(0, obj_name + '~A', OBJPROP_TOOLTIP, 'Bearish signal: ' + TimeToString(time[second]))
            ObjectSetInteger(0, obj_name + '~', OBJPROP_RAY, False)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TMACDDivergence(_MQL5Indicator):
    name = 'TMACD_Divergence'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 7,  # Fast MA period
        'InpPeriodSlow': 14,  # Slow MA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

