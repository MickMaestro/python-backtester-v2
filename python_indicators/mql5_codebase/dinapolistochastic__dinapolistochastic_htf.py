"""dinapolistochastic — converted from MQL5: MQL5 Indicators/DiNapoliStochastic_HTF/dinapolistochastic.mq5

Copyright: Copyright © 2010, LenIFCHIK; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, LenIFCHIK', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [36095], 2: [14822282]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Stochastic', 2: 'Signal'}, 'levels': [70.0, 50.0, 30.0], 'description': [], 'name': 'dinapolistochastic', 'source': 'MQL5 Indicators/DiNapoliStochastic_HTF/dinapolistochastic.mq5', 'folder': 'DiNapoliStochastic_HTF', 'inputs': [{'mql': 'FastK', 'py': 'FastK', 'param': 'FastK', 'type': 'uint', 'default': 8, 'label': 'Быстрый период %K', 'sinput': False}, {'mql': 'SlowK', 'py': 'SlowK', 'param': 'SlowK', 'type': 'uint', 'default': 3, 'label': 'Медленный период %K', 'sinput': False}, {'mql': 'SlowD', 'py': 'SlowD', 'param': 'SlowD', 'type': 'uint', 'default': 3, 'label': 'Медленный период %D', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastK = _input('FastK', 8)  # Быстрый период %K
SlowK = _input('SlowK', 3)  # Медленный период %K
SlowD = _input('SlowD', 3)  # Медленный период %D
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
StoBuffer = Arr(0, 0.0)
SigBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(FastK)
    SetIndexBuffer(0, StoBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(StoBuffer, True)
    SetIndexBuffer(1, SigBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SigBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'DiNapoliStochastic(', FastK, ', ', SlowK, ', ', SlowD, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    Range = 0.0
    Res = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        StoBuffer[limit + 1] = 50.0
        SigBuffer[limit + 1] = 50.0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, FastK)]
        LL = low[ArrayMinimum(low, bar, FastK)]
        Range = MathMax(HH - LL, 1 * Point())
        Res = _fdiv(100 * (close[bar] - LL), Range)
        StoBuffer[bar] = StoBuffer[bar + 1] + ((Res - StoBuffer[bar + 1]) / SlowK)
        SigBuffer[bar] = SigBuffer[bar + 1] + ((StoBuffer[bar] - SigBuffer[bar + 1]) / SlowD)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dinapolistochastic(_MQL5Indicator):
    name = 'dinapolistochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastK': 8,  # Быстрый период %K
        'SlowK': 3,  # Медленный период %K
        'SlowD': 3,  # Медленный период %D
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

