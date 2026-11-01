"""rbci — converted from MQL5: MQL5 Indicators/RBCI/rbci.mq5

Copyright: 2010,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh
from backtester.mql5.lib.indicatorsalgorithms import *  # #include indicatorsalgorithms.mqh

MQL5_META = {'props': {'copyright': '2010,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [65280], 2: [42495], 3: [42495], 4: [8421504], 5: [42495], 6: [42495]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4}, 'labels': {1: 'RBCI', 2: '+2Sigma', 3: '+Sigma', 4: 'Middle', 5: '-Sigma', 6: '-2Sigma'}, 'levels': [], 'description': [], 'name': 'rbci', 'source': 'MQL5 Indicators/RBCI/rbci.mq5', 'folder': 'RBCI', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 100, 'label': 'Period for Bollinger levels', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation', 'sinput': False}, {'mql': 'RBCIShift', 'py': 'RBCIShift', 'param': 'RBCIShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of RBCI in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh', 'indicatorsalgorithms.mqh']}

# ---- inputs and global variables
BBPeriod = _input('BBPeriod', 100)  # Period for Bollinger levels
BandsDeviation = _input('BandsDeviation', 2.0)  # Deviation
RBCIShift = _input('RBCIShift', 0)  # Horizontal shift of RBCI in bars
RBCIPeriod = 56
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, RBCIShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, RBCIPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'RBCI(', RBCIShift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, RBCIPeriod + BBPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, RBCIPeriod + BBPeriod)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, RBCIPeriod + BBPeriod)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, RBCIPeriod + BBPeriod)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, RBCIPeriod + BBPeriod)
    PlotIndexSetString(1, PLOT_LABEL, '+2Sigma')
    PlotIndexSetString(2, PLOT_LABEL, '+Sigma')
    PlotIndexSetString(3, PLOT_LABEL, 'Middle')
    PlotIndexSetString(4, PLOT_LABEL, '-Sigma')
    PlotIndexSetString(5, PLOT_LABEL, '-2Sigma')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (RBCIPeriod - 1 + begin):
        return 0
    first = 0
    bar = 0
    RBCI = 0.0
    BB = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = RBCIPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + RBCIPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        RBCI = (-35.52418194 * price[bar - 0]) - (29.33398965 * price[bar - 1]) - (18.42774496 * price[bar - 2]) - (5.341847567 * price[bar - 3]) + (7.023163695 * price[bar - 4]) + (16.17628156 * price[bar - 5]) + (20.65662104 * price[bar - 6]) + (20.32661158 * price[bar - 7]) + (16.27023906 * price[bar - 8]) + (10.35240127 * price[bar - 9]) + (4.596423992 * price[bar - 10]) + (0.5817527531 * price[bar - 11]) - (0.9559211961 * price[bar - 12]) - (0.2191111431 * price[bar - 13]) + (1.861734281 * price[bar - 14]) + (4.04333043 * price[bar - 15]) + (5.234224328 * price[bar - 16]) + (4.851086292 * price[bar - 17]) + (2.960440887 * price[bar - 18]) + (0.1815496232 * price[bar - 19]) - (2.591938701 * price[bar - 20]) - (4.535883446 * price[bar - 21]) - (5.180855695 * price[bar - 22]) - (4.54225353 * price[bar - 23]) - (3.067145982 * price[bar - 24]) - (1.431012658 * price[bar - 25]) - (0.2740437883 * price[bar - 26]) + (0.0260722294 * price[bar - 27]) - (0.5359717954 * price[bar - 28]) - (1.62749164 * price[bar - 29]) - (2.732295856 * price[bar - 30]) - (3.358959682 * price[bar - 31]) - (3.221651455 * price[bar - 32]) - (2.332625794 * price[bar - 33]) - (0.9760510577 * price[bar - 34]) + (0.4132650195 * price[bar - 35]) + (1.420216677 * price[bar - 36]) + (1.796998735 * price[bar - 37]) + (1.54127228 * price[bar - 38]) + (0.8771442423 * price[bar - 39]) + (0.1561848839 * price[bar - 40]) - (0.2797065802 * price[bar - 41]) - (0.2245901578 * price[bar - 42]) + (0.3278853523 * price[bar - 43]) + (1.188784148 * price[bar - 44]) + (2.057741075 * price[bar - 45]) + (2.627040982 * price[bar - 46]) + (2.697374234 * price[bar - 47]) + (2.228994128 * price[bar - 48]) + (1.353679243 * price[bar - 49]) + (0.3089253193 * price[bar - 50]) - (0.6386689841 * price[bar - 51]) - (1.276670767 * price[bar - 52]) - (1.513691845 * price[bar - 53]) - (1.377516078 * price[bar - 54]) - (1.615617397 * price[bar - 55])
        ExtLineBuffer0[bar] = -RBCI
    else:
        bar = _range_end(bar, rates_total, 1)
    if rates_total < (RBCIPeriod + BBPeriod - 1 + begin):
        return rates_total
    if prev_calculated == 0:
        first = RBCIPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin + RBCIPeriod + BBPeriod)
            PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, begin + RBCIPeriod + BBPeriod)
            PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, begin + RBCIPeriod + BBPeriod)
            PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, begin + RBCIPeriod + BBPeriod)
            PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, begin + RBCIPeriod + BBPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        _s_OnCalculate_BBands.BBandsSeries(RBCIPeriod + begin, prev_calculated, rates_total, BBPeriod, BandsDeviation, MODE_SMA, ExtLineBuffer0[bar], bar, False, _ElemRef(ExtLineBuffer5, bar), _ElemRef(ExtLineBuffer3, bar), _ElemRef(ExtLineBuffer1, bar))
        BB = (ExtLineBuffer1[bar] - ExtLineBuffer3[bar]) / 2
        ExtLineBuffer2[bar] = ExtLineBuffer3[bar] + BB
        ExtLineBuffer4[bar] = ExtLineBuffer3[bar] - BB
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_BBands = CBBands()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rbci(_MQL5Indicator):
    name = 'rbci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 100,  # Period for Bollinger levels
        'BandsDeviation': 2.0,  # Deviation
        'RBCIShift': 0,  # Horizontal shift of RBCI in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

