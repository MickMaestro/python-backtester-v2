"""Repulse_Divergence — converted from MQL5: MQL5 Indicators/Repulse_Divergence/Repulse_Divergence.mq5

Repulse Divergence
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 16, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [16711680], 2: [255], 3: [16711680], 4: [255], 5: [32768], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Long signal', 2: 'Short signal', 3: 'Line to up', 4: 'Line to down', 5: 'Repulse line', 6: 'Signal line'}, 'levels': [], 'description': ['Repulse Divergence'], 'name': 'Repulse_Divergence', 'source': 'MQL5 Indicators/Repulse_Divergence/Repulse_Divergence.mq5', 'folder': 'Repulse_Divergence', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 5, 'label': 'Repulse period', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 15, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpRepulseLine', 'py': 'InpRepulseLine', 'param': 'InpRepulseLine', 'type': 'int', 'default': 0, 'label': 'Repulse line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

indicator_color1 = 16711680  # #property indicator_color1
indicator_color2 = 255  # #property indicator_color2
indicator_color3 = 16711680  # #property indicator_color3
indicator_color4 = 255  # #property indicator_color4

# enum ENUM_MODE_LINE
MODE_LINE_MAIN = 0
MODE_LINE_SIGNAL = 1
_enum('ENUM_MODE_LINE', {0: 'MODE_LINE_MAIN', 1: 'MODE_LINE_SIGNAL'})

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 5)  # Repulse period
InpPeriod2 = _input('InpPeriod2', 15)  # Signal period
InpRepulseLine = _input('InpRepulseLine', MODE_LINE_MAIN)  # Repulse line
BufferArrowToUP = Arr(0, 0.0)
BufferLineToUP = Arr(0, 0.0)
BufferArrowToDN = Arr(0, 0.0)
BufferLineToDN = Arr(0, 0.0)
BufferRP1 = Arr(0, 0.0)
BufferRP2 = Arr(0, 0.0)
BufferPos1 = Arr(0, 0.0)
BufferNeg1 = Arr(0, 0.0)
BufferPos2 = Arr(0, 0.0)
BufferNeg2 = Arr(0, 0.0)
BufferPos1tmp = Arr(0, 0.0)
BufferNeg1tmp = Arr(0, 0.0)
BufferPos2tmp = Arr(0, 0.0)
BufferNeg2tmp = Arr(0, 0.0)
BufferDivRepulse = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
prefix = ""
period1 = 0
period2 = 0
handle_atr = 0

def OnInit():
    global handle_atr, period1, period2, prefix
    period1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    prefix = 'repulsediv'
    SetIndexBuffer(0, BufferArrowToUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferArrowToDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLineToUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferLineToDN, INDICATOR_DATA)
    SetIndexBuffer(4, BufferRP1, INDICATOR_DATA)
    SetIndexBuffer(5, BufferRP2, INDICATOR_DATA)
    SetIndexBuffer(6, BufferPos1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferNeg1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferPos2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferNeg2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferDivRepulse, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferPos1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferNeg1tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferPos2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, BufferNeg2tmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(15, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Repulse Divergence(' + _str(period1) + ',' + _str(period2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, indicator_color1)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, indicator_color2)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, indicator_color3)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, indicator_color4)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferArrowToUP, True)
    ArraySetAsSeries(BufferArrowToDN, True)
    ArraySetAsSeries(BufferLineToUP, True)
    ArraySetAsSeries(BufferLineToDN, True)
    ArraySetAsSeries(BufferDivRepulse, True)
    ArraySetAsSeries(BufferRP1, True)
    ArraySetAsSeries(BufferRP2, True)
    ArraySetAsSeries(BufferPos1, True)
    ArraySetAsSeries(BufferNeg1, True)
    ArraySetAsSeries(BufferPos2, True)
    ArraySetAsSeries(BufferNeg2, True)
    ArraySetAsSeries(BufferPos1tmp, True)
    ArraySetAsSeries(BufferNeg1tmp, True)
    ArraySetAsSeries(BufferPos2tmp, True)
    ArraySetAsSeries(BufferNeg2tmp, True)
    ArraySetAsSeries(BufferATR, True)
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
    if rates_total < 4 or Point() == 0:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    max_ = fmax(4, fmax(period1, period2))
    if limit > 1:
        limit = rates_total - max_ - 1
        ArrayInitialize(BufferArrowToUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrowToDN, EMPTY_VALUE)
        ArrayInitialize(BufferLineToUP, EMPTY_VALUE)
        ArrayInitialize(BufferLineToDN, EMPTY_VALUE)
        ArrayInitialize(BufferDivRepulse, 0)
        ArrayInitialize(BufferATR, 0)
        ArrayInitialize(BufferRP1, EMPTY_VALUE)
        ArrayInitialize(BufferRP2, EMPTY_VALUE)
        ArrayInitialize(BufferPos1, 0)
        ArrayInitialize(BufferNeg1, 0)
        ArrayInitialize(BufferPos2, 0)
        ArrayInitialize(BufferNeg2, 0)
        ArrayInitialize(BufferPos1tmp, 0)
        ArrayInitialize(BufferNeg1tmp, 0)
        ArrayInitialize(BufferPos2tmp, 0)
        ArrayInitialize(BufferNeg2tmp, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    MinPrice = 0.0
    MaxPrice = 0.0
    bl = WRONG_VALUE
    bh = WRONG_VALUE
    for i in range(limit, 0 - 1, -1):
        if close[i] == 0:
            continue
        bl = Lowest(period1, i)
        bh = Highest(period1, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        MinPrice = low[bl]
        MaxPrice = high[bh]
        BufferPos1tmp[i] = _fdiv(100.0 * ((3.0 * close[i]) - (2.0 * MinPrice) - open[i]), close[i])
        BufferNeg1tmp[i] = _fdiv(100.0 * (open[i] + (2.0 * MaxPrice) - (3.0 * close[i])), close[i])
        bl = Lowest(period2, i)
        bh = Highest(period2, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        MinPrice = low[bl]
        MaxPrice = high[bh]
        BufferPos2tmp[i] = _fdiv(100.0 * ((3.0 * close[i]) - (2.0 * MinPrice) - open[i + period2]), close[i])
        BufferNeg2tmp[i] = _fdiv(100.0 * (open[i + period2] + (2.0 * MaxPrice) - (3.0 * close[i])), close[i])
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 5 * period1, BufferPos1tmp, BufferPos1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 5 * period1, BufferNeg1tmp, BufferNeg1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 5 * period2, BufferPos2tmp, BufferPos2)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, 5 * period2, BufferNeg2tmp, BufferNeg2)
    for i in range(limit, 0 - 1, -1):
        BufferRP1[i] = _fdiv(BufferPos1[i] - BufferNeg1[i], Point())
        BufferRP2[i] = _fdiv(BufferPos2[i] - BufferNeg2[i], Point())
        BufferDivRepulse[i] = (BufferRP1[i] if (not InpRepulseLine) else BufferRP2[i])
    for i in range(limit, 0 - 1, -1):
        BufferArrowToDN[i] = EMPTY_VALUE
        BufferArrowToUP[i] = BufferArrowToDN[i]
        BufferLineToDN[i] = BufferArrowToUP[i]
        BufferLineToUP[i] = BufferLineToDN[i]
        ProcessBullish(rates_total, high, low, time, i + 2)
        ProcessBearish(rates_total, high, low, time, i + 2)
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE

def IsTrough(rates_total, index):
    if (BufferDivRepulse[index] < 0 and BufferDivRepulse[index] < BufferDivRepulse[index + 1]) and BufferDivRepulse[index] < BufferDivRepulse[index - 1]:
        for n in range(index + 1, rates_total - 2):
            if BufferDivRepulse[n] > 0:
                return True
            elif BufferDivRepulse[index] > BufferDivRepulse[n]:
                return False
    return False

def PrevTrough(rates_total, index):
    for n in range(index + 5, rates_total - 3):
        if ((BufferDivRepulse[n] <= BufferDivRepulse[n + 1] and BufferDivRepulse[n] < BufferDivRepulse[n + 2]) and BufferDivRepulse[n] <= BufferDivRepulse[n - 1]) and BufferDivRepulse[n] < BufferDivRepulse[n - 2]:
            return n
    return WRONG_VALUE

def ProcessBullish(rates_total, high, low, time, index):
    if IsTrough(rates_total, index):
        curr = index
        prev = PrevTrough(rates_total, index)
        if prev != WRONG_VALUE:
            if BufferDivRepulse[curr] > BufferDivRepulse[prev] and low[curr] < low[prev]:
                DrawDivergence(high, low, time, prev, curr, True)
            elif BufferDivRepulse[curr] < BufferDivRepulse[prev] and low[curr] > low[prev]:
                DrawDivergence(high, low, time, prev, curr, True)

def IsPeak(rates_total, index):
    if (BufferDivRepulse[index] > 0 and BufferDivRepulse[index] > BufferDivRepulse[index + 1]) and BufferDivRepulse[index] > BufferDivRepulse[index - 1]:
        for n in range(index + 1, rates_total - 2):
            if BufferDivRepulse[n] < 0:
                return True
            elif BufferDivRepulse[index] < BufferDivRepulse[n]:
                return False
    return False

def PrevPeak(rates_total, index):
    for n in range(index + 5, rates_total - 3):
        if ((BufferDivRepulse[n] >= BufferDivRepulse[n + 1] and BufferDivRepulse[n] > BufferDivRepulse[n + 2]) and BufferDivRepulse[n] >= BufferDivRepulse[n - 1]) and BufferDivRepulse[n] > BufferDivRepulse[n - 2]:
            return n
    return WRONG_VALUE

def ProcessBearish(rates_total, high, low, time, index):
    if IsPeak(rates_total, index):
        curr = index
        prev = PrevPeak(rates_total, index)
        if prev != WRONG_VALUE:
            if BufferDivRepulse[curr] < BufferDivRepulse[prev] and high[curr] > high[prev]:
                DrawDivergence(high, low, time, prev, curr, False)
            elif BufferDivRepulse[curr] > BufferDivRepulse[prev] and high[curr] < high[prev]:
                DrawDivergence(high, low, time, prev, curr, False)

def DrawDivergence(high, low, time, first, second, bull_flag):
    obj_name = prefix + _str(time[first]) + '_' + _str(time[second])
    wnd = 0
    if ObjectFind(0, obj_name) < 0:
        wnd = ChartWindowFind()
        if wnd != WRONG_VALUE:
            if bull_flag:
                BufferArrowToUP[second] = BufferDivRepulse[second]
                for j in range(first, second - 1, -1):
                    BufferLineToUP[j] = EquationDirect(first, BufferDivRepulse[first], second, BufferDivRepulse[second], j)
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
                BufferArrowToDN[second] = BufferDivRepulse[second]
                for j in range(first, second - 1, -1):
                    BufferLineToDN[j] = EquationDirect(first, BufferDivRepulse[first], second, BufferDivRepulse[second], j)
                ObjectCreate(0, obj_name + '~', OBJ_TREND, 0, time[first], high[first], time[second], high[second])
                ObjectSetInteger(0, obj_name + '~', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_COLOR, indicator_color4)
                ObjectSetString(0, obj_name + '~', OBJPROP_TOOLTIP, '\n')
                ObjectCreate(0, obj_name + '~A', OBJ_ARROW, 0, time[second], high[second] + BufferATR[second])
                ObjectSetInteger(0, obj_name + '~', OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, obj_name + '~', OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_COLOR, indicator_color4)
                ObjectSetInteger(0, obj_name + '~A', OBJPROP_ARROWCODE, 242)
                ObjectSetString(0, obj_name + '~A', OBJPROP_TOOLTIP, 'Bearish signal: ' + TimeToString(time[second]))
            ObjectSetInteger(0, obj_name + '~', OBJPROP_RAY, False)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RepulseDivergence(_MQL5Indicator):
    name = 'Repulse_Divergence'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 5,  # Repulse period
        'InpPeriod2': 15,  # Signal period
        'InpRepulseLine': _Choice({0: 'Main', 1: 'Signal'}, default=0),  # Repulse line
    }

