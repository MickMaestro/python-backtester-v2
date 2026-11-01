"""momemtintime — converted from MQL5: MQL5 Indicators/Momemtum In Time/momemtintime.mq5

Copyright: Copyright © 2010, LeMan.; Link: b-market@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, LeMan.', 'link': 'b-market@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 5}, 'colors': {1: [255], 2: [65280]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0}, 'labels': {1: 'MomemtInTime Oscillator', 2: 'MomemtInTime'}, 'levels': [], 'description': [], 'name': 'momemtintime', 'source': 'MQL5 Indicators/Momemtum In Time/momemtintime.mq5', 'folder': 'Momemtum In Time', 'inputs': [{'mql': 'tm', 'py': 'tm', 'param': None, 'type': 'string', 'default': '00:00', 'label': 'time in the format hours:minutes', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
tm = _input('tm', '00:00')  # time in the format hours:minutes
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
OscBuffer = Arr(0, 0.0)
MomBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, OscBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, MomBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    shortname = Box("")
    StringConcatenate(shortname, 'MomemtInTime(', tm, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Open
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        MomBuffer[bar] = EMPTY_VALUE
        if TimeToString(time[bar], TIME_MINUTES) == tm:
            _s_OnCalculate_Open = open[bar]
            MomBuffer[bar] = 0.0
        OscBuffer[bar] = NormalizeDouble(close[bar] - _s_OnCalculate_Open, Digits())
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Open = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Momemtintime(_MQL5Indicator):
    name = 'momemtintime'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

