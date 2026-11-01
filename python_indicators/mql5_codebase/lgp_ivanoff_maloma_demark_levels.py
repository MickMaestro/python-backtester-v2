"""LGP_Ivanoff_Maloma-Demark_levels — converted from MQL5: MQL5 Indicators/LGP_Ivanoff_Maloma-Demark_levels/LGP_Ivanoff_Maloma-Demark_levels.mq5

Copyright: Copyright © 2006, LGP; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, LGP', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [255], 2: [3329330], 3: [16711935], 4: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Fractal Up', 2: 'Fractal Down', 3: 'Signal Up', 4: 'Signal Down'}, 'levels': [], 'description': [], 'name': 'LGP_Ivanoff_Maloma-Demark_levels', 'source': 'MQL5 Indicators/LGP_Ivanoff_Maloma-Demark_levels/LGP_Ivanoff_Maloma-Demark_levels.mq5', 'folder': 'LGP_Ivanoff_Maloma-Demark_levels', 'inputs': [{'mql': 'width_H_L', 'py': 'width_H_L', 'param': 'width_H_L', 'type': 'uint', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
width_H_L = _input('width_H_L', 0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)
ExtMapBuffer4 = Arr(0, 0.0)
min_rates_total = 0
P = 0.0

def OnInit():
    global P, min_rates_total
    min_rates_total = 6
    if Period() >= PERIOD_D1:
        P = 15 * Point()
    elif Period() >= PERIOD_H4:
        P = 7 * Point()
    elif Period() >= PERIOD_H1:
        P = 4 * Point()
    elif Period() >= PERIOD_M30:
        P = 3 * Point()
    elif Period() >= PERIOD_M15:
        P = 2 * Point()
    elif Period() >= PERIOD_M5:
        P = 1 * Point()
    if Period() == PERIOD_M1:
        P = 0.5 * Point()
    shortname = Box("")
    StringConcatenate(shortname, 'LGP_Ivanoff_Maloma-Demark_levels(', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 217)
    ArraySetAsSeries(ExtMapBuffer1, True)
    SetIndexBuffer(1, ExtMapBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 218)
    ArraySetAsSeries(ExtMapBuffer3, True)
    SetIndexBuffer(2, ExtMapBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBuffer2, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 217)
    SetIndexBuffer(3, ExtMapBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBuffer4, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(3, PLOT_ARROW, 218)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = rates_total - min_rates_total - 3
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Close, True)
    bar = 1
    while bar <= limit:
        ExtMapBuffer1[bar] = 0.0
        ExtMapBuffer2[bar] = 0.0
        j = bar
        for k in range(bar, rates_total - 2 + 1):
            if Close[j + 1] != Close[bar]:
                break
            j += 1
        if (Close[bar] > Close[bar - 1] and Close[bar] > Close[j + 1]) and Close[j + 1] > Close[j + 2]:
            if Close[bar] > High[bar - 1]:
                ExtMapBuffer2[bar - 1] = Close[bar - 1] + P
            else:
                ExtMapBuffer1[bar] = High[bar] + P
        bar = j
        bar += 1
    bar = 1
    while bar <= limit:
        ExtMapBuffer3[bar] = 0.0
        ExtMapBuffer4[bar] = 0.0
        j = bar
        for k in range(bar, rates_total - 2 + 1):
            if Close[j + 1] != Close[bar]:
                break
            j += 1
        if (Close[bar] < Close[bar - 1] and Close[bar] < Close[j + 1]) and Close[j + 1] < Close[j + 2]:
            if Close[bar] < Low[bar - 1]:
                ExtMapBuffer4[bar - 1] = Close[bar - 1] - P
            else:
                ExtMapBuffer3[bar] = Low[bar] - P
        bar = j
        bar += 1
    ExtMapBuffer1[0] = 0.0
    ExtMapBuffer2[0] = 0.0
    ExtMapBuffer3[0] = 0.0
    ExtMapBuffer4[0] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LGPIvanoffMalomaDemarkLevels(_MQL5Indicator):
    name = 'LGP_Ivanoff_Maloma-Demark_levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'width_H_L': 0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

