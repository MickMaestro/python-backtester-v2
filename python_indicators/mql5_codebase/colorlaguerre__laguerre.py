"""colorlaguerre — converted from MQL5: MQL5 Indicators/Laguerre/colorlaguerre.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [4294967295, 65280, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'colorlaguerre', 'source': 'MQL5 Indicators/Laguerre/colorlaguerre.mq5', 'folder': 'Laguerre', 'inputs': [{'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.7, 'label': '', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 85, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# ---- inputs and global variables
gamma = _input('gamma', 0.7)
HighLevel = _input('HighLevel', 85)
MiddleLevel = _input('MiddleLevel', 50)
LowLevel = _input('LowLevel', 15)
ColorBuffer = Arr(0, 0.0)
ExtLineBuffer = Arr(0, 0.0)

def PointIndicator(Min_rates_total, IndBuffer, ColorIndBuffer, HighLevel_, MiddleLevel_, LowLevel_, bar):
    if bar < (Min_rates_total + 1):
        return
    EMPTY = 0
    HighLev = 1
    HighLevMiddle = 2
    LowLevMiddle = 3
    LowLev = 4
    Level0 = EMPTY
    Level1 = EMPTY
    IndVelue = 0.0
    IndVelue = IndBuffer[bar]
    if IndVelue > HighLevel_:
        Level0 = HighLev
    elif IndVelue > MiddleLevel_:
        Level0 = HighLevMiddle
    if IndVelue < LowLevel_:
        Level0 = LowLev
    elif IndVelue <= MiddleLevel_:
        Level0 = LowLevMiddle
    IndVelue = IndBuffer[bar - 1]
    if IndVelue > HighLevel_:
        Level1 = HighLev
    elif IndVelue > MiddleLevel_:
        Level1 = HighLevMiddle
    if IndVelue < LowLevel_:
        Level1 = LowLev
    elif IndVelue <= MiddleLevel_:
        Level1 = LowLevMiddle
    _sw1 = Level0
    if _sw1 == HighLev:
        ColorIndBuffer[bar] = 1.0
    elif _sw1 == HighLevMiddle:
        _sw2 = Level1
        if _sw2 == HighLev:
            ColorIndBuffer[bar] = 2.0
        elif _sw2 == HighLevMiddle:
            ColorIndBuffer[bar] = ColorIndBuffer[bar - 1]
        elif _sw2 == LowLevMiddle:
            ColorIndBuffer[bar] = 1.0
        elif _sw2 == LowLev:
            ColorIndBuffer[bar] = 1.0
    elif _sw1 == LowLevMiddle:
        _sw3 = Level1
        if _sw3 == HighLev:
            ColorIndBuffer[bar] = 2.0
        elif _sw3 == HighLevMiddle:
            ColorIndBuffer[bar] = 2.0
        elif _sw3 == LowLevMiddle:
            ColorIndBuffer[bar] = ColorIndBuffer[bar - 1]
        elif _sw3 == LowLev:
            ColorIndBuffer[bar] = 1.0
    elif _sw1 == LowLev:
        ColorIndBuffer[bar] = 2.0

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'Laguerre(', gamma, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Gray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_L0A_, _s_OnCalculate_L0_, _s_OnCalculate_L1A_, _s_OnCalculate_L1_, _s_OnCalculate_L2A_, _s_OnCalculate_L2_, _s_OnCalculate_L3A_, _s_OnCalculate_L3_
    if rates_total < begin:
        return 0
    first = 0
    bar = 0
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L0A = 0.0
    L1A = 0.0
    L2A = 0.0
    L3A = 0.0
    LRSI = 0.0
    CU = 0.0
    CD = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = begin + 1
        _s_OnCalculate_L0_ = price[first]
        _s_OnCalculate_L1_ = price[first]
        _s_OnCalculate_L2_ = price[first]
        _s_OnCalculate_L3_ = price[first]
        _s_OnCalculate_L0A_ = price[first]
        _s_OnCalculate_L1A_ = price[first]
        _s_OnCalculate_L2A_ = price[first]
        _s_OnCalculate_L3A_ = price[first]
    else:
        first = prev_calculated - 1
    L0 = _s_OnCalculate_L0_
    L1 = _s_OnCalculate_L1_
    L2 = _s_OnCalculate_L2_
    L3 = _s_OnCalculate_L3_
    L0A = _s_OnCalculate_L0A_
    L1A = _s_OnCalculate_L1A_
    L2A = _s_OnCalculate_L2A_
    L3A = _s_OnCalculate_L3A_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_L0_ = L0
            _s_OnCalculate_L1_ = L1
            _s_OnCalculate_L2_ = L2
            _s_OnCalculate_L3_ = L3
            _s_OnCalculate_L0A_ = L0A
            _s_OnCalculate_L1A_ = L1A
            _s_OnCalculate_L2A_ = L2A
            _s_OnCalculate_L3A_ = L3A
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        L0 = ((1 - gamma) * price[bar]) + (gamma * L0A)
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
            LRSI = _fdiv(CU, CU + CD)
        LRSI *= 100
        ExtLineBuffer[bar] = LRSI
        PointIndicator(31, ExtLineBuffer, ColorBuffer, HighLevel, MiddleLevel, LowLevel, bar)
    else:
        bar = _range_end(bar, rates_total, 1)
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


class Colorlaguerre(_MQL5Indicator):
    name = 'colorlaguerre'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'gamma': 0.7,
        'HighLevel': 85,
        'MiddleLevel': 50,
        'LowLevel': 15,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

