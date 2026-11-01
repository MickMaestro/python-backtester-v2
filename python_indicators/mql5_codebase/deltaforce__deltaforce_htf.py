"""DeltaForce — converted from MQL5: MQL5 Indicators/DeltaForce_HTF/DeltaForce.mq5

Copyright: Copyright © 2004, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [16711680, 16748574], 2: [16711935, 8388736]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'High', 2: 'Low'}, 'levels': [], 'description': [], 'name': 'DeltaForce', 'source': 'MQL5 Indicators/DeltaForce_HTF/DeltaForce.mq5', 'folder': 'DeltaForce_HTF', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
HIndBuffer = Arr(0, 0.0)
ColorHIndBuffer = Arr(0, 0.0)
LIndBuffer = Arr(0, 0.0)
ColorLIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, HIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorHIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, LIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorLIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DeltaForce')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_deltah_prev, _s_OnCalculate_deltal_prev, _s_OnCalculate_resh_prev, _s_OnCalculate_resl_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    diff = 0
    deltah = 0
    deltal = 0
    resh = 0
    resl = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_deltah_prev = 0
        _s_OnCalculate_deltal_prev = 0
        _s_OnCalculate_resh_prev = 0
        _s_OnCalculate_resl_prev = 0
    else:
        first = prev_calculated - 1
    deltah = _s_OnCalculate_deltah_prev
    deltal = _s_OnCalculate_deltal_prev
    resh = _s_OnCalculate_resh_prev
    resl = _s_OnCalculate_resl_prev
    bar = first
    for bar in range(bar, rates_total):
        HIndBuffer[bar] = 0.0
        LIndBuffer[bar] = 0.0
        diff = _int(_fdiv(close[bar] - close[bar - 1], Point()))
        if diff > 0:
            resl = 0
            if not resh:
                deltah = 0
            deltah += diff
            resh = 1
        if not resh:
            deltah = 0
        HIndBuffer[bar] = deltah
        if diff < 0:
            resh = 0
            if not resl:
                deltal = 0
            deltal += diff
            resl = 1
        if not resl:
            deltal = 0
        LIndBuffer[bar] = deltal
        if bar < (rates_total - 1):
            _s_OnCalculate_deltah_prev = deltah
            _s_OnCalculate_deltal_prev = deltal
            _s_OnCalculate_resh_prev = resh
            _s_OnCalculate_resl_prev = resl
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + 1
    bar = first
    for bar in range(bar, rates_total):
        ColorHIndBuffer[bar] = ColorHIndBuffer[bar - 1]
        if HIndBuffer[bar - 1] < HIndBuffer[bar]:
            ColorHIndBuffer[bar] = 0.0
        elif HIndBuffer[bar - 1] > HIndBuffer[bar]:
            ColorHIndBuffer[bar] = 1.0
        ColorLIndBuffer[bar] = ColorLIndBuffer[bar - 1]
        if LIndBuffer[bar - 1] > LIndBuffer[bar]:
            ColorLIndBuffer[bar] = 0.0
        elif LIndBuffer[bar - 1] < LIndBuffer[bar]:
            ColorLIndBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_deltah_prev = 0
_s_OnCalculate_deltal_prev = 0
_s_OnCalculate_resh_prev = 0
_s_OnCalculate_resl_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeltaForce(_MQL5Indicator):
    name = 'DeltaForce'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

