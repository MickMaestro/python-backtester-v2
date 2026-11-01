"""vhpchannel_02 — converted from MQL5: MQL5 Indicators/Hodrick-Prescott Channel/vhpchannel_02.mq5

VHPChannel

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [55295], 2: [10061943], 3: [36095], 4: [36095]}, 'widths': {}, 'styles': {2: 3}, 'labels': {1: 'VHPChannel'}, 'levels': [], 'description': ['VHPChannel'], 'name': 'vhpchannel_02', 'source': 'MQL5 Indicators/Hodrick-Prescott Channel/vhpchannel_02.mq5', 'folder': 'Hodrick-Prescott Channel', 'inputs': [{'mql': 'InpHPPeriodFast', 'py': 'InpHPPeriodFast', 'param': 'InpHPPeriodFast', 'type': 'int', 'default': 21, 'label': 'HP Fast Period (4...32)', 'sinput': False}, {'mql': 'InpHPPeriodSlow', 'py': 'InpHPPeriodSlow', 'param': 'InpHPPeriodSlow', 'type': 'int', 'default': 144, 'label': 'HP Slow Period (48...256)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

LimeGreen = 0x32CD32  # MQL4 colour name

# ---- inputs and global variables
InpHPPeriodFast = _input('InpHPPeriodFast', 21)  # HP Fast Period (4...32)
InpHPPeriodSlow = _input('InpHPPeriodSlow', 144)  # HP Slow Period (48...256)
HP = Arr(0, 0.0)
HPSlow = Arr(0, 0.0)
Dev1 = Arr(0, 0.0)
Dev2 = Arr(0, 0.0)
HPPeriodFast = 0
HPPeriodSlow = 0
Lambda = 0.0
Lambda2 = 0.0
ShortName = ""

def OnInit():
    global HPPeriodFast, HPPeriodSlow, Lambda, Lambda2, ShortName
    if InpHPPeriodFast < 4 or InpHPPeriodFast > 32:
        printf('Input parameter InpHPPeriodFast has incorrect value (%d). Indicator will use value 21 for calculations.', InpHPPeriodFast)
        HPPeriodFast = 21
    else:
        HPPeriodFast = InpHPPeriodFast
    if InpHPPeriodSlow < 48 or InpHPPeriodSlow > 256:
        printf('Input parameter InpHPPeriodSlow has incorrect value (%d). Indicator will use value 144 for calculations.', InpHPPeriodSlow)
        HPPeriodSlow = 144
    else:
        HPPeriodSlow = InpHPPeriodSlow
    SetIndexBuffer(0, HP, INDICATOR_DATA)
    ArraySetAsSeries(HP, True)
    SetIndexBuffer(1, HPSlow, INDICATOR_DATA)
    ArraySetAsSeries(HPSlow, True)
    SetIndexBuffer(2, Dev1, INDICATOR_DATA)
    ArraySetAsSeries(Dev1, True)
    SetIndexBuffer(3, Dev2, INDICATOR_DATA)
    ArraySetAsSeries(Dev2, True)
    ShortName = 'VHPChannel(' + IntegerToString(HPPeriodFast) + ',' + IntegerToString(HPPeriodSlow) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    PlotIndexSetString(0, PLOT_LABEL, 'HP')
    PlotIndexSetString(1, PLOT_LABEL, 'HPSlow')
    PlotIndexSetString(2, PLOT_LABEL, 'Dev1')
    PlotIndexSetString(3, PLOT_LABEL, 'Dev2')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    Lambda = _fdiv(0.0625, MathPow(MathSin(_fdiv(M_PI, HPPeriodFast)), 4))
    Lambda2 = _fdiv(0.0625, MathPow(MathSin(_fdiv(M_PI, HPPeriodSlow)), 4))
    ObjectCreate(0, ShortName, OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, ShortName, OBJPROP_ANCHOR, ANCHOR_RIGHT_LOWER)
    ObjectSetInteger(0, ShortName, OBJPROP_CORNER, CORNER_RIGHT_LOWER)
    ObjectSetInteger(0, ShortName, OBJPROP_XDISTANCE, 32)
    ObjectSetInteger(0, ShortName, OBJPROP_YDISTANCE, 28)
    ObjectSetInteger(0, ShortName, OBJPROP_FONTSIZE, 11)
    ObjectSetInteger(0, ShortName, OBJPROP_COLOR, LimeGreen)
    ObjectSetInteger(0, ShortName, OBJPROP_SELECTABLE, True)
    ObjectSetString(0, ShortName, OBJPROP_FONT, 'Tahoma')
    return 0

def OnDeinit(reason):
    ObjectDelete(0, ShortName)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    InpDat = Arr(0, 0.0)
    disp = 0.0
    dev = 0.0
    val = 0.0
    if rates_total < (HPPeriodSlow + 1):
        return 0
    if rates_total != prev_calculated:
        i = Bars(Symbol(), 0) - HPPeriodSlow
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, i)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, i)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, i)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, i)
    ArraySetAsSeries(Close, True)
    ArrayResize(InpDat, HPPeriodSlow)
    ArraySetAsSeries(InpDat, True)
    i = 0
    for i in range(i, HPPeriodSlow):
        InpDat[i] = Close[i]
    else:
        i = _range_end(i, HPPeriodSlow, 1)
    HPF(HPPeriodSlow, Lambda, InpDat, HP)
    HPF(HPPeriodSlow, Lambda2, HP, HPSlow)
    disp = 0.0
    i = 0
    for i in range(i, HPPeriodSlow):
        disp += (HP[i] - HPSlow[i]) * (HP[i] - HPSlow[i])
    else:
        i = _range_end(i, HPPeriodSlow, 1)
    disp = _fdiv(disp, HPPeriodSlow - 1)
    dev = MathSqrt(disp) * 2.0
    i = 0
    for i in range(i, HPPeriodSlow):
        Dev1[i] = HPSlow[i] + dev
        Dev2[i] = HPSlow[i] - dev
    else:
        i = _range_end(i, HPPeriodSlow, 1)
    val = _fdiv(dev, HPSlow[0]) * 200
    ObjectSetString(0, ShortName, OBJPROP_TEXT, 'Channel=' + DoubleToString(val, 2) + '%')
    return rates_total

def HPF(nobs, lambda_, x, y):
    a = Arr(0, 0.0)
    b = Arr(0, 0.0)
    c = Arr(0, 0.0)
    H1 = 0.0
    H2 = 0.0
    H3 = 0.0
    H4 = 0.0
    H5 = 0.0
    HH1 = 0.0
    HH2 = 0.0
    HH3 = 0.0
    HH5 = 0.0
    HB = 0.0
    HC = 0.0
    Z = 0.0
    i = 0
    ArrayResize(a, nobs)
    ArrayResize(b, nobs)
    ArrayResize(c, nobs)
    ZeroMemory(a)
    ZeroMemory(b)
    ZeroMemory(c)
    a[0] = 1.0 + lambda_
    b[0] = -2.0 * lambda_
    c[0] = lambda_
    i = 1
    for i in range(i, nobs - 2):
        a[i] = (6.0 * lambda_) + 1.0
        b[i] = -4.0 * lambda_
        c[i] = lambda_
    else:
        i = _range_end(i, nobs - 2, 1)
    a[1] = (5.0 * lambda_) + 1
    a[nobs - 1] = 1.0 + lambda_
    a[nobs - 2] = (5.0 * lambda_) + 1.0
    b[nobs - 2] = -2.0 * lambda_
    b[nobs - 1] = 0.0
    c[nobs - 2] = 0.0
    c[nobs - 1] = 0.0
    i = 0
    for i in range(i, nobs):
        Z = a[i] - (H4 * H1) - (HH5 * HH2)
        HB = b[i]
        HH1 = H1
        H1 = _fdiv(HB - (H4 * H2), Z)
        b[i] = H1
        HC = c[i]
        HH2 = H2
        H2 = _fdiv(HC, Z)
        c[i] = H2
        a[i] = _fdiv(x[i] - (HH3 * HH5) - (H3 * H4), Z)
        HH3 = H3
        H3 = a[i]
        H4 = HB - (H5 * HH1)
        HH5 = H5
        H5 = HC
    else:
        i = _range_end(i, nobs, 1)
    H2 = 0.0
    H1 = a[nobs - 1]
    y[nobs - 1] = H1
    i = nobs - 2
    for i in range(i, 0 - 1, -1):
        y[i] = a[i] - (b[i] * H1) - (c[i] * H2)
        H2 = H1
        H1 = y[i]
    else:
        i = _range_end(i, 0 - 1, -1)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vhpchannel02(_MQL5Indicator):
    name = 'vhpchannel_02'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpHPPeriodFast': 21,  # HP Fast Period (4...32)
        'InpHPPeriodSlow': 144,  # HP Slow Period (48...256)
    }

