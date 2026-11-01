"""laguerre_roc — converted from MQL5: MQL5 Indicators/Laguerre_ROC/laguerre_roc.mq5

Copyright: Copyright © 2005, Emerald King , MTE&I; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Emerald King , MTE&I', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1, 'indicator_maximum': 1.1, 'indicator_minimum': -0.1}, 'types': {1: 11}, 'colors': {1: [36095, 2763429, 8421504, 16711680, 16760576]}, 'widths': {1: 5}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [0.0], 'description': [], 'name': 'laguerre_roc', 'source': 'MQL5 Indicators/Laguerre_ROC/laguerre_roc.mq5', 'folder': 'Laguerre_ROC', 'inputs': [{'mql': 'vPeriod', 'py': 'vPeriod', 'param': 'vPeriod', 'type': 'uint', 'default': 5, 'label': 'Period', 'sinput': False}, {'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.5, 'label': 'Averaging ratio', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'double', 'default': 0.75, 'label': 'Overbought level in %', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'double', 'default': 0.25, 'label': 'Oversold level in %', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Overbought level color', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Oversold level color', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Style of levels', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Width of levels', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
vPeriod = _input('vPeriod', 5)  # Period
gamma = _input('gamma', 0.5)  # Averaging ratio
UpLevel = _input('UpLevel', 0.75)  # Overbought level in %
DnLevel = _input('DnLevel', 0.25)  # Oversold level in %
UpLevelsColor = _input('UpLevelsColor', clrMagenta)  # Overbought level color
DnLevelsColor = _input('DnLevelsColor', clrMagenta)  # Oversold level color
Levelstyle = _input('Levelstyle', DASH_)  # Style of levels
LevelsWidth = _input('LevelsWidth', Width_1)  # Width of levels
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(vPeriod + 1)
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(2, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Laguerre_ROC')
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, DnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 0.5)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, DASHDOTDOT_)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_L0A_, _s_OnCalculate_L0_, _s_OnCalculate_L1A_, _s_OnCalculate_L1_, _s_OnCalculate_L2A_, _s_OnCalculate_L2_, _s_OnCalculate_L3A_, _s_OnCalculate_L3_
    if rates_total < (min_rates_total + begin):
        return 0
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L0A = 0.0
    L1A = 0.0
    L2A = 0.0
    L3A = 0.0
    CU = 0.0
    CD = 0.0
    ROC = 0.0
    LROC = 0.0
    limit = 0
    bar = 0
    vbar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1 - begin
        bar = limit + 1
        vbar = limit + _int(vPeriod) + 1
        ROC = _fdiv(price[bar] - price[vbar], price[vbar]) + Point()
        _s_OnCalculate_L0_ = ROC
        _s_OnCalculate_L1_ = ROC
        _s_OnCalculate_L2_ = ROC
        _s_OnCalculate_L3_ = ROC
        _s_OnCalculate_L0A_ = ROC
        _s_OnCalculate_L1A_ = ROC
        _s_OnCalculate_L2A_ = ROC
        _s_OnCalculate_L3A_ = ROC
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(price, True)
    L0 = _s_OnCalculate_L0_
    L1 = _s_OnCalculate_L1_
    L2 = _s_OnCalculate_L2_
    L3 = _s_OnCalculate_L3_
    L0A = _s_OnCalculate_L0A_
    L1A = _s_OnCalculate_L1A_
    L2A = _s_OnCalculate_L2A_
    L3A = _s_OnCalculate_L3A_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        vbar = bar + _int(vPeriod)
        ROC = _fdiv(price[bar] - price[vbar], price[vbar]) + Point()
        L0 = ((1 - gamma) * ROC) + (gamma * L0A)
        L1 = ((-gamma) * L0) + L0A + (gamma * L1A)
        L2 = ((-gamma) * L1) + L1A + (gamma * L2A)
        L3 = ((-gamma) * L2) + L2A + (gamma * L3A)
        CU = 0.0
        CD = 0.0
        if L0 >= L1:
            CU = L0 - L1
        else:
            CD = L1 - L0
        if L1 >= L2:
            CU += L1 - L2
        else:
            CD += L2 - L1
        if L2 >= L3:
            CU += L2 - L3
        else:
            CD += L3 - L2
        if (CU + CD) != 0:
            LROC = _fdiv(CU, CU + CD)
        if bar == 1:
            _s_OnCalculate_L0_ = L0
            _s_OnCalculate_L1_ = L1
            _s_OnCalculate_L2_ = L2
            _s_OnCalculate_L3_ = L3
            _s_OnCalculate_L0A_ = L0A
            _s_OnCalculate_L1A_ = L1A
            _s_OnCalculate_L2A_ = L2A
            _s_OnCalculate_L3A_ = L3A
        UpIndBuffer[bar] = LROC
        DnIndBuffer[bar] = 0.5
        clr = 2
        if LROC > UpLevel:
            clr = 4
        elif LROC > 0.5:
            clr = 3
        if LROC < DnLevel:
            clr = 0
        elif LROC < 0.5:
            clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_L0_ = 0.0
_s_OnCalculate_L1_ = 0.0
_s_OnCalculate_L2_ = 0.0
_s_OnCalculate_L3_ = 0.0
_s_OnCalculate_L0A_ = 0.0
_s_OnCalculate_L1A_ = 0.0
_s_OnCalculate_L2A_ = 0.0
_s_OnCalculate_L3A_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LaguerreRoc(_MQL5Indicator):
    name = 'laguerre_roc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'vPeriod': 5,  # Period
        'gamma': 0.5,  # Averaging ratio
        'UpLevel': 0.75,  # Overbought level in %
        'DnLevel': 0.25,  # Oversold level in %
        'Levelstyle': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # Style of levels
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Width of levels
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }
    y_range = (-0.1, 1.1)

