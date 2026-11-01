"""corr — converted from MQL5: MQL5 Indicators/Corr/corr.mq5

Copyright: Copyright © 2006, Nike; Link: http://www.mql4.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Nike', 'link': 'http://www.mql4.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Corr'}, 'levels': [], 'description': [], 'name': 'corr', 'source': 'MQL5 Indicators/Corr/corr.mq5', 'folder': 'Corr', 'inputs': [{'mql': 'CorrLen', 'py': 'CorrLen', 'param': 'CorrLen', 'type': 'uint', 'default': 7, 'label': 'период', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CorrLen = _input('CorrLen', 7)  # период
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(CorrLen)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'Corr(', CorrLen, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        IndBuffer[bar] = _fdiv(close[bar] - open[bar], Point())
        IndBuffer[bar] = corr(IndBuffer, bar, CorrLen)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def corr(a, index, len_):
    m1 = 0.0
    m2 = 0.0
    m1_2 = 0.0
    m2_2 = 0.0
    m12 = 0.0
    for i in range(0, len_):
        m1 += a[i]
        m2 += a[index - i]
        m1_2 += a[i] * a[i]
        m2_2 += a[index - i] * a[index - i]
        m12 += a[i] * a[index - i]
    m1 = _fdiv(m1, len_)
    m2 = _fdiv(m2, len_)
    m1_2 = _fdiv(m1_2, len_)
    m2_2 = _fdiv(m2_2, len_)
    m12 = _fdiv(m12, len_)
    res = (m1_2 - (m1 * m1)) * (m2_2 - (m2 * m2))
    if not res:
        return 0.0
    return _fdiv(m12 - (m1 * m2), MathSqrt(MathAbs(res)))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Corr(_MQL5Indicator):
    name = 'corr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CorrLen': 7,  # период
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

