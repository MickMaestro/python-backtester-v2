"""AroonHorn — converted from MQL5: MQL5 Indicators/AroonHorn/AroonHorn.mq5

Copyright: Copyright © 2011, tonyc2a; Link: mailto:tonyc2a@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, tonyc2a', 'link': 'mailto:tonyc2a@yahoo.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 7}, 'colors': {1: [3329330], 2: [3937500], 3: [10025880, 12695295]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'BullsAroon', 2: 'BearsAroon', 3: 'Signal Aroon Cloud'}, 'levels': [70.0, 50.0, 30.0], 'description': [], 'name': 'AroonHorn', 'source': 'MQL5 Indicators/AroonHorn/AroonHorn.mq5', 'folder': 'AroonHorn', 'inputs': [{'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 9, 'label': 'период индикатора', 'sinput': False}, {'mql': 'AroonShift', 'py': 'AroonShift', 'param': 'AroonShift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AroonPeriod = _input('AroonPeriod', 9)  # период индикатора
AroonShift = _input('AroonShift', 0)  # сдвиг индикатора по горизонтали в барах
BullsAroonBuffer1 = Arr(0, 0.0)
BearsAroonBuffer1 = Arr(0, 0.0)
BullsAroonBuffer2 = Arr(0, 0.0)
BearsAroonBuffer2 = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BullsAroonBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, AroonPeriod)
    SetIndexBuffer(1, BearsAroonBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, AroonPeriod)
    SetIndexBuffer(2, BullsAroonBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, BearsAroonBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, AroonShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, AroonPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'Aroon(', AroonPeriod, ', ', AroonShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (AroonPeriod - 1):
        return 0
    first = 0
    bar = 0
    BULLS = 0.0
    BEARS = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = AroonPeriod - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        barx = rates_total - bar - 1
        BULLS = NormalizeDouble(100 - (((ArrayMaximum(high, barx, AroonPeriod) - barx + 0.5) * 100) / AroonPeriod), 0)
        BEARS = NormalizeDouble(100 - (((ArrayMinimum(low, barx, AroonPeriod) - barx + 0.5) * 100) / AroonPeriod), 0)
        BullsAroonBuffer1[bar] = BULLS
        BearsAroonBuffer1[bar] = BEARS
        BullsAroonBuffer2[bar] = 0.0
        BearsAroonBuffer2[bar] = 0.0
        if BULLS != BEARS:
            if BULLS > BEARS and BULLS >= 50:
                BullsAroonBuffer2[bar] = BULLS
                BearsAroonBuffer2[bar] = BEARS
            if BULLS < BEARS and BEARS >= 50:
                BullsAroonBuffer2[bar] = BULLS
                BearsAroonBuffer2[bar] = BEARS
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonHorn(_MQL5Indicator):
    name = 'AroonHorn'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AroonPeriod': 9,  # период индикатора
        'AroonShift': 0,  # сдвиг индикатора по горизонтали в барах
    }

