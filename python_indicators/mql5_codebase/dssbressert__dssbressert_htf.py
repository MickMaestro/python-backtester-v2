"""dssbressert — converted from MQL5: MQL5 Indicators/DSSBressert_HTF/dssbressert.mq5

Copyright: Copyright © 2008, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711680, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'DSS Bressert'}, 'levels': [80.0, 20.0], 'description': [], 'name': 'dssbressert', 'source': 'MQL5 Indicators/DSSBressert_HTF/dssbressert.mq5', 'folder': 'DSSBressert_HTF', 'inputs': [{'mql': 'EMA_period', 'py': 'EMA_period', 'param': 'EMA_period', 'type': 'uint', 'default': 8, 'label': 'Период EMA', 'sinput': False}, {'mql': 'Sto_period', 'py': 'Sto_period', 'param': 'Sto_period', 'type': 'uint', 'default': 13, 'label': 'Период стохастика', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
EMA_period = _input('EMA_period', 8)  # Период EMA
Sto_period = _input('Sto_period', 13)  # Период стохастика
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
DssBuffer = Arr(0, 0.0)
MitBuffer = Arr(0, 0.0)
smooth_coefficient = 0.0

def OnInit():
    global min_rates_total, smooth_coefficient
    min_rates_total = _int(Sto_period + 1)
    smooth_coefficient = _fdiv(2.0, 1.0 + EMA_period)
    SetIndexBuffer(0, DssBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DssBuffer, True)
    SetIndexBuffer(1, MitBuffer, INDICATOR_DATA)
    ArraySetAsSeries(MitBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'DSS Bressert(', EMA_period, ', ', Sto_period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    HighRange = 0.0
    LowRange = 0.0
    delta = 0.0
    MIT = 0.0
    DSS = 0.0
    limit = 0
    bar = 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        MitBuffer[limit + 1] = 50.0
        DssBuffer[limit + 1] = 50.0
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HighRange = high[ArrayMaximum(high, bar, Sto_period)]
        LowRange = low[ArrayMinimum(low, bar, Sto_period)]
        delta = close[bar] - LowRange
        MIT = _fdiv(delta, HighRange - LowRange) * 100.0
        MitBuffer[bar] = (smooth_coefficient * (MIT - MitBuffer[bar + 1])) + MitBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HighRange = MitBuffer[ArrayMaximum(MitBuffer, bar, Sto_period)]
        LowRange = MitBuffer[ArrayMinimum(MitBuffer, bar, Sto_period)]
        delta = MitBuffer[bar] - LowRange
        DSS = _fdiv(delta, HighRange - LowRange) * 100.0
        DssBuffer[bar] = (smooth_coefficient * (DSS - DssBuffer[bar + 1])) + DssBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dssbressert(_MQL5Indicator):
    name = 'dssbressert'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EMA_period': 8,  # Период EMA
        'Sto_period': 13,  # Период стохастика
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

