"""Momentum YTG — converted from MQL5: MQL5 Indicators/Momentum YTG/Momentum YTG.mq5

Copyright: Iurii Tokman (YTG); Link: http://ytg.com.ua; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Iurii Tokman (YTG)', 'link': 'http://ytg.com.ua', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 3}, 'colors': {1: [255], 2: [32768]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Momentum YTG', 'source': 'MQL5 Indicators/Momentum YTG/Momentum YTG.mq5', 'folder': 'Momentum YTG', 'inputs': [{'mql': 'MomentumPeriod', 'py': 'MomentumPeriod', 'param': 'MomentumPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MomentumPeriod = _input('MomentumPeriod', 14)
B0 = Arr(0, 0.0)
B1 = Arr(0, 0.0)
M_Period = 0

def OnInit():
    global M_Period
    if MomentumPeriod <= 0:
        M_Period = 14
        Print('Input parameter MomentumPeriod has wrong value. Indicator will use value ', M_Period)
    else:
        M_Period = MomentumPeriod
    SetIndexBuffer(0, B0, INDICATOR_DATA)
    SetIndexBuffer(1, B1, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Momentum YTG' + '(' + _str(M_Period) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, M_Period - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, M_Period - 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    res = 0.0
    StartCalcPosition = M_Period - 1 + begin
    if rates_total < StartCalcPosition:
        return 0
    pos = prev_calculated - 1
    if pos < StartCalcPosition:
        pos = begin + M_Period
    for i in range(pos, rates_total):
        res = _fdiv(price[i] * 100, price[i - M_Period]) - 100.0
        if res < 0:
            B0[i] = res
        else:
            B1[i] = res
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MomentumYTG(_MQL5Indicator):
    name = 'Momentum YTG'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MomentumPeriod': 14,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

