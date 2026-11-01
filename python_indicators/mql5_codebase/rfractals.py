"""rfractals — converted from MQL5: MQL5 Indicators/RFractals/rfractals.mq5

Fine Fractals
Copyright: Copyright © 2009 Lizhniyk E; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009 Lizhniyk E', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16748574], 2: [13850042]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Up Fractal', 2: 'Down Fractal'}, 'levels': [], 'description': ['Fine Fractals'], 'name': 'rfractals', 'source': 'MQL5 Indicators/RFractals/rfractals.mq5', 'folder': 'RFractals', 'inputs': [{'mql': 'RangeFractal', 'py': 'RangeFractal', 'param': 'RangeFractal', 'type': 'uint', 'default': 5, 'label': 'fractal rank (odd numbers not less than 3)', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'int', 'default': 217, 'label': 'upper fractal label', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'int', 'default': 218, 'label': 'lower fractal label', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RangeFractal = _input('RangeFractal', 5)  # fractal rank (odd numbers not less than 3)
UpLable = _input('UpLable', 217)  # upper fractal label
DnLable = _input('DnLable', 218)  # lower fractal label
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
center = 0
min_rates_total = 0
range_fractal = 0

def OnInit():
    global center, min_rates_total, range_fractal
    range_fractal = _int(RangeFractal)
    if _imod(range_fractal, 2) == 0:
        range_fractal += 1
    range_fractal = MathMax(range_fractal, 3)
    center = _idiv(range_fractal, 2) + 1
    min_rates_total = range_fractal + 1
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Up Fractal')
    PlotIndexSetInteger(0, PLOT_ARROW, UpLable)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'Down Fractal')
    PlotIndexSetInteger(1, PLOT_ARROW, DnLable)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RFractals(' + _str(range_fractal) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    barC = 0
    cur = 0.0
    found = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        UpBuffer[bar] = 0.0
        DnBuffer[bar] = 0.0
        barC = bar + center
        found = False
        cur = high[barC]
        if cur > high[bar + 1] and cur > high[bar + range_fractal]:
            found = True
        else:
            found = False
        if found:
            for j in range(1, center):
                if cur >= high[barC - j] and cur >= high[barC + j]:
                    found = True
                else:
                    found = False
                    break
        if found:
            UpBuffer[barC] = cur
            UpBuffer[barC + 1] = 0.0
        found = False
        cur = low[barC]
        if cur < low[bar + 1] and cur < low[bar + range_fractal]:
            found = True
        else:
            found = False
        if found:
            for k in range(1, center):
                if cur <= low[barC - k] and cur <= low[barC + k]:
                    found = True
                else:
                    found = False
                    break
        if found:
            DnBuffer[barC] = cur
            DnBuffer[barC + 1] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rfractals(_MQL5Indicator):
    name = 'rfractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangeFractal': 5,  # fractal rank (odd numbers not less than 3)
        'UpLable': 217,  # upper fractal label
        'DnLable': 218,  # lower fractal label
    }

