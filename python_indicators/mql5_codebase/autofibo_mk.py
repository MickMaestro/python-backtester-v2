"""AutoFibo_MK — converted from MQL5: MQL5 Indicators/AutoFibo indicator of two last swings based on ZigZag/AutoFibo_MK.mq5

AutoFibo based on Zigzag by Nikolay Kositsin
Copyright: Marek Korzeniewski; Link: sunok.fx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Marek Korzeniewski', 'link': 'sunok.fx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [16711935, 14822282]}, 'widths': {1: 1}, 'styles': {1: 1}, 'labels': {1: 'AutoFibo'}, 'levels': [], 'description': ['AutoFibo based on Zigzag by Nikolay Kositsin'], 'name': 'AutoFibo_MK', 'source': 'MQL5 Indicators/AutoFibo indicator of two last swings based on ZigZag/AutoFibo_MK.mq5', 'folder': 'AutoFibo indicator of two last swings based on ZigZag', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'DynamicFiboFlag', 'py': 'DynamicFiboFlag', 'param': 'DynamicFiboFlag', 'type': 'bool', 'default': True, 'label': 'DynamicFibo display flag', 'sinput': False}, {'mql': 'DynamicFibo_color', 'py': 'DynamicFibo_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'DynamicFibo color', 'sinput': False}, {'mql': 'DynamicFibo_style', 'py': 'DynamicFibo_style', 'param': 'DynamicFibo_style', 'type': 'int', 'default': 2, 'label': 'DynamicFibo style', 'sinput': False}, {'mql': 'DynamicFibo_width', 'py': 'DynamicFibo_width', 'param': 'DynamicFibo_width', 'type': 'int', 'default': 1, 'label': 'DynamicFibo line width', 'sinput': False}, {'mql': 'DynamicFibo_AsRay', 'py': 'DynamicFibo_AsRay', 'param': 'DynamicFibo_AsRay', 'type': 'bool', 'default': True, 'label': 'DynamicFibo ray', 'sinput': False}, {'mql': 'StaticFiboFlag', 'py': 'StaticFiboFlag', 'param': 'StaticFiboFlag', 'type': 'bool', 'default': True, 'label': 'StaticFibo display flag', 'sinput': False}, {'mql': 'StaticFibo_color', 'py': 'StaticFibo_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'StaticFibo color', 'sinput': False}, {'mql': 'StaticFibo_style', 'py': 'StaticFibo_style', 'param': 'StaticFibo_style', 'type': 'int', 'default': 2, 'label': 'StaticFibo style', 'sinput': False}, {'mql': 'StaticFibo_width', 'py': 'StaticFibo_width', 'param': 'StaticFibo_width', 'type': 'int', 'default': 1, 'label': 'StaticFibo line width', 'sinput': False}, {'mql': 'StaticFibo_AsRay', 'py': 'StaticFibo_AsRay', 'param': 'StaticFibo_AsRay', 'type': 'bool', 'default': False, 'label': 'StaticFibo ray', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 6)
ExtBackstep = _input('ExtBackstep', 4)
DynamicFiboFlag = _input('DynamicFiboFlag', True)  # DynamicFibo display flag
DynamicFibo_style = _input('DynamicFibo_style', STYLE_DOT)  # DynamicFibo style
DynamicFibo_width = _input('DynamicFibo_width', 1)  # DynamicFibo line width
DynamicFibo_AsRay = _input('DynamicFibo_AsRay', True)  # DynamicFibo ray
StaticFiboFlag = _input('StaticFiboFlag', True)  # StaticFibo display flag
StaticFibo_style = _input('StaticFibo_style', STYLE_DOT)  # StaticFibo style
StaticFibo_width = _input('StaticFibo_width', 1)  # StaticFibo line width
StaticFibo_AsRay = _input('StaticFibo_AsRay', False)  # StaticFibo ray
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
LASTlowpos = 0
LASThighpos = 0
LASTColor = 0
LASTlow0 = 0.0
LASTlow1 = 0.0
LASThigh0 = 0.0
LASThigh1 = 0.0
StartBars = 0

def CreateFibo(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text):
    ObjectCreate(chart_id, name, OBJ_FIBO, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width + 2)
    if ray > 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    if ray < 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, True)
    if ray == 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, False)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    for numb in range(0, 10):
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELCOLOR, numb, Color)
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELSTYLE, numb, style)
        ObjectSetInteger(chart_id, name, OBJPROP_LEVELWIDTH, numb, width)

def SetFibo(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text):
    if ObjectFind(chart_id, name) == -1:
        CreateFibo(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text)
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
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetString(0, PLOT_LABEL, 'ZigZag Lowest')
    PlotIndexSetString(1, PLOT_LABEL, 'ZigZag Highest')
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag (ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnDeinit(reason):
    ObjectDelete(0, 'DynamicFibo')
    ObjectDelete(0, 'StaticFibo')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LASThigh0, LASThigh1, LASThighpos, LASTlow0, LASTlow1, LASTlowpos
    if rates_total < StartBars:
        return 0
    limit = 0
    climit = 0
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
    Max = False
    Min = False
    bar1 = 0
    bar2 = 0
    bar3 = 0
    sign = Box(0)
    price1 = Box(0.0)
    price2 = Box(0.0)
    price3 = Box(0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
        climit = limit
        lastlow1 = -1.0
        lasthigh1 = -1.0
        lastlowpos = -1
        lasthighpos = -1
    else:
        limit = rates_total - prev_calculated
        climit = limit + StartBars
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
    bar = climit
    for bar in range(bar, 0 - 1, -1):
        Max = (HighestBuffer[bar] != 0)
        Min = (LowestBuffer[bar] != 0)
        if (not Max) and (not Min):
            ColorBuffer[bar] = ColorBuffer[bar + 1]
        if Max and Min:
            if ColorBuffer[bar + 1] == 0:
                ColorBuffer[bar] = 1.0
            else:
                ColorBuffer[bar] = 0.0
        if Max and (not Min):
            ColorBuffer[bar] = 1.0
        if (not Max) and Min:
            ColorBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if StaticFiboFlag or DynamicFiboFlag:
        bar1 = FindFirstExtremum(0, rates_total, HighestBuffer, LowestBuffer, sign, price1)
        bar2 = FindSecondExtremum(sign.v, bar1, rates_total, HighestBuffer, LowestBuffer, sign, price2)
        if DynamicFiboFlag:
            SetFibo(0, 'DynamicFibo', 0, time[bar2], price2.v, time[bar1], price1.v, DynamicFibo_color, DynamicFibo_style, DynamicFibo_width, DynamicFibo_AsRay, 'DynamicFibo')
        if StaticFiboFlag:
            bar3 = FindSecondExtremum(sign.v, bar2, rates_total, HighestBuffer, LowestBuffer, sign, price3)
            SetFibo(0, 'StaticFibo', 0, time[bar3], price3.v, time[bar2], price2.v, StaticFibo_color, StaticFibo_style, StaticFibo_width, StaticFibo_AsRay, 'StaticFibo')
        ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
DynamicFibo_color = _input('DynamicFibo_color', _uint(Blue))  # DynamicFibo color
StaticFibo_color = _input('StaticFibo_color', _uint(Red))  # StaticFibo color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AutoFiboMK(_MQL5Indicator):
    name = 'AutoFibo_MK'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 6,
        'ExtBackstep': 4,
        'DynamicFiboFlag': True,  # DynamicFibo display flag
        'DynamicFibo_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # DynamicFibo style
        'DynamicFibo_width': 1,  # DynamicFibo line width
        'DynamicFibo_AsRay': True,  # DynamicFibo ray
        'StaticFiboFlag': True,  # StaticFibo display flag
        'StaticFibo_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # StaticFibo style
        'StaticFibo_width': 1,  # StaticFibo line width
        'StaticFibo_AsRay': False,  # StaticFibo ray
    }

