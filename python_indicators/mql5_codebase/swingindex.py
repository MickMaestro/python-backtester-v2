"""swingindex — converted from MQL5: MQL5 Indicators/Swing Index/swingindex.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SwingIndex'}, 'levels': [], 'description': [], 'name': 'swingindex', 'source': 'MQL5 Indicators/Swing Index/swingindex.mq5', 'folder': 'Swing Index', 'inputs': [{'mql': 'T', 'py': 'T_v', 'param': 'T_v', 'type': 'double', 'default': 30000.0, 'label': 'Scaling ratio', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
T_v = _input('T_v', 30000.0)  # Scaling ratio
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
SWINGINDEX = Arr(0, 0.0)
StartBars = 1

def OnInit():
    SetIndexBuffer(0, SWINGINDEX, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'SwingIndex( ', DoubleToString(T_v, 2), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    O = 0.0
    O1 = 0.0
    C = 0.0
    C1 = 0.0
    H = 0.0
    L = 0.0
    K = 0.0
    TR = 0.0
    SH1 = 0.0
    SI = 0.0
    ER = 0.0
    R = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        O = open[bar]
        O1 = open[bar - 1]
        C = close[bar]
        C1 = close[bar - 1]
        H = high[bar]
        L = low[bar]
        K = MathMax(MathAbs(H - C1), MathAbs(L - C1))
        TR = MathMax(MathMax(MathAbs(H - C1), MathAbs(L - C1)), MathAbs(H - L))
        ER = 0.0
        if C1 > H:
            ER = MathAbs(H - C1)
        if C1 < L:
            ER = MathAbs(L - C1)
        SH1 = MathAbs(C1 - O1)
        R = TR - (0.5 * ER) + (0.25 * SH1)
        SI = 0.0
        if R != 0:
            SI = _fdiv(50 * (C - C1 + (0.5 * (C - O)) + (0.25 * (C1 - O1))) * (K / T_v), R)
        SWINGINDEX[bar] = SI
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Swingindex(_MQL5Indicator):
    name = 'swingindex'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T_v': 30000.0,  # Scaling ratio
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

