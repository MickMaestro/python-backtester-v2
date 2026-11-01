"""garch — converted from MQL5: MQL5 Indicators/GARCH/garch.mq5

Это индикатор фрактальной волатильности на базе модели GARCH Тима Боллерслева
Copyright: Copyright © 2012, Andres Barale Sarti; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Andres Barale Sarti', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'GARCH'}, 'levels': [], 'description': ['Это индикатор фрактальной волатильности на базе модели GARCH Тима Боллерслева'], 'name': 'garch', 'source': 'MQL5 Indicators/GARCH/garch.mq5', 'folder': 'GARCH', 'inputs': [{'mql': 'e_alpha', 'py': 'e_alpha', 'param': 'e_alpha', 'type': 'double', 'default': 0.01, 'label': '', 'sinput': False}, {'mql': 'e_beta', 'py': 'e_beta', 'param': 'e_beta', 'type': 'double', 'default': 0.08, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
e_alpha = _input('e_alpha', 0.01)
e_beta = _input('e_beta', 0.08)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
GarchNumVar = 0.0
min_rates_total = 0

def OnInit():
    global GarchNumVar, min_rates_total
    min_rates_total = 2
    GarchNumVar = 1e-06
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'GARCH')
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global GarchNumVar, _s_OnCalculate_GarchNumVar_
    if rates_total < (min_rates_total + begin):
        return 0
    limit = 0
    bar = 0
    GarchNum = 0.0
    residual = 0.0
    residualSq = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - begin
        _s_OnCalculate_GarchNumVar_ = 0.0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(price, True)
    GarchNumVar = _s_OnCalculate_GarchNumVar_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        residual = price[bar] - price[bar + 1]
        residualSq = MathPow(residual, 2.0)
        GarchNumVar = (e_alpha * residualSq) + (e_beta * GarchNumVar)
        GarchNum = MathSqrt(GarchNumVar)
        IndBuffer[bar] = GarchNum
        if bar:
            _s_OnCalculate_GarchNumVar_ = GarchNumVar
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_GarchNumVar_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Garch(_MQL5Indicator):
    name = 'garch'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'e_alpha': 0.01,
        'e_beta': 0.08,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

