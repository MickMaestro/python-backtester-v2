"""dserg-ppz — converted from MQL5: MQL5 Indicators/Dserg-PPZ/dserg-ppz.mq5

Indicator for the automatic drawing of PPZ levels by three fractals
Copyright: Copyright © 2010 Dserg; Link: http://www.mql4.com/ru/users/Dserg; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010 Dserg', 'link': 'http://www.mql4.com/ru/users/Dserg', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [11823615], 3: [8421376], 4: [4678655]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {}, 'labels': {1: 'PPZ 0', 2: 'PPZ 1', 3: 'PPZ 2', 4: 'PPZ 3'}, 'levels': [], 'description': ['Indicator for the automatic drawing of PPZ levels by three fractals'], 'name': 'dserg-ppz', 'source': 'MQL5 Indicators/Dserg-PPZ/dserg-ppz.mq5', 'folder': 'Dserg-PPZ', 'inputs': [{'mql': 'Nbars_', 'py': 'Nbars_', 'param': 'Nbars_', 'type': 'int', 'default': 150, 'label': '??Width of the window in which the levels are sought', 'sinput': False}, {'mql': 'Nfirst', 'py': 'Nfirst', 'param': 'Nfirst', 'type': 'int', 'default': 0, 'label': 'offset of right bar fot the window', 'sinput': False}, {'mql': 'minDiff', 'py': 'minDiff', 'param': 'minDiff', 'type': 'double', 'default': 300.0, 'label': 'Minimal distance between the levels in points', 'sinput': False}, {'mql': 'minBars', 'py': 'minBars', 'param': 'minBars', 'type': 'int', 'default': 5, 'label': 'Minimum distance between the fractals in bars', 'sinput': False}, {'mql': 'Color_PPZ0', 'py': 'Color_PPZ0', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'PPZ0 level color', 'sinput': False}, {'mql': 'Color_PPZ1', 'py': 'Color_PPZ1', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'PPZ1 level color', 'sinput': False}, {'mql': 'Color_PPZ2', 'py': 'Color_PPZ2', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'PPZ2 level color', 'sinput': False}, {'mql': 'Color_PPZ3', 'py': 'Color_PPZ3', 'param': None, 'type': 'color', 'default': 14822282, 'label': 'PPZ3 level color', 'sinput': False}, {'mql': 'Color_V1', 'py': 'Color_V1', 'param': None, 'type': 'color', 'default': 255, 'label': 'V1 level color', 'sinput': False}, {'mql': 'Color_V2', 'py': 'Color_V2', 'param': None, 'type': 'color', 'default': 65280, 'label': 'V2 level color', 'sinput': False}, {'mql': 'Style_PPZ0', 'py': 'Style_PPZ0', 'param': 'Style_PPZ0', 'type': 'int', 'default': 0, 'label': 'PPZ0 level line style', 'sinput': False}, {'mql': 'Style_PPZ1', 'py': 'Style_PPZ1', 'param': 'Style_PPZ1', 'type': 'int', 'default': 0, 'label': 'PPZ1 level line style', 'sinput': False}, {'mql': 'Style_PPZ2', 'py': 'Style_PPZ2', 'param': 'Style_PPZ2', 'type': 'int', 'default': 0, 'label': 'PPZ2 level line style', 'sinput': False}, {'mql': 'Style_PPZ3', 'py': 'Style_PPZ3', 'param': 'Style_PPZ3', 'type': 'int', 'default': 0, 'label': 'PPZ3 level line style', 'sinput': False}, {'mql': 'Style_V1', 'py': 'Style_V1', 'param': 'Style_V1', 'type': 'int', 'default': 0, 'label': 'V1 level line style', 'sinput': False}, {'mql': 'Style_V2', 'py': 'Style_V2', 'param': 'Style_V2', 'type': 'int', 'default': 0, 'label': 'V2 level line style', 'sinput': False}, {'mql': 'Width_PPZ0', 'py': 'Width_PPZ0', 'param': 'Width_PPZ0', 'type': 'int', 'default': 1, 'label': 'PPZ0 level line width', 'sinput': False}, {'mql': 'Width_PPZ1', 'py': 'Width_PPZ1', 'param': 'Width_PPZ1', 'type': 'int', 'default': 1, 'label': 'PPZ1 level line width', 'sinput': False}, {'mql': 'Width_PPZ2', 'py': 'Width_PPZ2', 'param': 'Width_PPZ2', 'type': 'int', 'default': 1, 'label': 'PPZ2 level line width', 'sinput': False}, {'mql': 'Width_PPZ3', 'py': 'Width_PPZ3', 'param': 'Width_PPZ3', 'type': 'int', 'default': 1, 'label': 'PPZ3 level line width', 'sinput': False}, {'mql': 'Width_V1', 'py': 'Width_V1', 'param': 'Width_V1', 'type': 'int', 'default': 3, 'label': 'V1 level line width', 'sinput': False}, {'mql': 'Width_V2', 'py': 'Width_V2', 'param': 'Width_V2', 'type': 'int', 'default': 3, 'label': 'V2 level line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Width
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('Width', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
Nbars_ = _input('Nbars_', 150)  # ??Width of the window in which the levels are sought
Nfirst = _input('Nfirst', 0)  # offset of right bar fot the window
minDiff = _input('minDiff', 300.0)  # Minimal distance between the levels in points
minBars = _input('minBars', 5)  # Minimum distance between the fractals in bars
Color_PPZ0 = _input('Color_PPZ0', clrBlue)  # PPZ0 level color
Color_PPZ1 = _input('Color_PPZ1', clrMagenta)  # PPZ1 level color
Color_PPZ2 = _input('Color_PPZ2', clrTeal)  # PPZ2 level color
Color_PPZ3 = _input('Color_PPZ3', clrBlueViolet)  # PPZ3 level color
Color_V1 = _input('Color_V1', clrRed)  # V1 level color
Color_V2 = _input('Color_V2', clrLime)  # V2 level color
Style_PPZ0 = _input('Style_PPZ0', SOLID_)  # PPZ0 level line style
Style_PPZ1 = _input('Style_PPZ1', SOLID_)  # PPZ1 level line style
Style_PPZ2 = _input('Style_PPZ2', SOLID_)  # PPZ2 level line style
Style_PPZ3 = _input('Style_PPZ3', SOLID_)  # PPZ3 level line style
Style_V1 = _input('Style_V1', SOLID_)  # V1 level line style
Style_V2 = _input('Style_V2', SOLID_)  # V2 level line style
Width_PPZ0 = _input('Width_PPZ0', Width_1)  # PPZ0 level line width
Width_PPZ1 = _input('Width_PPZ1', Width_1)  # PPZ1 level line width
Width_PPZ2 = _input('Width_PPZ2', Width_1)  # PPZ2 level line width
Width_PPZ3 = _input('Width_PPZ3', Width_1)  # PPZ3 level line width
Width_V1 = _input('Width_V1', Width_3)  # V1 level line width
Width_V2 = _input('Width_V2', Width_3)  # V2 level line width
B0Buffer = Arr(0, 0.0)
B1Buffer = Arr(0, 0.0)
B2Buffer = Arr(0, 0.0)
B3Buffer = Arr(0, 0.0)
Fr0 = Arr(1000, 0.0, dyn=False)
Ind0 = Arr(1000, 0, dyn=False)
FRA_Handle = 0
min_rates_total = 0
Nbars = 0
loopbegin = 0

def CreateHline(chart_id, name, nwin, price, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)

def CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    ObjectCreate(chart_id, name, OBJ_VLINE, nwin, time1, 999999999)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetString(chart_id, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetVline(chart_id, name, nwin, time1, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateVline(chart_id, name, nwin, time1, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, 999999999)

def OnInit():
    global FRA_Handle, Nbars, loopbegin, min_rates_total
    FRA_Handle = iFractals(None, 0)
    if FRA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iFractals indicator')
    Nbars = Nbars_
    if Nbars > 500:
        Comment('Too many bars for the calculation! The parameter value will be limited to 500')
        Nbars = 500
    loopbegin = Nbars + Nfirst
    min_rates_total = loopbegin
    SetIndexBuffer(0, B0Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    ArraySetAsSeries(B0Buffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, B1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(B1Buffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, B2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 119)
    ArraySetAsSeries(B2Buffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, B3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 119)
    ArraySetAsSeries(B3Buffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Fine Fractals'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnDeinit(reason):
    ObjectDelete(0, 'PPZ')
    ObjectDelete(0, 'PPZ1')
    ObjectDelete(0, 'PPZ2')
    ObjectDelete(0, 'PPZ3')
    ObjectDelete(0, 'V1')
    ObjectDelete(0, 'V2')
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(FRA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    if rates_total == prev_calculated:
        return rates_total
    i = 0
    j = 0
    k = 0
    l = 0
    imin = 0
    jmin = 0
    kmin = 0
    lmin = 0
    imin1 = 0
    jmin1 = 0
    kmin1 = 0
    lmin1 = 0
    imin2 = 0
    jmin2 = 0
    kmin2 = 0
    lmin2 = 0
    imin3 = 0
    jmin3 = 0
    kmin3 = 0
    lmin3 = 0
    f0 = 0.0
    f1 = 0.0
    f2 = 0.0
    f3 = 0.0
    p0 = 0.0
    s0 = 0.0
    pmin = 0.0
    smin = 0.0
    pmin1 = 0.0
    smin1 = 0.0
    pmin2 = 0.0
    smin2 = 0.0
    pmin3 = 0.0
    smin3 = 0.0
    UpFractal = Arr(0, 0.0)
    DnFractal = Arr(0, 0.0)
    A = 0.0
    B = 0.0
    C = 0.0
    Nmax = 0
    to_copy = loopbegin + 1
    if CopyBuffer(FRA_Handle, 0, 0, to_copy, UpFractal) <= 0:
        return 0
    if CopyBuffer(FRA_Handle, 1, 0, to_copy, DnFractal) <= 0:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(UpFractal, True)
    ArraySetAsSeries(DnFractal, True)
    pmin = 10.0
    smin = 10000.0
    pmin1 = 20.0
    smin1 = 20000.0
    pmin2 = 30.0
    smin2 = 30000.0
    pmin3 = 40.0
    smin3 = 40000.0
    i = 0
    for i in range(i, rates_total):
        B0Buffer[i] = 0.0
        B1Buffer[i] = 0.0
        B2Buffer[i] = 0.0
        B3Buffer[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    j = 0
    i = loopbegin
    for i in range(i, Nfirst, -1):
        f0 = UpFractal[i]
        if not f0:
            f0 = DnFractal[i]
        if f0:
            Fr0[j] = f0
            Ind0[j] = i
            j += 1
    else:
        i = _range_end(i, Nfirst, -1)
    Nmax = j
    i = 0
    for i in range(i, Nmax):
        f0 = Fr0[i]
        j = 0
        for j in range(j, Nmax):
            f1 = Fr0[j]
            A = MathAbs(Ind0[i] - Ind0[j])
            if i != j and A > minBars:
                k = 0
                for k in range(k, Nmax):
                    f2 = Fr0[k]
                    A = MathAbs(Ind0[i] - Ind0[k])
                    B = MathAbs(Ind0[k] - Ind0[j])
                    if ((k != j and k != j) and A > minBars) and B > minBars:
                        l = 0
                        for l in range(l, Nmax):
                            f3 = Fr0[l]
                            A = MathAbs(Ind0[i] - Ind0[l])
                            B = MathAbs(Ind0[j] - Ind0[l])
                            C = MathAbs(Ind0[k] - Ind0[l])
                            if ((((l != i and l != j) and l != k) and A > minBars) and B > minBars) and C > minBars:
                                p0 = (f0 + f1 + f2 + f3) / 4.0
                                s0 = ((f0 - p0) * (f0 - p0)) + ((f1 - p0) * (f1 - p0)) + ((f2 - p0) * (f2 - p0)) + ((f2 - p0) * (f2 - p0))
                                if s0 < smin:
                                    smin = s0
                                    pmin = p0
                                    imin = i
                                    jmin = j
                                    kmin = k
                                    lmin = l
                        else:
                            l = _range_end(l, Nmax, 1)
                else:
                    k = _range_end(k, Nmax, 1)
        else:
            j = _range_end(j, Nmax, 1)
    else:
        i = _range_end(i, Nmax, 1)
    i = 0
    for i in range(i, Nmax):
        f0 = Fr0[i]
        if ((i != imin and i != jmin) and i != kmin) and i != lmin:
            j = 0
            for j in range(j, Nmax):
                f1 = Fr0[j]
                A = MathAbs(Ind0[i] - Ind0[j])
                if ((((i != j and A > minBars) and j != imin) and j != jmin) and j != kmin) and j != lmin:
                    k = 0
                    for k in range(k, Nmax):
                        f2 = Fr0[k]
                        A = MathAbs(Ind0[i] - Ind0[k])
                        B = MathAbs(Ind0[k] - Ind0[j])
                        if ((((((k != j and k != j) and A > minBars) and B > minBars) and k != imin) and k != jmin) and k != kmin) and k != lmin:
                            l = 0
                            for l in range(l, Nmax):
                                f3 = Fr0[l]
                                A = MathAbs(Ind0[i] - Ind0[l])
                                B = MathAbs(Ind0[j] - Ind0[l])
                                C = MathAbs(Ind0[k] - Ind0[l])
                                if ((((((((l != i and l != j) and l != k) and A > minBars) and B > minBars) and C > minBars) and l != imin) and l != jmin) and l != kmin) and l != lmin:
                                    p0 = (f0 + f1 + f2 + f3) / 4.0
                                    s0 = ((f0 - p0) * (f0 - p0)) + ((f1 - p0) * (f1 - p0)) + ((f2 - p0) * (f2 - p0)) + ((f2 - p0) * (f2 - p0))
                                    if s0 < smin1 and MathAbs(p0 - pmin) > (minDiff * Point()):
                                        smin1 = s0
                                        pmin1 = p0
                                        imin1 = i
                                        jmin1 = j
                                        kmin1 = k
                                        lmin1 = l
                            else:
                                l = _range_end(l, Nmax, 1)
                    else:
                        k = _range_end(k, Nmax, 1)
            else:
                j = _range_end(j, Nmax, 1)
    else:
        i = _range_end(i, Nmax, 1)
    i = 0
    for i in range(i, Nmax):
        f0 = Fr0[i]
        if ((((((i != imin and i != jmin) and i != kmin) and i != lmin) and i != imin1) and i != jmin1) and i != kmin1) and i != lmin1:
            j = 0
            for j in range(j, Nmax):
                f1 = Fr0[j]
                A = MathAbs(Ind0[i] - Ind0[j])
                if ((((((((i != j and A > minBars) and j != imin) and j != jmin) and j != kmin) and j != lmin) and j != imin1) and j != jmin1) and j != kmin1) and j != lmin1:
                    k = 0
                    for k in range(k, Nmax):
                        f2 = Fr0[k]
                        A = MathAbs(Ind0[i] - Ind0[k])
                        B = MathAbs(Ind0[k] - Ind0[j])
                        if ((((((((((k != j and k != j) and A > minBars) and B > minBars) and k != imin) and k != jmin) and k != kmin) and k != lmin) and k != imin1) and k != jmin1) and k != kmin1) and k != lmin1:
                            l = 0
                            for l in range(l, Nmax):
                                f3 = Fr0[l]
                                A = MathAbs(Ind0[i] - Ind0[l])
                                B = MathAbs(Ind0[j] - Ind0[l])
                                C = MathAbs(Ind0[k] - Ind0[l])
                                if ((((((((((((l != i and l != j) and l != k) and A > minBars) and B > minBars) and C > minBars) and l != imin) and l != jmin) and l != kmin) and l != lmin) and l != imin1) and l != jmin1) and l != kmin1) and l != lmin1:
                                    p0 = (f0 + f1 + f2 + f3) / 4.0
                                    s0 = ((f0 - p0) * (f0 - p0)) + ((f1 - p0) * (f1 - p0)) + ((f2 - p0) * (f2 - p0)) + ((f2 - p0) * (f2 - p0))
                                    if (s0 < smin2 and MathAbs(p0 - pmin) > (minDiff * Point())) and MathAbs(p0 - pmin1) > (minDiff * Point()):
                                        smin2 = s0
                                        pmin2 = p0
                                        imin2 = i
                                        jmin2 = j
                                        kmin2 = k
                                        lmin2 = l
                            else:
                                l = _range_end(l, Nmax, 1)
                    else:
                        k = _range_end(k, Nmax, 1)
            else:
                j = _range_end(j, Nmax, 1)
    else:
        i = _range_end(i, Nmax, 1)
    i = 0
    for i in range(i, Nmax):
        f0 = Fr0[i]
        if ((((((((((i != imin and i != jmin) and i != kmin) and i != lmin) and i != imin1) and i != jmin1) and i != kmin1) and i != lmin1) and i != imin2) and i != jmin2) and i != kmin2) and i != lmin2:
            j = 0
            for j in range(j, Nmax):
                f1 = Fr0[j]
                A = MathAbs(Ind0[i] - Ind0[j])
                if ((((((((((((i != j and A > minBars) and j != imin) and j != jmin) and j != kmin) and j != lmin) and j != imin1) and j != jmin1) and j != kmin1) and j != lmin1) and j != imin2) and j != jmin2) and j != kmin2) and j != lmin2:
                    k = 0
                    for k in range(k, Nmax):
                        f2 = Fr0[k]
                        A = MathAbs(Ind0[i] - Ind0[k])
                        B = MathAbs(Ind0[k] - Ind0[j])
                        if ((((((((((((((k != j and k != j) and A > minBars) and B > minBars) and k != imin) and k != jmin) and k != kmin) and k != lmin) and k != imin1) and k != jmin1) and k != kmin1) and k != lmin1) and k != imin2) and k != jmin2) and k != kmin2) and k != lmin2:
                            l = 0
                            for l in range(l, Nmax):
                                f3 = Fr0[l]
                                A = MathAbs(Ind0[i] - Ind0[l])
                                B = MathAbs(Ind0[j] - Ind0[l])
                                C = MathAbs(Ind0[k] - Ind0[l])
                                if ((((((((((((((((l != i and l != j) and l != k) and A > minBars) and B > minBars) and C > minBars) and l != imin) and l != jmin) and l != kmin) and l != lmin) and l != imin1) and l != jmin1) and l != kmin1) and l != lmin1) and l != imin2) and l != jmin2) and l != kmin2) and l != lmin2:
                                    p0 = (f0 + f1 + f2 + f3) / 4.0
                                    s0 = ((f0 - p0) * (f0 - p0)) + ((f1 - p0) * (f1 - p0)) + ((f2 - p0) * (f2 - p0)) + ((f2 - p0) * (f2 - p0))
                                    if ((s0 < smin3 and MathAbs(p0 - pmin) > (minDiff * Point())) and MathAbs(p0 - pmin1) > (minDiff * Point())) and MathAbs(p0 - pmin2) > (minDiff * Point()):
                                        smin3 = s0
                                        pmin3 = p0
                                        imin3 = i
                                        jmin3 = j
                                        kmin3 = k
                                        lmin3 = l
                            else:
                                l = _range_end(l, Nmax, 1)
                    else:
                        k = _range_end(k, Nmax, 1)
            else:
                j = _range_end(j, Nmax, 1)
    else:
        i = _range_end(i, Nmax, 1)
    Max = 1000 - 1
    imin = MathMin(imin, Max)
    jmin = MathMin(jmin, Max)
    kmin = MathMin(kmin, Max)
    lmin = MathMin(lmin, Max)
    imin1 = MathMin(imin1, Max)
    jmin1 = MathMin(jmin1, Max)
    kmin1 = MathMin(kmin1, Max)
    lmin1 = MathMin(lmin1, Max)
    imin2 = MathMin(imin2, Max)
    jmin2 = MathMin(jmin2, Max)
    kmin2 = MathMin(kmin2, Max)
    lmin2 = MathMin(lmin2, Max)
    imin3 = MathMin(imin3, Max)
    jmin3 = MathMin(jmin3, Max)
    kmin3 = MathMin(kmin3, Max)
    lmin3 = MathMin(lmin3, Max)
    B0Buffer[Ind0[imin]] = open[Ind0[imin]]
    B0Buffer[Ind0[jmin]] = open[Ind0[jmin]]
    B0Buffer[Ind0[kmin]] = open[Ind0[kmin]]
    B0Buffer[Ind0[lmin]] = open[Ind0[lmin]]
    B1Buffer[Ind0[imin1]] = open[Ind0[imin1]]
    B1Buffer[Ind0[jmin1]] = open[Ind0[jmin1]]
    B1Buffer[Ind0[kmin1]] = open[Ind0[kmin1]]
    B1Buffer[Ind0[lmin1]] = open[Ind0[lmin1]]
    B2Buffer[Ind0[imin2]] = open[Ind0[imin2]]
    B2Buffer[Ind0[jmin2]] = open[Ind0[jmin2]]
    B2Buffer[Ind0[kmin2]] = open[Ind0[kmin2]]
    B2Buffer[Ind0[lmin2]] = open[Ind0[lmin2]]
    B3Buffer[Ind0[imin3]] = open[Ind0[imin3]]
    B3Buffer[Ind0[jmin3]] = open[Ind0[jmin3]]
    B3Buffer[Ind0[kmin3]] = open[Ind0[kmin3]]
    B3Buffer[Ind0[lmin3]] = open[Ind0[lmin3]]
    velue = NormalizeDouble(pmin, Digits())
    svelue = _str(velue)
    SetHline(0, 'PPZ', 0, velue, Color_PPZ0, Style_PPZ0, Width_PPZ0, 'PPZ' + svelue)
    velue = NormalizeDouble(pmin1, Digits())
    svelue = _str(velue)
    SetHline(0, 'PPZ1', 0, velue, Color_PPZ1, Style_PPZ1, Width_PPZ1, 'PPZ1' + svelue)
    velue = NormalizeDouble(pmin2, Digits())
    svelue = _str(velue)
    SetHline(0, 'PPZ2', 0, velue, Color_PPZ2, Style_PPZ2, Width_PPZ2, 'PPZ2' + svelue)
    velue = NormalizeDouble(pmin3, Digits())
    svelue = _str(velue)
    SetHline(0, 'PPZ3', 0, velue, Color_PPZ3, Style_PPZ3, Width_PPZ3, 'PPZ3' + svelue)
    SetVline(0, 'V1', 0, time[Nbars + Nfirst], Color_V1, Style_V1, Width_V1, True, 'V1')
    SetVline(0, 'V2', 0, time[Nfirst], Color_V2, Style_V2, Width_V2, True, 'V2')
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DsergPpz(_MQL5Indicator):
    name = 'dserg-ppz'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Nbars_': 150,  # ??Width of the window in which the levels are sought
        'Nfirst': 0,  # offset of right bar fot the window
        'minDiff': 300.0,  # Minimal distance between the levels in points
        'minBars': 5,  # Minimum distance between the fractals in bars
        'Style_PPZ0': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # PPZ0 level line style
        'Style_PPZ1': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # PPZ1 level line style
        'Style_PPZ2': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # PPZ2 level line style
        'Style_PPZ3': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # PPZ3 level line style
        'Style_V1': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # V1 level line style
        'Style_V2': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # V2 level line style
        'Width_PPZ0': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # PPZ0 level line width
        'Width_PPZ1': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # PPZ1 level line width
        'Width_PPZ2': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # PPZ2 level line width
        'Width_PPZ3': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # PPZ3 level line width
        'Width_V1': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # V1 level line width
        'Width_V2': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # V2 level line width
    }

