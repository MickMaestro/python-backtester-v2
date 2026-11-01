"""bullsbearseyes — converted from MQL5: MQL5 Indicators/BullsBearsEyes/bullsbearseyes.mq5

BullsBearsEyes
Copyright: Copyright © 2007, EmeraldKing, transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, EmeraldKing, transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BullsBearsEyes'}, 'levels': [1.0, 0.75, 0.5, 0.25, 0.0], 'description': ['BullsBearsEyes'], 'name': 'bullsbearseyes', 'source': 'MQL5 Indicators/BullsBearsEyes/bullsbearseyes.mq5', 'folder': 'BullsBearsEyes', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'double', 'default': 13.0, 'label': 'Indicator smoothing period', 'sinput': False}, {'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.6, 'label': 'Indicator smoothing ratio', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 13.0)  # Indicator smoothing period
gamma = _input('gamma', 0.6)  # Indicator smoothing ratio
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
BullsBearsEyes = Arr(0, 0.0)
Bears_Handle = 0
Bulls_Handle = 0
min_rates_total = 0

def OnInit():
    global Bears_Handle, Bulls_Handle, min_rates_total
    min_rates_total = _int(period + 1)
    Bears_Handle = iBearsPower(None, 0, _int(period))
    if Bears_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iBearsPower indicator')
    Bulls_Handle = iBullsPower(None, 0, _int(period))
    if Bulls_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iBullsPower indicator')
    SetIndexBuffer(0, BullsBearsEyes, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(BullsBearsEyes, True)
    shortname = Box("")
    StringConcatenate(shortname, 'BullsBearsEyes(', period, ', ', gamma, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_L0_, _s_OnCalculate_L1_, _s_OnCalculate_L2_, _s_OnCalculate_L3_
    if (BarsCalculated(Bears_Handle) < rates_total or BarsCalculated(Bulls_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    result = 0.0
    Bears = Arr(0, 0.0)
    Bulls = Arr(0, 0.0)
    CU = 0.0
    CD = 0.0
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L0A = 0.0
    L1A = 0.0
    L2A = 0.0
    L3A = 0.0
    limit = 0
    bar = 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Bears, True)
    ArraySetAsSeries(Bulls, True)
    if CopyBuffer(Bears_Handle, 0, 0, to_copy, Bears) <= 0:
        return 0
    if CopyBuffer(Bulls_Handle, 0, 0, to_copy, Bulls) <= 0:
        return 0
    L0 = _s_OnCalculate_L0_
    L1 = _s_OnCalculate_L1_
    L2 = _s_OnCalculate_L2_
    L3 = _s_OnCalculate_L3_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_L0_ = L0
            _s_OnCalculate_L1_ = L1
            _s_OnCalculate_L2_ = L2
            _s_OnCalculate_L3_ = L3
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        L0 = ((1.0 - gamma) * (Bears[bar] + Bulls[bar])) + (gamma * L0A)
        L1 = ((-gamma) * L0) + L0A + (gamma * L1A)
        L2 = ((-gamma) * L1) + L1A + (gamma * L2A)
        L3 = ((-gamma) * L2) + L2A + (gamma * L3A)
        CU = 0.0
        CD = 0.0
        result = 0.0
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
            result = _fdiv(CU, CU + CD)
        BullsBearsEyes[bar] = result
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_L0_ = 0.0
_s_OnCalculate_L1_ = 0.0
_s_OnCalculate_L2_ = 0.0
_s_OnCalculate_L3_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bullsbearseyes(_MQL5Indicator):
    name = 'bullsbearseyes'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 13.0,  # Indicator smoothing period
        'gamma': 0.6,  # Indicator smoothing ratio
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

