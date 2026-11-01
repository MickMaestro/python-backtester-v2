"""Fibonacci_Channel — converted from MQL5: MQL5 Indicators/Quartile Trend Channel/Fibonacci_Channel.mq5

Fibonacci_Channel
Copyright: Copyright © 2021, Dark Ryd3r; Link: https://darkryd3r.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2021, Dark Ryd3r', 'link': 'https://darkryd3r.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Fibonacci_Channel'], 'name': 'Fibonacci_Channel', 'source': 'MQL5 Indicators/Quartile Trend Channel/Fibonacci_Channel.mq5', 'folder': 'Quartile Trend Channel', 'inputs': [{'mql': 'Levelclr', 'py': 'Levelclr', 'param': None, 'type': 'color', 'default': 13458026, 'label': '', 'sinput': False}, {'mql': 'LevelStyle', 'py': 'LevelStyle', 'param': 'LevelStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'FirstExtrNumb', 'py': 'FirstExtrNumb', 'param': 'FirstExtrNumb', 'type': 'int', 'default': 1, 'label': 'Numb', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
Fib_Levels = '-0.786,-0.618,-0.5,-0.382,-0.236'
Levelclr = _input('Levelclr', clrSlateBlue)
LevelStyle = _input('LevelStyle', STYLE_SOLID)
levels_values = Arr(0, 0.0)  # Array of level values
levels_descriptions = Arr.of([], fill="")  # Array of level descriptions
ExtDepth = _input('ExtDepth', 55)
ExtDeviation = _input('ExtDeviation', 3)
ExtBackstep = _input('ExtBackstep', 1)
FirstExtrNumb = _input('FirstExtrNumb', 1)  # Numb
Upper_color = clrDeepPink  # Upper channel line color
Upper_style = STYLE_DASH  # Upper channel line style
Upper_width = w_1  # Upper channel line width
Middle_color = 0x373737  # Middle line color
Middle_style = STYLE_DASH  # Middle line style
Middle_width = w_1  # Middle line width
Lower_color = clrDeepPink  # clrAqua
Lower_style = STYLE_DASH  # Lower channel line style
Lower_width = w_1  # Lower channel line width
L618_color = clrMagenta  # 618 line color
L618_style = STYLE_DASH  # 618 line style
L618_width = w_1  # 618 line width
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
LASTlowpos = 0
LASThighpos = 0
LASTColor = 0
LASTlow0 = 0.0
LASTlow1 = 0.0
LASThigh0 = 0.0
LASThigh1 = 0.0
StartBars = 0
prefix = ""

def CreateChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_CHANNEL, nwin, time1, price1, time2, price2, time3, price3)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)

def SetChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateChannel(chart_id, name, nwin, time1, price1, time2, price2, time3, price3, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectMove(chart_id, name, 2, time3, price3)

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectMove(chart_id, name, 0, time1, price1)
    ObjectMove(chart_id, name, 1, time2, price2)

def FindFirstExtremum(StartPos, Rates_total, UpArray, DnArray, Sign, Extremum):
    if StartPos >= Rates_total:
        StartPos = Rates_total - 1
    for bar in range(StartPos, Rates_total):
        if UpArray[bar] != 0.0 and UpArray[bar] != EMPTY_VALUE:
            Sign.v = 1
            Extremum.v = UpArray[bar]
            return bar
            break
        if DnArray[bar] != 0.0 and DnArray[bar] != EMPTY_VALUE:
            Sign.v = -1
            Extremum.v = DnArray[bar]
            return bar
            break
    return -1

def FindSecondExtremum(Direct, StartPos, Rates_total, UpArray, DnArray, Sign, Extremum):
    if StartPos >= Rates_total:
        StartPos = Rates_total - 1
    if Direct == -1:
        for bar in range(StartPos, Rates_total):
            if UpArray[bar] != 0.0 and UpArray[bar] != EMPTY_VALUE:
                Sign.v = 1
                Extremum.v = UpArray[bar]
                return bar
                break
    if Direct == 1:
        for bar in range(StartPos, Rates_total):
            if DnArray[bar] != 0.0 and DnArray[bar] != EMPTY_VALUE:
                Sign.v = -1
                Extremum.v = DnArray[bar]
                return bar
                break
    return -1

def OnInit():
    global StartBars, prefix
    prefix = 'w_'
    StartBars = ExtDepth + ExtBackstep
    SetIndexBuffer(0, LowestBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag Lowest')
    PlotIndexSetString(1, PLOT_LABEL, 'ZigZag Highest')
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag (ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if rates_total < StartBars:
        return 0
    limit = 0
    bar = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    curlow = 0.0
    curhigh = 0.0
    lasthigh0 = 0.0
    lastlow0 = 0.0
    lasthigh1 = 0.0
    lastlow1 = 0.0
    val = 0.0
    res = 0.0
    bar1 = 0
    bar2 = 0
    bar3 = 0
    bar4 = 0
    sign = Box(0)
    price1 = Box(0.0)
    price2 = Box(0.0)
    price3 = Box(0.0)
    price4 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
        lastlow1 = -1.0
        lasthigh1 = -1.0
        lastlowpos = -1
        lasthighpos = -1
    else:
        limit = rates_total - prev_calculated
        lastlow0 = LASTlow0
        lasthigh0 = LASThigh0
        lastlow1 = LASTlow1
        lasthigh1 = LASThigh1
        lastlowpos = LASTlowpos + limit
        lasthighpos = LASThighpos + limit
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            LASTlow0 = lastlow0
            LASThigh0 = lasthigh0
        val = low[ArrayMinimum(low, bar, ExtDepth)]
        if val == lastlow0:
            val = 0.0
        else:
            lastlow0 = val
            if (low[bar] - val) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = LowestBuffer[bar + back]
                    if res != 0 and res > val:
                        LowestBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        LowestBuffer[bar] = val
        val = high[ArrayMaximum(high, bar, ExtDepth)]
        if val == lasthigh0:
            val = 0.0
        else:
            lasthigh0 = val
            if (val - high[bar]) > (ExtDeviation * Point()):
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = HighestBuffer[bar + back]
                    if res != 0 and res < val:
                        HighestBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        HighestBuffer[bar] = val
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            LASTlow1 = lastlow1
            LASThigh1 = lasthigh1
            LASTlowpos = lastlowpos
            LASThighpos = lasthighpos
        curlow = LowestBuffer[bar]
        curhigh = HighestBuffer[bar]
        if curlow == 0 and curhigh == 0:
            continue
        if curhigh != 0:
            if lasthigh1 > 0:
                if lasthigh1 < curhigh:
                    HighestBuffer[lasthighpos] = 0.0
                else:
                    HighestBuffer[bar] = 0.0
            if lasthigh1 < curhigh or lasthigh1 < 0:
                lasthigh1 = curhigh
                lasthighpos = bar
            lastlow1 = -1.0
        if curlow != 0:
            if lastlow1 > 0:
                if lastlow1 > curlow:
                    LowestBuffer[lastlowpos] = 0.0
                else:
                    LowestBuffer[bar] = 0.0
            if curlow < lastlow1 or lastlow1 < 0:
                lastlow1 = curlow
                lastlowpos = bar
            lasthigh1 = -1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar1 = FindFirstExtremum(0, rates_total, HighestBuffer, LowestBuffer, sign, price1)
    numb = 1
    while numb <= FirstExtrNumb and bar1 > -1:
        bar1 = FindSecondExtremum(sign.v, bar1, rates_total, HighestBuffer, LowestBuffer, sign, price1)
        numb += 1
    if bar1 == -1:
        ObjectsDeleteAll(0, prefix)
        return rates_total
    bar2 = FindSecondExtremum(sign.v, bar1, rates_total, HighestBuffer, LowestBuffer, sign, price2)
    bar3 = FindSecondExtremum(sign.v, bar2, rates_total, HighestBuffer, LowestBuffer, sign, price3)
    bar4 = bar2 + bar3 - bar1
    price4 = price2.v + price3.v - price1.v
    if sign.v == 1:
        FiboChannelCreate(0, prefix + 'Upper Fib', 0, time[bar3], price3.v, time[bar1], price1.v, time[bar4], price4, Upper_color, Upper_style)
        SetFiboLevels(prefix + 'Upper Fib', levels_values)
        SetFiboDescriptions(prefix + 'Upper Fib', levels_descriptions)
    if sign.v == -1:
        FiboChannelCreate(0, prefix + 'Lower Fib', 0, time[bar4], price4, time[bar2], price2.v, time[bar3], price3.v, Upper_color, Upper_style)
        SetFiboLevels(prefix + 'Lower Fib', levels_values)
        SetFiboDescriptions(prefix + 'Lower Fib', levels_descriptions)
    ChartRedraw(0)
    return rates_total

def FiboChannelCreate(chart_ID=0, name='FiboChannel', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, time3=0, price3=0.0, clr=clrCrimson, style=STYLE_SOLID, width=1, back=False, selection=True, ray_left=False, ray_right=True, hidden=True, z_order=0):
    time1 = Box(time1)
    price1 = Box(price1)
    time2 = Box(time2)
    price2 = Box(price2)
    time3 = Box(time3)
    price3 = Box(price3)
    ChangeFiboChannelEmptyPoints(time1, price1, time2, price2, time3, price3)
    StringToDoubleArray(Fib_Levels, levels_values)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_FIBOCHANNEL, sub_window, time1.v, price1.v, time2.v, price2.v, time3.v, price3.v):
        Print('FiboChannelCreate', ': failed to create "Fibonacci Channel"! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_LEFT, ray_left)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def FiboChannelPointChange(chart_ID=0, name='FiboChannel', point_index=0, time=0, price=0.0):
    if not time:
        time = TimeCurrent()
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, point_index, time, price):
        Print('FiboChannelPointChange', ': failed to move the anchor point! Error code = ', GetLastError())
        return False
    return True

def ChangeFiboChannelEmptyPoints(time1, price1, time2, price2, time3, price3):
    if not time2.v:
        time2.v = TimeCurrent()
    if not price2.v:
        price2.v = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    if not time1.v:
        temp = Arr(10, 0, dyn=False)
        CopyTime(Symbol(), Period(), _DT(time2.v), 10, temp)
        time1.v = temp[0]
    if not price1.v:
        price1.v = price2.v + (300 * SymbolInfoDouble(Symbol(), SYMBOL_POINT))
    if not time3.v:
        time3.v = time1.v
    if not price3.v:
        price3.v = price2.v

def StringToDoubleArray(_haystack, _result, _delimiter=','):
    haystack_pieces = Arr(0, "")
    pieces_count = 0
    i = 0
    current_number = ''
    pieces_count = StringSplit(_haystack, StringGetCharacter(_delimiter, 0), haystack_pieces)
    if pieces_count > 0:
        ArrayResize(_result, pieces_count)
        i = 0
        for i in range(i, pieces_count):
            StringTrimLeft(_ElemRef(haystack_pieces, i))
            StringTrimRight(_ElemRef(haystack_pieces, i))
            _result[i] = StringToDouble(haystack_pieces[i])
        else:
            i = _range_end(i, pieces_count, 1)
    else:
        ArrayResize(_result, 1)
        _result[0] = 0.0

def SetFiboLevels(_object_name, _levels_values):
    i = 0
    levels_count = ArraySize(_levels_values)
    ObjectSetInteger(0, _object_name, OBJPROP_LEVELS, levels_count)
    i = 0
    for i in range(i, levels_count):
        ObjectSetDouble(0, _object_name, OBJPROP_LEVELVALUE, i, _levels_values[i])
        ObjectSetInteger(0, _object_name, OBJPROP_LEVELCOLOR, i, Levelclr)
        ObjectSetInteger(0, _object_name, OBJPROP_LEVELSTYLE, i, LevelStyle)
    else:
        i = _range_end(i, levels_count, 1)
    ChartRedraw(0)

def SetFiboDescriptions(_object_name, _levels_descriptions):
    i = 0
    levels_count = _int(ObjectGetInteger(0, _object_name, OBJPROP_LEVELS))
    array_size = ArraySize(_levels_descriptions)
    i = 0
    for i in range(i, levels_count):
        Cuttext = DoubleToString(levels_values[i])
        if array_size > 0 and i < array_size:
            ObjectSetString(0, _object_name, OBJPROP_LEVELTEXT, i, _levels_descriptions[i])
        else:
            ObjectSetString(0, _object_name, OBJPROP_LEVELTEXT, i, StringSubstr(Cuttext, 0, StringLen(Cuttext) - 5))
    else:
        i = _range_end(i, levels_count, 1)
    ChartRedraw(0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FibonacciChannel(_MQL5Indicator):
    name = 'Fibonacci_Channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LevelStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'ExtDepth': 55,
        'ExtDeviation': 3,
        'ExtBackstep': 1,
        'FirstExtrNumb': 1,  # Numb
    }

