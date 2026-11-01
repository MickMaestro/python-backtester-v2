"""zigzagonparabolic_fibo_channel — converted from MQL5: MQL5 Indicators/ZigZag on Parabolic + Fibo + Channel/zigzagonparabolic_fibo_channel.mq5

ZigZag on Parabolic
Copyright: Copyright © 2009, EarnForex; Link: http://www.earnforex.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, EarnForex', 'link': 'http://www.earnforex.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 13}, 'colors': {1: [8034025, 16748574]}, 'widths': {1: 1}, 'styles': {1: 1}, 'labels': {1: 'ZigZag'}, 'levels': [], 'description': ['ZigZag on Parabolic'], 'name': 'zigzagonparabolic_fibo_channel', 'source': 'MQL5 Indicators/ZigZag on Parabolic + Fibo + Channel/zigzagonparabolic_fibo_channel.mq5', 'folder': 'ZigZag on Parabolic + Fibo + Channel', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.02, 'label': 'SAR step', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'SAR maximum', 'sinput': False}, {'mql': 'ExtremumsShift', 'py': 'ExtremumsShift', 'param': 'ExtremumsShift', 'type': 'bool', 'default': True, 'label': 'Extremum shift flag', 'sinput': False}, {'mql': 'FirstExtrNumb', 'py': 'FirstExtrNumb', 'param': 'FirstExtrNumb', 'type': 'int', 'default': 1, 'label': 'First extremum number (0,1,2,3...)', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Channel upper line color', 'sinput': False}, {'mql': 'Upper_style', 'py': 'Upper_style', 'param': 'Upper_style', 'type': 'int', 'default': 0, 'label': 'Channel upper line style', 'sinput': False}, {'mql': 'Upper_width', 'py': 'Upper_width', 'param': 'Upper_width', 'type': 'int', 'default': 3, 'label': 'Channel upper line width', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Middle line color', 'sinput': False}, {'mql': 'Middle_style', 'py': 'Middle_style', 'param': 'Middle_style', 'type': 'int', 'default': 4, 'label': 'Middle line style', 'sinput': False}, {'mql': 'Middle_width', 'py': 'Middle_width', 'param': 'Middle_width', 'type': 'int', 'default': 1, 'label': 'Middle line width', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Channel lower line color', 'sinput': False}, {'mql': 'Lower_style', 'py': 'Lower_style', 'param': 'Lower_style', 'type': 'int', 'default': 0, 'label': 'Channel lower line style', 'sinput': False}, {'mql': 'Lower_width', 'py': 'Lower_width', 'param': 'Lower_width', 'type': 'int', 'default': 3, 'label': 'Channel lower line width', 'sinput': False}, {'mql': 'DynamicFiboFlag', 'py': 'DynamicFiboFlag', 'param': 'DynamicFiboFlag', 'type': 'bool', 'default': True, 'label': 'DynamicFibo display flag', 'sinput': False}, {'mql': 'DynamicFibo_color', 'py': 'DynamicFibo_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'DynamicFibo color', 'sinput': False}, {'mql': 'DynamicFibo_style', 'py': 'DynamicFibo_style', 'param': 'DynamicFibo_style', 'type': 'int', 'default': 4, 'label': 'DynamicFibo style', 'sinput': False}, {'mql': 'DynamicFibo_width', 'py': 'DynamicFibo_width', 'param': 'DynamicFibo_width', 'type': 'int', 'default': 1, 'label': 'DynamicFibo line width', 'sinput': False}, {'mql': 'DynamicFibo_AsRay', 'py': 'DynamicFibo_AsRay', 'param': 'DynamicFibo_AsRay', 'type': 'bool', 'default': True, 'label': 'DynamicFibo ray', 'sinput': False}, {'mql': 'StaticFiboFlag', 'py': 'StaticFiboFlag', 'param': 'StaticFiboFlag', 'type': 'bool', 'default': True, 'label': 'StaticFibo display flag', 'sinput': False}, {'mql': 'StaticFibo_color', 'py': 'StaticFibo_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'StaticFibo color', 'sinput': False}, {'mql': 'StaticFibo_style', 'py': 'StaticFibo_style', 'param': 'StaticFibo_style', 'type': 'int', 'default': 1, 'label': 'StaticFibo style', 'sinput': False}, {'mql': 'StaticFibo_width', 'py': 'StaticFibo_width', 'param': 'StaticFibo_width', 'type': 'int', 'default': 1, 'label': 'StaticFibo line width', 'sinput': False}, {'mql': 'StaticFibo_AsRay', 'py': 'StaticFibo_AsRay', 'param': 'StaticFibo_AsRay', 'type': 'bool', 'default': False, 'label': 'StaticFibo ray', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
DarkViolet = 0xD30094  # MQL4 colour name
DeepPink = 0x9314FF  # MQL4 colour name
MediumVioletRed = 0x8515C7  # MQL4 colour name
Teal = 0x808000  # MQL4 colour name

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
Step = _input('Step', 0.02)  # SAR step
Maximum = _input('Maximum', 0.2)  # SAR maximum
ExtremumsShift = _input('ExtremumsShift', True)  # Extremum shift flag
FirstExtrNumb = _input('FirstExtrNumb', 1)  # First extremum number (0,1,2,3...)
Upper_style = _input('Upper_style', STYLE_SOLID)  # Channel upper line style
Upper_width = _input('Upper_width', w_3)  # Channel upper line width
Middle_style = _input('Middle_style', STYLE_DASHDOTDOT)  # Middle line style
Middle_width = _input('Middle_width', w_1)  # Middle line width
Lower_style = _input('Lower_style', STYLE_SOLID)  # Channel lower line style
Lower_width = _input('Lower_width', w_3)  # Channel lower line width
DynamicFiboFlag = _input('DynamicFiboFlag', True)  # DynamicFibo display flag
DynamicFibo_style = _input('DynamicFibo_style', STYLE_DASHDOTDOT)  # DynamicFibo style
DynamicFibo_width = _input('DynamicFibo_width', w_1)  # DynamicFibo line width
DynamicFibo_AsRay = _input('DynamicFibo_AsRay', True)  # DynamicFibo ray
StaticFiboFlag = _input('StaticFiboFlag', True)  # StaticFibo display flag
StaticFibo_style = _input('StaticFibo_style', STYLE_DASH)  # StaticFibo style
StaticFibo_width = _input('StaticFibo_width', w_1)  # StaticFibo line width
StaticFibo_AsRay = _input('StaticFibo_AsRay', False)  # StaticFibo ray
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
EShift = 0
min_rates_total = 0
SAR_Handle = 0

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

def CreateFibo(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, ray, text):
    ObjectCreate(chart_id, name, OBJ_FIBO, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    if ray > 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    if ray < 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, True)
    if ray == 0:
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
        ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, False)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
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
        if DnArray[bar] != 0.0 and DnArray[bar] != EMPTY_VALUE:
            Sign.v = -1
            Extremum.v = DnArray[bar]
            return bar
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
    global EShift, SAR_Handle, min_rates_total
    min_rates_total = 1
    if ExtremumsShift:
        EShift = 1
    else:
        EShift = 0
    SAR_Handle = iSAR(None, 0, Step, Maximum)
    if SAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SAR indicator')
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
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ZigZag on Parabolic(', Step, ', ', Maximum, ', ', ExtremumsShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnDeinit(reason):
    ObjectDelete(0, 'DynamicFibo')
    ObjectDelete(0, 'StaticFibo')
    ObjectDelete(0, 'Upper Line')
    ObjectDelete(0, 'Middle Line')
    ObjectDelete(0, 'Lower Line')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_dir_, _s_OnCalculate_h_, _s_OnCalculate_j_, _s_OnCalculate_l_, _s_OnCalculate_lastcolor_
    if BarsCalculated(SAR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    j = 0
    limit = 0
    climit = 0
    to_copy = 0
    bar = 0
    shift = 0
    NewBar = 0
    lastcolor = 0
    h = 0.0
    l = 0.0
    mid0 = 0.0
    mid1 = 0.0
    SAR = Arr(0, 0.0)
    dir = False
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
        limit = rates_total - 1 - min_rates_total
        _s_OnCalculate_h_ = 0.0
        _s_OnCalculate_l_ = 999999999.0
        _s_OnCalculate_dir_ = False
        _s_OnCalculate_j_ = 0
        _s_OnCalculate_lastcolor_ = 0
    else:
        limit = rates_total - prev_calculated
    climit = limit
    to_copy = limit + 2
    if limit == 0:
        NewBar = 1
    else:
        NewBar = 0
    ArraySetAsSeries(SAR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    if CopyBuffer(SAR_Handle, 0, 0, to_copy, SAR) <= 0:
        return 0
    j = _s_OnCalculate_j_
    dir = _s_OnCalculate_dir_
    h = _s_OnCalculate_h_
    l = _s_OnCalculate_l_
    lastcolor = _s_OnCalculate_lastcolor_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_j_ = j
            _s_OnCalculate_dir_ = dir
            _s_OnCalculate_h_ = h
            _s_OnCalculate_l_ = l
        mid0 = (high[bar] + low[bar]) / 2
        mid1 = (high[bar + 1] + low[bar + 1]) / 2
        HighestBuffer[bar] = 0.0
        LowestBuffer[bar] = 0.0
        if bar > 0:
            j += 1
        if dir:
            if h < high[bar]:
                h = high[bar]
                j = NewBar
            if SAR[bar + 1] <= mid1 and SAR[bar] > mid0:
                shift = bar + (EShift * (j + NewBar))
                if shift > (rates_total - 1):
                    shift = rates_total - 1
                HighestBuffer[shift] = h
                dir = False
                l = low[bar]
                j = 0
                if shift > climit:
                    climit = shift
        else:
            if l > low[bar]:
                l = low[bar]
                j = NewBar
            if SAR[bar + 1] >= mid1 and SAR[bar] < mid0:
                shift = bar + (EShift * (j + NewBar))
                if shift > (rates_total - 1):
                    shift = rates_total - 1
                LowestBuffer[shift] = l
                dir = True
                h = high[bar]
                j = 0
                if shift > climit:
                    climit = shift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = climit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_lastcolor_ = lastcolor
        if HighestBuffer[bar] == 0.0 or LowestBuffer[bar] == 0.0:
            ColorBuffer[bar] = lastcolor
        if HighestBuffer[bar] != 0.0 or LowestBuffer[bar] != 0.0:
            if lastcolor == 0:
                ColorBuffer[bar] = 1.0
                lastcolor = 1
            else:
                ColorBuffer[bar] = 0.0
                lastcolor = 0
        if HighestBuffer[bar] != 0.0 or LowestBuffer[bar] == 0.0:
            ColorBuffer[bar] = 1.0
            lastcolor = 1
        if HighestBuffer[bar] == 0.0 or LowestBuffer[bar] != 0.0:
            ColorBuffer[bar] = 0.0
            lastcolor = 0
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
Upper_color = _input('Upper_color', _uint(DarkViolet))  # Channel upper line color
Middle_color = _input('Middle_color', _uint(Blue))  # Middle line color
Lower_color = _input('Lower_color', _uint(MediumVioletRed))  # Channel lower line color
DynamicFibo_color = _input('DynamicFibo_color', _uint(DeepPink))  # DynamicFibo color
StaticFibo_color = _input('StaticFibo_color', _uint(Teal))  # StaticFibo color

# ---- static local variables
_s_OnCalculate_j_ = 0
_s_OnCalculate_lastcolor_ = 0
_s_OnCalculate_dir_ = False
_s_OnCalculate_h_ = 0.0
_s_OnCalculate_l_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigzagonparabolicFiboChannel(_MQL5Indicator):
    name = 'zigzagonparabolic_fibo_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 0.02,  # SAR step
        'Maximum': 0.2,  # SAR maximum
        'ExtremumsShift': True,  # Extremum shift flag
        'FirstExtrNumb': 1,  # First extremum number (0,1,2,3...)
        'Upper_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Channel upper line style
        'Upper_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Channel upper line width
        'Middle_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Middle line style
        'Middle_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Middle line width
        'Lower_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Channel lower line style
        'Lower_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Channel lower line width
        'DynamicFiboFlag': True,  # DynamicFibo display flag
        'DynamicFibo_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # DynamicFibo style
        'DynamicFibo_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # DynamicFibo line width
        'DynamicFibo_AsRay': True,  # DynamicFibo ray
        'StaticFiboFlag': True,  # StaticFibo display flag
        'StaticFibo_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # StaticFibo style
        'StaticFibo_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # StaticFibo line width
        'StaticFibo_AsRay': False,  # StaticFibo ray
    }

