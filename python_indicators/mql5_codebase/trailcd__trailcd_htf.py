"""trailcd — converted from MQL5: MQL5 Indicators/TrailCD_HTF/trailcd.mq5

Схождение/расхождение быстрого и медленного тралов
Copyright: Copyright © 2007, John Smith; Link: https://www.mql5.com/ru/code/7383; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, John Smith', 'link': 'https://www.mql5.com/ru/code/7383', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 128, 9639167, 8421504, 16748574, 32768, 16776960]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TrailCD'}, 'levels': [], 'description': ['Схождение/расхождение быстрого и медленного тралов'], 'name': 'trailcd', 'source': 'MQL5 Indicators/TrailCD_HTF/trailcd.mq5', 'folder': 'TrailCD_HTF', 'inputs': [{'mql': 'TrailFast', 'py': 'TrailFast', 'param': 'TrailFast', 'type': 'uint', 'default': 25, 'label': 'Быстрый трал', 'sinput': False}, {'mql': 'TrailSlow', 'py': 'TrailSlow', 'param': 'TrailSlow', 'type': 'uint', 'default': 65, 'label': 'Медленный трал', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TrailFast = _input('TrailFast', 25)  # Быстрый трал
TrailSlow = _input('TrailSlow', 65)  # Медленный трал
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrailCD')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    nprice = 0
    clr = 0
    value_fast = 0
    value_slow = 0
    value_fast_ = 0
    value_slow_ = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        value_slow_ = _int(MathRound(_fdiv(price[first - 1], Point())))
        value_fast_ = value_slow_
    else:
        first = prev_calculated - 1
    value_fast = value_fast_
    value_slow = value_slow_
    bar = first
    for bar in range(bar, rates_total):
        nprice = _int(MathRound(_fdiv(price[bar], Point())))
        if value_fast < (nprice - _int(TrailFast)):
            value_fast = nprice - _int(TrailFast)
        if value_fast > (nprice + _int(TrailFast)):
            value_fast = nprice + _int(TrailFast)
        if value_slow < (nprice - _int(TrailSlow)):
            value_slow = nprice - _int(TrailSlow)
        if value_slow > (nprice + _int(TrailSlow)):
            value_slow = nprice + _int(TrailSlow)
        IndBuffer[bar] = value_fast - value_slow
        if bar <= (rates_total - 2):
            value_fast_ = value_fast
            value_slow_ = value_slow
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 3
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 6
            if IndBuffer[bar] == IndBuffer[bar - 1]:
                clr = 5
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 4
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] == IndBuffer[bar - 1]:
                clr = 1
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 2
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trailcd(_MQL5Indicator):
    name = 'trailcd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TrailFast': 25,  # Быстрый трал
        'TrailSlow': 65,  # Медленный трал
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

