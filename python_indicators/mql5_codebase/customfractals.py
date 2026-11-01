"""CustomFractals — converted from MQL5: MQL5 Indicators/Custom Fractals/CustomFractals.mq5

Copyright: 2009-2020, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009-2020, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Fractal Up', 2: 'Fractal Down'}, 'levels': [], 'description': [], 'name': 'CustomFractals', 'source': 'MQL5 Indicators/Custom Fractals/CustomFractals.mq5', 'folder': 'Custom Fractals', 'inputs': [{'mql': 'how_many', 'py': 'how_many', 'param': 'how_many', 'type': 'int', 'default': 2, 'label': 'bars left and right', 'sinput': False}, {'mql': 'how_far_away', 'py': 'how_far_away', 'param': 'how_far_away', 'type': 'int', 'default': -10, 'label': '', 'sinput': False}, {'mql': 'sign_size', 'py': 'sign_size', 'param': 'sign_size', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'wingding_num1', 'py': 'wingding_num1', 'param': 'wingding_num1', 'type': 'int', 'default': 217, 'label': '', 'sinput': False}, {'mql': 'wingding_num2', 'py': 'wingding_num2', 'param': 'wingding_num2', 'type': 'int', 'default': 218, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtUpperBuffer = Arr(0, 0.0)
ExtLowerBuffer = Arr(0, 0.0)
ExtArrowShift = -10
ExtWingding01 = 217
ExtWingding02 = 218
how_many = _input('how_many', 2)  # bars left and right
how_far_away = _input('how_far_away', -10)
sign_size = _input('sign_size', 3)
wingding_num1 = _input('wingding_num1', 217)
wingding_num2 = _input('wingding_num2', 218)

def OnInit():
    global ExtArrowShift, ExtWingding01, ExtWingding02
    SetIndexBuffer(0, ExtUpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLowerBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if wingding_num1 < 0 or wingding_num1 > 255:
        ExtWingding01 = 217
        Print('unicode character must be within 255+0')
    else:
        ExtWingding01 = wingding_num1
    if wingding_num2 < 0 or wingding_num2 > 255:
        ExtWingding02 = 218
        Print('unicode character must be within 255+0')
    else:
        ExtWingding02 = wingding_num2
    PlotIndexSetInteger(0, PLOT_ARROW, wingding_num1)
    PlotIndexSetInteger(1, PLOT_ARROW, wingding_num2)
    ExtArrowShift = how_far_away
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, ExtArrowShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -ExtArrowShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, sign_size)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, sign_size)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < ((how_many * 2) + 1):
        return 0
    start = 0
    if prev_calculated < ((how_many * 2) + 3):
        start = how_many
    else:
        start = rates_total - ((how_many * 2) + 1)
    ArrayInitialize(ExtUpperBuffer, EMPTY_VALUE)
    ArrayInitialize(ExtLowerBuffer, EMPTY_VALUE)
    for i in range(start, rates_total - (how_many + 1)):
        IsFractalUp = True
        j = 1
        while j <= how_many and IsFractalUp == True:
            IsFractalUp &= high[i] > high[i + j]
            IsFractalUp &= high[i] > high[i - j]
            j += 1
        if IsFractalUp:
            ExtUpperBuffer[i] = high[i]
        else:
            ExtUpperBuffer[i] = EMPTY_VALUE
    for i in range(start, rates_total - (how_many + 1)):
        IsFractalDn = True
        j = 1
        while j <= how_many and IsFractalDn == True:
            IsFractalDn &= low[i] < low[i + j]
            IsFractalDn &= low[i] < low[i - j]
            j += 1
        if IsFractalDn:
            ExtLowerBuffer[i] = low[i]
        else:
            ExtLowerBuffer[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomFractals(_MQL5Indicator):
    name = 'CustomFractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'how_many': 2,  # bars left and right
        'how_far_away': -10,
        'sign_size': 3,
        'wingding_num1': 217,
        'wingding_num2': 218,
    }

