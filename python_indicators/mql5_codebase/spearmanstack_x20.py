"""spearmanstack_x20 — converted from MQL5: MQL5 Indicators/SpearmanStack_X20 (SpearmanRankCorrelation indicator threads)/spearmanstack_x20.mq5

SpearmanStack-X8
Copyright: Copyright © 2010, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_minimum': -1.0, 'indicator_maximum': 1.0, 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [0.5, 0.0, -0.5], 'description': ['SpearmanStack-X8'], 'name': 'spearmanstack_x20', 'source': 'MQL5 Indicators/SpearmanStack_X20 (SpearmanRankCorrelation indicator threads)/spearmanstack_x20.mq5', 'folder': 'SpearmanStack_X20 (SpearmanRankCorrelation indicator threads)', 'inputs': [{'mql': 'rangeN', 'py': 'rangeN', 'param': 'rangeN', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'CalculatedBars', 'py': 'CalculatedBars', 'param': 'CalculatedBars', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'direction', 'py': 'direction', 'param': 'direction', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
rangeN = _input('rangeN', 14)
step = _input('step', 6)
CalculatedBars = _input('CalculatedBars', 0)
Maxrange = 0
direction = _input('direction', True)
Spear_Handle = Arr(20, 0, dyn=False)
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def OnInit():
    global Maxrange, min_rates_total
    min_rates_total = _int(rangeN + (step * (20 - 1))) + 1
    Maxrange = rangeN + (20 * (step - 1 + 1) * 2)
    period = rangeN
    for numb in range(0, 20):
        period += step
        Spear_Handle[numb] = iCustom(None, 0, 'SpearmanRankCorrelation', period, CalculatedBars, Maxrange, direction)
        if Spear_Handle[numb] == INVALID_HANDLE:
            Print(' Failed to get the SpearmanRankCorrelation indicator handle ', numb)
        shortname = Box('')
        StringConcatenate(shortname, 'SpearmanRankCorrelation X', 20, '*', period, ')')
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        SetIndexBuffer(numb, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        PlotIndexSetInteger(numb, PLOT_DRAW_TYPE, PlotIndexGetInteger(0, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb, PLOT_LINE_STYLE, PlotIndexGetInteger(0, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb, PLOT_LINE_WIDTH, PlotIndexGetInteger(0, PLOT_LINE_WIDTH))
        PlotIndexSetInteger(numb, PLOT_LINE_COLOR, PlotIndexGetInteger(0, PLOT_LINE_COLOR))
    shortname = Box("")
    StringConcatenate(shortname, 'SpearmanRankCorrelation X', 20, '*', rangeN, '(', step, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for numb in range(0, 20):
        if BarsCalculated(Spear_Handle[numb]) < min_rates_total:
            return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    for numb in range(0, 20):
        if CopyBuffer(Spear_Handle[numb], 0, 0, to_copy, Ind[numb].IndBuffer) <= 0:
            return 0
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(20, 0, dyn=False, factory=CIndicatorsBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpearmanstackX20(_MQL5Indicator):
    name = 'spearmanstack_x20'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'rangeN': 14,
        'step': 6,
        'CalculatedBars': 0,
        'direction': True,
    }
    y_range = (-1.0, 1.0)

