"""BS_Living_Now — converted from MQL5: MQL5 Indicators/BS_Living_Now/BS_Living_Now.mq5

Copyright: Copyright © 2013, Backspace; Link: Success Version; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Backspace', 'link': 'Success Version', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [65280], 2: [255], 3: [16711680], 4: [16711935]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {}, 'labels': {1: 'BS_Living_Now ExtrimHi', 2: 'BS_Living_Now ExtrimLo', 3: 'Buy BS_Living_Now BreakHi', 4: 'Sell BS_Living_Now BreakLo'}, 'levels': [], 'description': [], 'name': 'BS_Living_Now', 'source': 'MQL5 Indicators/BS_Living_Now/BS_Living_Now.mq5', 'folder': 'BS_Living_Now', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 10)  # Период индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtrimHi = Arr(0, 0.0)
ExtrimLo = Arr(0, 0.0)
BreakHi = Arr(0, 0.0)
BreakLo = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(iPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'BS_Living_Now(', _str(iPeriod), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, ExtrimHi, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(ExtrimHi, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 217)
    SetIndexBuffer(1, ExtrimLo, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(ExtrimLo, True)
    PlotIndexSetInteger(1, PLOT_ARROW, 218)
    SetIndexBuffer(2, BreakHi, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BreakHi, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 177)
    SetIndexBuffer(3, BreakLo, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BreakLo, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(3, PLOT_ARROW, 177)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    limit = 0
    bar = 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtrimHi[bar] = 0.0
        ExtrimLo[bar] = 0.0
        BreakHi[bar] = 0.0
        BreakLo[bar] = 0.0
        if not bar:
            break
        HH = high[ArrayMaximum(high, bar + 1, iPeriod)]
        LL = low[ArrayMinimum(low, bar + 1, iPeriod)]
        if high[bar] > HH and high[bar] > high[bar - 1]:
            AvgRange = 0.0
            for iii in range(0, _int(iPeriod)):
                AvgRange += MathAbs(high[bar + iii] - low[bar + iii])
            AvgRange = AvgRange / iPeriod
            ExtrimHi[bar] = high[bar] + (0.3 * AvgRange)
            for iii in range(_int(iPeriod), 0, -1):
                if high[bar + iii] < high[ArrayMaximum(high, bar + iii + 1, iPeriod)]:
                    BreakHi[bar] = low[ArrayMinimum(low, bar + iii + 1, iPeriod)]
        if low[bar] < LL and low[bar] < low[bar - 1]:
            AvgRange = 0.0
            for iii in range(0, _int(iPeriod)):
                AvgRange += MathAbs(high[bar + iii] - low[bar + iii])
            AvgRange = AvgRange / iPeriod
            ExtrimLo[bar] = low[bar] - (0.3 * AvgRange)
            for iii in range(_int(iPeriod), 0, -1):
                if low[bar + iii] > low[ArrayMinimum(low, bar + iii + 1, iPeriod)]:
                    BreakLo[bar] = high[ArrayMaximum(high, bar + iii + 1, iPeriod)]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BSLivingNow(_MQL5Indicator):
    name = 'BS_Living_Now'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 10,  # Период индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

