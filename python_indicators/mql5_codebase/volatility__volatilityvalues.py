"""Volatility — converted from MQL5: MQL5 Indicators/VolatilityValues/Volatility.mq5

Copyright: Copyright © 2009, Trofimov Evgeniy Vitalyevich; Link: http://TrofimovVBA.narod.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Trofimov Evgeniy Vitalyevich', 'link': 'http://TrofimovVBA.narod.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Volatility'}, 'levels': [], 'description': [], 'name': 'Volatility', 'source': 'MQL5 Indicators/VolatilityValues/Volatility.mq5', 'folder': 'VolatilityValues', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'uint', 'default': 12, 'label': 'период канала', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
N = _input('N', 12)  # период канала
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(N)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = 'Volatility(' + _str(N) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        HH = high[ArrayMaximum(high, bar, N)]
        LL = low[ArrayMinimum(low, bar, N)]
        IndBuffer[bar] = _fdiv(HH - LL, Point() * N)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Volatility(_MQL5Indicator):
    name = 'Volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 12,  # период канала
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

