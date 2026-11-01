"""jmaslope — converted from MQL5: MQL5 Indicators/JMASlope_HTF/jmaslope.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 8388736, 8421504, 16711680, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'JMASlope'}, 'levels': [], 'description': [], 'name': 'jmaslope', 'source': 'MQL5 Indicators/JMASlope_HTF/jmaslope.mq5', 'folder': 'JMASlope_HTF', 'inputs': [{'mql': 'jLength', 'py': 'jLength', 'param': 'jLength', 'type': 'int', 'default': 14, 'label': 'Depth of smoothing', 'sinput': False}, {'mql': 'jPhase', 'py': 'jPhase', 'param': 'jPhase', 'type': 'int', 'default': 0, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
jLength = _input('jLength', 14)  # Depth of smoothing
jPhase = _input('jPhase', 0)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 30 + 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    JMA = CJJMA()
    JMA.JJMALengthCheck('jLength', jLength)
    JMA.JJMAPhaseCheck('jPhase', jPhase)
    IndicatorSetString(INDICATOR_SHORTNAME, 'JMASlope')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_j1jma
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    series = 0.0
    j1jma = 0.0
    djjma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_prev_j1jma = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = PriceSeries(IPC, bar, open, low, high, close)
        j1jma = _s_OnCalculate_JMA.JJMASeries(1, prev_calculated, rates_total, 0, jPhase, jLength, series, bar, False)
        djjma = _fdiv(j1jma - _s_OnCalculate_prev_j1jma, Point())
        IndBuffer[bar] = djjma
        if bar != (rates_total - 1):
            _s_OnCalculate_prev_j1jma = j1jma
        ColorIndBuffer[bar] = 2.0
        if djjma > 0:
            if djjma > IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 4.0
            if djjma < IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 3.0
        if djjma < 0:
            if djjma < IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 0.0
            if djjma > IndBuffer[bar - 1]:
                ColorIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_j1jma = 0.0
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jmaslope(_MQL5Indicator):
    name = 'jmaslope'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'jLength': 14,  # Depth of smoothing
        'jPhase': 0,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

