"""laguerre — converted from MQL5: MQL5 Indicators/Laguerre_HTF/laguerre.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [0.75, 0.45, 0.15], 'description': [], 'name': 'laguerre', 'source': 'MQL5 Indicators/Laguerre_HTF/laguerre.mq5', 'folder': 'Laguerre_HTF', 'inputs': [{'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.7, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
gamma = _input('gamma', 0.7)
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'Laguerre_PlusDi(', gamma, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_L0A_, _s_OnCalculate_L0_, _s_OnCalculate_L1A_, _s_OnCalculate_L1_, _s_OnCalculate_L2A_, _s_OnCalculate_L2_, _s_OnCalculate_L3A_, _s_OnCalculate_L3_
    if rates_total < min_rates_total:
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
        first = begin
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
        ExtLineBuffer[bar] = LRSI
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


class Laguerre(_MQL5Indicator):
    name = 'laguerre'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'gamma': 0.7,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

