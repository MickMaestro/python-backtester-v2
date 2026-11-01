"""laguerrevolume — converted from MQL5: MQL5 Indicators/LaguerreVolume/laguerrevolume.mq5

Copyright: Copyright © 2007, Emerald King, t_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Emerald King, t_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13382297]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'LaguerreVolume'}, 'levels': [], 'description': [], 'name': 'laguerrevolume', 'source': 'MQL5 Indicators/LaguerreVolume/laguerrevolume.mq5', 'folder': 'LaguerreVolume', 'inputs': [{'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.618, 'label': 'smoothing ratio', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'inHighLevel', 'py': 'inHighLevel', 'param': 'inHighLevel', 'type': 'double', 'default': 0.75, 'label': '', 'sinput': False}, {'mql': 'inMiddleLevel', 'py': 'inMiddleLevel', 'param': 'inMiddleLevel', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'inLowLevel', 'py': 'inLowLevel', 'param': 'inLowLevel', 'type': 'double', 'default': 0.25, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
gamma = _input('gamma', 0.618)  # smoothing ratio
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
inHighLevel = _input('inHighLevel', 0.75)
inMiddleLevel = _input('inMiddleLevel', 0.5)
inLowLevel = _input('inLowLevel', 0.25)
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'LaguerreVolume', DoubleToString(gamma, 3), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inHighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inMiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, inLowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_L0A_, _s_OnCalculate_L0_, _s_OnCalculate_L1A_, _s_OnCalculate_L1_, _s_OnCalculate_L2A_, _s_OnCalculate_L2_, _s_OnCalculate_L3A_, _s_OnCalculate_L3_
    if rates_total < min_rates_total:
        return 0
    vol = 0
    limit = 0
    bar = 0
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L0A = 0.0
    L1A = 0.0
    L2A = 0.0
    L3A = 0.0
    CD = 0.0
    CU = 0.0
    RES = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        Vol = 0.0
        if VolumeType == VOLUME_TICK:
            Vol = float(tick_volume[0])
        else:
            Vol = float(volume[0])
        _s_OnCalculate_L0_ = Vol
        _s_OnCalculate_L1_ = Vol
        _s_OnCalculate_L2_ = Vol
        _s_OnCalculate_L3_ = Vol
        _s_OnCalculate_L0A_ = Vol
        _s_OnCalculate_L1A_ = Vol
        _s_OnCalculate_L2A_ = Vol
        _s_OnCalculate_L3A_ = Vol
    else:
        limit = rates_total - prev_calculated
    L0 = _s_OnCalculate_L0_
    L1 = _s_OnCalculate_L1_
    L2 = _s_OnCalculate_L2_
    L3 = _s_OnCalculate_L3_
    L0A = _s_OnCalculate_L0A_
    L1A = _s_OnCalculate_L1A_
    L2A = _s_OnCalculate_L2A_
    L3A = _s_OnCalculate_L3A_
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(tick_volume, True)
    else:
        ArraySetAsSeries(volume, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        if VolumeType == VOLUME_TICK:
            vol = tick_volume[bar]
        else:
            vol = volume[bar]
        L0 = ((1 - gamma) * vol) + (gamma * L0A)
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
        RES = CU + CD
        if RES:
            IndBuffer[bar] = _fdiv(CU, RES)
        else:
            IndBuffer[bar] = 0.0
        if bar:
            _s_OnCalculate_L0_ = L0
            _s_OnCalculate_L1_ = L1
            _s_OnCalculate_L2_ = L2
            _s_OnCalculate_L3_ = L3
            _s_OnCalculate_L0A_ = L0A
            _s_OnCalculate_L1A_ = L1A
            _s_OnCalculate_L2A_ = L2A
            _s_OnCalculate_L3A_ = L3A
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


class Laguerrevolume(_MQL5Indicator):
    name = 'laguerrevolume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'gamma': 0.618,  # smoothing ratio
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'Shift': 0,  # horizontal shift of the indicator in bars
        'inHighLevel': 0.75,
        'inMiddleLevel': 0.5,
        'inLowLevel': 0.25,
    }

