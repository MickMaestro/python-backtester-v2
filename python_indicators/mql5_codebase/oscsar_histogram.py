"""OscSAR_Histogram — converted from MQL5: MQL5 Indicators/OscSAR_Histogram/OscSAR_Histogram.mq5

Copyright: Copyright © 2010, LeMan; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, LeMan', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421376, 8421504, 16711935]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'OscSAR_Histogram'}, 'levels': [], 'description': [], 'name': 'OscSAR_Histogram', 'source': 'MQL5 Indicators/OscSAR_Histogram/OscSAR_Histogram.mq5', 'folder': 'OscSAR_Histogram', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.02, 'label': 'Шаг iSAR', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'Максимум iSAR', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Step = _input('Step', 0.02)  # Шаг iSAR
Maximum = _input('Maximum', 0.2)  # Максимум iSAR
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
SAR_Handle = 0
min_rates_total = 0

def OnInit():
    global SAR_Handle, min_rates_total
    min_rates_total = 2
    SAR_Handle = iSAR(None, 0, Step, Maximum)
    if SAR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора SAR')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'OscSAR_Histogram(', DoubleToString(Step, 3), ',', DoubleToString(Maximum, 3), ',', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(SAR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(SAR_Handle, 0, 0, to_copy, IndBuffer) <= 0:
        return 0
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = _fdiv(close[bar] - IndBuffer[bar], Point())
        clr = _int(1.0)
        if IndBuffer[bar] > 0:
            clr = _int(0.0)
        elif IndBuffer[bar] < 0:
            clr = _int(2.0)
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OscSARHistogram(_MQL5Indicator):
    name = 'OscSAR_Histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 0.02,  # Шаг iSAR
        'Maximum': 0.2,  # Максимум iSAR
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

