"""t3taotra — converted from MQL5: MQL5 Indicators/T3Taotra/t3taotra.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [65535], 2: [255], 3: [16711935], 4: [16776960], 5: [3329330], 6: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'T3Taotra'}, 'levels': [], 'description': [], 'name': 't3taotra', 'source': 'MQL5 Indicators/T3Taotra/t3taotra.mq5', 'folder': 'T3Taotra', 'inputs': [{'mql': 'T3_Period_1', 'py': 'T3_Period_1', 'param': 'T3_Period_1', 'type': 'int', 'default': 3, 'label': 'Indicator period 1', 'sinput': False}, {'mql': 'T3_Period_2', 'py': 'T3_Period_2', 'param': 'T3_Period_2', 'type': 'int', 'default': 5, 'label': 'Indicator period 2', 'sinput': False}, {'mql': 'T3_Period_3', 'py': 'T3_Period_3', 'param': 'T3_Period_3', 'type': 'int', 'default': 8, 'label': 'Indicator period 3', 'sinput': False}, {'mql': 'T3_Period_4', 'py': 'T3_Period_4', 'param': 'T3_Period_4', 'type': 'int', 'default': 12, 'label': 'Indicator period 4', 'sinput': False}, {'mql': 'T3_Period_5', 'py': 'T3_Period_5', 'param': 'T3_Period_5', 'type': 'int', 'default': 21, 'label': 'Indicator period 5', 'sinput': False}, {'mql': 'T3_Period_6', 'py': 'T3_Period_6', 'param': 'T3_Period_6', 'type': 'int', 'default': 34, 'label': 'Indicator period 6', 'sinput': False}, {'mql': 'Smooth_Curvature', 'py': 'Smooth_Curvature', 'param': 'Smooth_Curvature', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'int', 'default': 0, 'label': 'Shift of the indicator 1 along the timeline', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'int', 'default': 0, 'label': 'Shift of the indicator 2 along the timeline', 'sinput': False}, {'mql': 'Shift3', 'py': 'Shift3', 'param': 'Shift3', 'type': 'int', 'default': 0, 'label': 'Shift of the indicator 3 along the timeline', 'sinput': False}, {'mql': 'Shift4', 'py': 'Shift4', 'param': 'Shift4', 'type': 'int', 'default': 0, 'label': 'Shift of the indicator 4 along the timeline', 'sinput': False}, {'mql': 'Shift5', 'py': 'Shift5', 'param': 'Shift5', 'type': 'int', 'default': 0, 'label': 'Shift of the indicator 5 along the timeline', 'sinput': False}, {'mql': 'Shift6', 'py': 'Shift6', 'param': 'Shift6', 'type': 'int', 'default': 0, 'label': 'Shift of the indicator 6 along the timeline', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
T3_Period_1 = _input('T3_Period_1', 3)  # Indicator period 1
T3_Period_2 = _input('T3_Period_2', 5)  # Indicator period 2
T3_Period_3 = _input('T3_Period_3', 8)  # Indicator period 3
T3_Period_4 = _input('T3_Period_4', 12)  # Indicator period 4
T3_Period_5 = _input('T3_Period_5', 21)  # Indicator period 5
T3_Period_6 = _input('T3_Period_6', 34)  # Indicator period 6
Smooth_Curvature = _input('Smooth_Curvature', 100)
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
Shift1 = _input('Shift1', 0)  # Shift of the indicator 1 along the timeline
Shift2 = _input('Shift2', 0)  # Shift of the indicator 2 along the timeline
Shift3 = _input('Shift3', 0)  # Shift of the indicator 3 along the timeline
Shift4 = _input('Shift4', 0)  # Shift of the indicator 4 along the timeline
Shift5 = _input('Shift5', 0)  # Shift of the indicator 5 along the timeline
Shift6 = _input('Shift6', 0)  # Shift of the indicator 6 along the timeline
Ind_Buffer1 = Arr(0, 0.0)
Ind_Buffer2 = Arr(0, 0.0)
Ind_Buffer3 = Arr(0, 0.0)
Ind_Buffer4 = Arr(0, 0.0)
Ind_Buffer5 = Arr(0, 0.0)
Ind_Buffer6 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, Ind_Buffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, Ind_Buffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, Ind_Buffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift3)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, Ind_Buffer4, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift4)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, Ind_Buffer5, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift5)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, Ind_Buffer6, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift6)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'T3Taotra( ', T3_Period_1, ', ', T3_Period_2, ', ', T3_Period_3, ', ', T3_Period_4, ', ', T3_Period_5, ', ', T3_Period_6, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    T3_ = CT3()
    T3_.MALengthCheck_1('T3_Period_1', T3_Period_1)
    T3_.MALengthCheck_1('T3_Period_2', T3_Period_2)
    T3_.MALengthCheck_1('T3_Period_3', T3_Period_3)
    T3_.MALengthCheck_1('T3_Period_4', T3_Period_4)
    T3_.MALengthCheck_1('T3_Period_5', T3_Period_5)
    T3_.MALengthCheck_1('T3_Period_6', T3_Period_6)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 0:
        return 0
    series = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = PriceSeries(IPC, bar, open, low, high, close)
        Ind_Buffer1[bar] = _s_OnCalculate_T3_[0].T3Series(0, prev_calculated, rates_total, 0, Smooth_Curvature, T3_Period_1, series, bar, False)
        Ind_Buffer2[bar] = _s_OnCalculate_T3_[1].T3Series(0, prev_calculated, rates_total, 0, Smooth_Curvature, T3_Period_2, series, bar, False)
        Ind_Buffer3[bar] = _s_OnCalculate_T3_[2].T3Series(0, prev_calculated, rates_total, 0, Smooth_Curvature, T3_Period_3, series, bar, False)
        Ind_Buffer4[bar] = _s_OnCalculate_T3_[3].T3Series(0, prev_calculated, rates_total, 0, Smooth_Curvature, T3_Period_4, series, bar, False)
        Ind_Buffer5[bar] = _s_OnCalculate_T3_[4].T3Series(0, prev_calculated, rates_total, 0, Smooth_Curvature, T3_Period_5, series, bar, False)
        Ind_Buffer6[bar] = _s_OnCalculate_T3_[5].T3Series(0, prev_calculated, rates_total, 0, Smooth_Curvature, T3_Period_6, series, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_T3_ = Arr(6, 0, dyn=False, factory=CT3)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3taotra(_MQL5Indicator):
    name = 't3taotra'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T3_Period_1': 3,  # Indicator period 1
        'T3_Period_2': 5,  # Indicator period 2
        'T3_Period_3': 8,  # Indicator period 3
        'T3_Period_4': 12,  # Indicator period 4
        'T3_Period_5': 21,  # Indicator period 5
        'T3_Period_6': 34,  # Indicator period 6
        'Smooth_Curvature': 100,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER', 10: 'PRICE_TRENDFOLLOW0', 11: 'PRICE_TRENDFOLLOW1'}, default=1),  # Price constant
        'Shift1': 0,  # Shift of the indicator 1 along the timeline
        'Shift2': 0,  # Shift of the indicator 2 along the timeline
        'Shift3': 0,  # Shift of the indicator 3 along the timeline
        'Shift4': 0,  # Shift of the indicator 4 along the timeline
        'Shift5': 0,  # Shift of the indicator 5 along the timeline
        'Shift6': 0,  # Shift of the indicator 6 along the timeline
    }

