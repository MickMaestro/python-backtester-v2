"""yeffekt — converted from MQL5: MQL5 Indicators/yEffekt/yeffekt.mq5

Copyright: Copyright © 2008, MNS777; Link: mns777.ru@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, MNS777', 'link': 'mns777.ru@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 8421376, 13828244, 6053069, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'yEffekt'}, 'levels': [0.5, 0.0, -0.5], 'description': [], 'name': 'yeffekt', 'source': 'MQL5 Indicators/yEffekt/yeffekt.mq5', 'folder': 'yEffekt', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 5
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total + 1)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = 'yEffekt'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit1 = 0
    limit2 = 0
    bar = 0
    Index = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit1 = rates_total - 1 - min_rates_total
        limit2 = limit1 - 1
    else:
        limit1 = rates_total - prev_calculated
        limit2 = limit1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit1
    for bar in range(bar, 0 - 1, -1):
        Index = high[bar] - low[bar] + (high[bar + 1] - low[bar + 1]) + (high[bar + 2] - low[bar + 2]) + (high[bar + 3] - low[bar + 3]) + (high[bar + 4] - low[bar + 4])
        if Index != 0.0:
            if high[bar] > low[bar + 4]:
                IndBuffer[bar] = _fdiv(high[bar] - low[bar + 4], Index)
            if low[bar] < high[bar + 4]:
                IndBuffer[bar] = _fdiv(low[bar] - high[bar + 4], Index)
        else:
            IndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit2
    for bar in range(bar, 0 - 1, -1):
        ColorIndBuffer[bar] = 0.0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 1.0
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 3.0
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                ColorIndBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Yeffekt(_MQL5Indicator):
    name = 'yeffekt'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

