"""cronex_t_demarker_gf — converted from MQL5: MQL5 Indicators/Cronex_T_DeMarker_GF/cronex_t_demarker_gf.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 10, 2: 1, 3: 8, 4: 5, 5: 5}, 'colors': {1: [6053069, 8421376], 2: [16711680], 3: [255, 65280], 4: [65280], 5: [255]}, 'widths': {1: 2, 2: 1, 3: 2, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 4}, 'labels': {1: 'Divergence move Down', 2: 'DeMarker Smoothed', 3: 'DeMarker Smoothed move Down', 4: 'Cross Up', 5: 'Cross Down'}, 'levels': [], 'description': [], 'name': 'cronex_t_demarker_gf', 'source': 'MQL5 Indicators/Cronex_T_DeMarker_GF/cronex_t_demarker_gf.mq5', 'folder': 'Cronex_T_DeMarker_GF', 'inputs': [{'mql': 'DeMarker', 'py': 'DeMarker', 'param': 'DeMarker', 'type': 'uint', 'default': 24, 'label': '', 'sinput': False}, {'mql': 'DeMStep', 'py': 'DeMStep', 'param': 'DeMStep', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'b_', 'py': 'b_', 'param': 'b_', 'type': 'double', 'default': 61.8, 'label': 'coefficient x100', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
DeMarker = _input('DeMarker', 24)
DeMStep = _input('DeMStep', 4)
b_ = _input('b_', 61.8)  # coefficient x100
min_rates_ = 0
min_rates_total = 0
DiverTBuffer = Arr(0, 0.0)
ColorDiverTBuffer = Arr(0, 0.0)
DeMarkerBuffer = Arr(0, 0.0)
DeMarkerTBuffer = Arr(0, 0.0)
ColorDeMarkerTBuffer = Arr(0, 0.0)
CrossUpTBuffer = Arr(0, 0.0)
CrossDnTBuffer = Arr(0, 0.0)
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = _int(DeMarker + (DeMStep * 3))
    min_rates_total = min_rates_ + 1
    Ind_Handle[0] = iDeMarker(Symbol(), PERIOD_CURRENT, DeMarker + (DeMStep * 0))
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Failed to get handle of iDeMarker 1 indicator')
    Ind_Handle[1] = iDeMarker(Symbol(), PERIOD_CURRENT, DeMarker + (DeMStep * 1))
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Failed to get handle of iDeMarker 2 indicator')
    Ind_Handle[2] = iDeMarker(Symbol(), PERIOD_CURRENT, DeMarker + (DeMStep * 2))
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Failed to get handle of iDeMarker 3 indicator')
    Ind_Handle[3] = iDeMarker(Symbol(), PERIOD_CURRENT, DeMarker + (DeMStep * 3))
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Failed to get handle of iDeMarker 4 indicator')
    SetIndexBuffer(0, DiverTBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(0, DiverTBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorDiverTBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, DeMarkerBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, DeMarkerTBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ColorDeMarkerTBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, CrossUpTBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, CrossDnTBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DiverTBuffer, True)
    ArraySetAsSeries(ColorDiverTBuffer, True)
    ArraySetAsSeries(DeMarkerBuffer, True)
    ArraySetAsSeries(DeMarkerTBuffer, True)
    ArraySetAsSeries(ColorDeMarkerTBuffer, True)
    ArraySetAsSeries(CrossUpTBuffer, True)
    ArraySetAsSeries(CrossDnTBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    PlotIndexSetInteger(4, PLOT_ARROW, 108)
    shortname = 'Cronex_T_DeMarker_GF(' + _str(DeMarker) + ', ' + _str(DeMStep) + ', ' + _str(b_) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((rates_total < min_rates_total or BarsCalculated(Ind_Handle[0]) < rates_total) or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    DeMark1 = Arr(0, 0.0)
    DeMark2 = Arr(0, 0.0)
    DeMark3 = Arr(0, 0.0)
    DeMark4 = Arr(0, 0.0)
    ArraySetAsSeries(DeMark1, True)
    ArraySetAsSeries(DeMark2, True)
    ArraySetAsSeries(DeMark3, True)
    ArraySetAsSeries(DeMark4, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 2
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, DeMark1) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, DeMark2) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, DeMark3) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, DeMark4) <= 0:
        return 0
    maxbar = rates_total - min_rates_total - 2
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        DeMarkerBuffer[bar] = (((DeMark1[bar] + DeMark2[bar] + DeMark3[bar] + DeMark4[bar]) * 100) / 4) - 50
        DeMarkerTBuffer[bar] = T3.T3Series(maxbar, prev_calculated, rates_total, 0, b_, DeMarker, DeMarkerBuffer[bar], bar, True)
        CrossUpTBuffer[bar] = EMPTY_VALUE
        CrossDnTBuffer[bar] = EMPTY_VALUE
        if DeMarkerBuffer[bar + 1] <= DeMarkerTBuffer[bar + 1] and DeMarkerBuffer[bar] > DeMarkerTBuffer[bar]:
            CrossUpTBuffer[bar] = DeMarkerTBuffer[bar]
        if DeMarkerBuffer[bar + 1] >= DeMarkerTBuffer[bar + 1] and DeMarkerBuffer[bar] < DeMarkerTBuffer[bar]:
            CrossDnTBuffer[bar] = DeMarkerTBuffer[bar]
        if DeMarkerBuffer[bar] < DeMarkerTBuffer[bar]:
            ColorDeMarkerTBuffer[bar] = 0.0
        else:
            ColorDeMarkerTBuffer[bar] = 1.0
        DiverTBuffer[bar] = DeMarkerBuffer[bar] - DeMarkerTBuffer[bar]
        if (DeMarkerBuffer[bar] - DeMarkerTBuffer[bar]) < (DeMarkerBuffer[bar + 1] - DeMarkerTBuffer[bar + 1]):
            ColorDiverTBuffer[bar] = 0.0
        else:
            ColorDiverTBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
T3 = _alloc(CT3)
T3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CronexTDemarkerGf(_MQL5Indicator):
    name = 'cronex_t_demarker_gf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DeMarker': 24,
        'DeMStep': 4,
        'b_': 61.8,  # coefficient x100
    }

