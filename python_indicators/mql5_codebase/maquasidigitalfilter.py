"""maquasidigitalfilter — converted from MQL5: MQL5 Indicators/The Moving Average Indicator, based on the Quasi-Digital Filter/maquasidigitalfilter.mq5

Moving Average - Quasi-Digital Filter
Copyright: 2010, Vlad; Link: http://www.becemal.ru/mql

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, Vlad', 'link': 'http://www.becemal.ru/mql', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [55295]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'QDF'}, 'levels': [], 'description': ['Moving Average - Quasi-Digital Filter'], 'name': 'maquasidigitalfilter', 'source': 'MQL5 Indicators/The Moving Average Indicator, based on the Quasi-Digital Filter/maquasidigitalfilter.mq5', 'folder': 'The Moving Average Indicator, based on the Quasi-Digital Filter', 'inputs': [{'mql': 'PeriodMA', 'py': 'PeriodMA', 'param': 'PeriodMA', 'type': 'int', 'default': 31, 'label': 'Period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': "Indicator's Shift", 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodMA = _input('PeriodMA', 31)  # Period
Shift = _input('Shift', 0)  # Indicator's Shift
QDFBuffer = Arr(0, 0.0)
Multiplier = Arr(0, 0.0)

def OnInit():
    i = 0
    SetIndexBuffer(0, QDFBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (2 * PeriodMA) - 2)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'QDF(' + _str(PeriodMA) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'QDF(' + _str(PeriodMA) + ')')
    ArrayResize(Multiplier, PeriodMA, 256)
    ArrayInitialize(Multiplier, 0.0)
    i = 0
    for i in range(i, PeriodMA):
        Multiplier[i] = MathExp(((-2.0 * M_PI * i * i) / PeriodMA) / PeriodMA)
    else:
        i = _range_end(i, PeriodMA, 1)
    SM = 0.0
    i = 0
    for i in range(i, PeriodMA):
        SM += Multiplier[i]
    else:
        i = _range_end(i, PeriodMA, 1)
    i = 0
    for i in range(i, PeriodMA):
        Multiplier[i] = _fdiv(Multiplier[i], SM)
    else:
        i = _range_end(i, PeriodMA, 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < PeriodMA:
        return 0
    limit = prev_calculated - 1
    if limit < PeriodMA:
        limit = PeriodMA
    i = limit
    while i < rates_total:
        S = 0.0
        for j in range(0, PeriodMA):
            S += price[i - j] * Multiplier[j]
        QDFBuffer[i] = S
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Maquasidigitalfilter(_MQL5Indicator):
    name = 'maquasidigitalfilter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodMA': 31,  # Period
        'Shift': 0,  # Indicator's Shift
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

