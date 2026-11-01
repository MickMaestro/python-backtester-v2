"""zigzag_nk_channel — converted from MQL5: MQL5 Indicators/ZigZag NK Channel/zigzag_nk_channel.mq5

ZigZag
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['ZigZag'], 'name': 'zigzag_nk_channel', 'source': 'MQL5 Indicators/ZigZag NK Channel/zigzag_nk_channel.mq5', 'folder': 'ZigZag NK Channel', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'FirstExtrNumb', 'py': 'FirstExtrNumb', 'param': 'FirstExtrNumb', 'type': 'int', 'default': 1, 'label': 'First peak index number (0,1,2,3...)', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Upper channel line color', 'sinput': False}, {'mql': 'Upper_style', 'py': 'Upper_style', 'param': 'Upper_style', 'type': 'int', 'default': 0, 'label': 'Upper channel line style', 'sinput': False}, {'mql': 'Upper_width', 'py': 'Upper_width', 'param': 'Upper_width', 'type': 'int', 'default': 3, 'label': 'Upper channel line width', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Middle line color', 'sinput': False}, {'mql': 'Middle_style', 'py': 'Middle_style', 'param': 'Middle_style', 'type': 'int', 'default': 4, 'label': 'Middle line style', 'sinput': False}, {'mql': 'Middle_width', 'py': 'Middle_width', 'param': 'Middle_width', 'type': 'int', 'default': 1, 'label': 'Middle line width', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Lower channel line color', 'sinput': False}, {'mql': 'Lower_style', 'py': 'Lower_style', 'param': 'Lower_style', 'type': 'int', 'default': 0, 'label': 'Lower channel line style', 'sinput': False}, {'mql': 'Lower_width', 'py': 'Lower_width', 'param': 'Lower_width', 'type': 'int', 'default': 3, 'label': 'Lower channel line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DeepSkyBlue = 0xFFBF00  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name
Teal = 0x808000  # MQL4 colour name

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
FirstExtrNumb = _input('FirstExtrNumb', 1)  # First peak index number (0,1,2,3...)
Upper_style = _input('Upper_style', STYLE_SOLID)  # Upper channel line style
Upper_width = _input('Upper_width', w_3)  # Upper channel line width
Middle_style = _input('Middle_style', STYLE_DASHDOTDOT)  # Middle line style
Middle_width = _input('Middle_width', w_1)  # Middle line width
Lower_style = _input('Lower_style', STYLE_SOLID)  # Lower channel line style
Lower_width = _input('Lower_width', w_3)  # Lower channel line width
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
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
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
    global StartBars
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
    ObjectDelete(0, 'Upper Line')
    ObjectDelete(0, 'Middle Line')
    ObjectDelete(0, 'Lower Line')

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
    dprice = 0.0
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
        ObjectDelete(0, 'Upper Line')
        ObjectDelete(0, 'Middle Line')
        ObjectDelete(0, 'Lower Line')
        return rates_total
    bar2 = FindSecondExtremum(sign.v, bar1, rates_total, HighestBuffer, LowestBuffer, sign, price2)
    bar3 = FindSecondExtremum(sign.v, bar2, rates_total, HighestBuffer, LowestBuffer, sign, price3)
    bar4 = bar2 + bar3 - bar1
    price4 = price2.v + price3.v - price1.v
    if sign.v == 1:
        SetTline(0, 'Upper Line', 0, time[bar3], price3.v, time[bar1], price1.v, Upper_color, Upper_style, Upper_width, 'Upper Line')
        SetTline(0, 'Lower Line', 0, time[bar4], price4, time[bar2], price2.v, Lower_color, Lower_style, Lower_width, 'Lower Line')
    if sign.v == -1:
        SetTline(0, 'Upper Line', 0, time[bar4], price4, time[bar2], price2.v, Upper_color, Upper_style, Upper_width, 'Upper Line')
        SetTline(0, 'Lower Line', 0, time[bar3], price3.v, time[bar1], price1.v, Lower_color, Lower_style, Lower_width, 'Lower Line')
    dprice = _fdiv(-(price3.v - price1.v), bar3 - bar1)
    dprice = (price3.v - price4 - (dprice * (bar4 - bar3))) / 2.0
    price4 += dprice
    price2.v += dprice
    SetTline(0, 'Middle Line', 0, time[bar4], price4, time[bar2], price2.v, Middle_color, Middle_style, Middle_width, 'Middle Line')
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Upper_color = _input('Upper_color', _uint(DeepSkyBlue))  # Upper channel line color
Middle_color = _input('Middle_color', _uint(Teal))  # Middle line color
Lower_color = _input('Lower_color', _uint(Magenta))  # Lower channel line color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigzagNkChannel(_MQL5Indicator):
    name = 'zigzag_nk_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
        'FirstExtrNumb': 1,  # First peak index number (0,1,2,3...)
        'Upper_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Upper channel line style
        'Upper_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Upper channel line width
        'Middle_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Middle line style
        'Middle_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Middle line width
        'Lower_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Lower channel line style
        'Lower_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Lower channel line width
    }

