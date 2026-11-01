"""cgoscillator — converted from MQL5: MQL5 Indicators/CG Oscillator/cgoscillator.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'CG Oscillator', 2: 'Trigger'}, 'levels': [0.0], 'description': [], 'name': 'cgoscillator', 'source': 'MQL5 Indicators/CG Oscillator/cgoscillator.mq5', 'folder': 'CG Oscillator', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'Indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)  # Indicator period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
CGBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
CGshift = 0.0

def OnInit():
    global CGshift, min_rates_total
    min_rates_total = Length
    CGshift = (Length + 1.0) / 2.0
    SetIndexBuffer(0, CGBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 3)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 3)
    shortname = Box("")
    StringConcatenate(shortname, 'CG Oscillator(', Length, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    Num = 0.0
    Denom = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Num = 0.0
        Denom = 0.0
        for count in range(0, Length):
            price = (high[bar - count] + low[bar - count]) / 2.0
            Num += (1.0 + count) * price
            Denom += price
        if Denom != 0.0:
            CGBuffer[bar] = _fdiv(-Num, Denom) + CGshift
        else:
            CGBuffer[bar] = 0.0
        TriggerBuffer[bar] = CGBuffer[bar - 1]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Cgoscillator(_MQL5Indicator):
    name = 'cgoscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Indicator period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

