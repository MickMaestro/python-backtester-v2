"""modified_optimum_elliptic_filter — converted from MQL5: MQL5 Indicators/Modified_Optimum_Elliptic_Filter_HTF/modified_optimum_elliptic_filter.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Modified Optimum Elliptic Filter'}, 'levels': [], 'description': [], 'name': 'modified_optimum_elliptic_filter', 'source': 'MQL5 Indicators/Modified_Optimum_Elliptic_Filter_HTF/modified_optimum_elliptic_filter.mq5', 'folder': 'Modified_Optimum_Elliptic_Filter_HTF', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг мувинга по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # сдвиг мувинга по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
min_rates_total = 0
coef1 = 0.0
coef2 = 0.0
coef3 = 0.0
coef4 = 0.0

def Get_Price(High, Low, bar):
    return (High[bar] + Low[bar]) / 2

def OnInit():
    global min_rates_total
    min_rates_total = 4
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'Modified Optimum Elliptic Filter(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if bar > min_rates_total:
            ExtLineBuffer[bar] = (0.13785 * ((2 * Get_Price(high, low, bar)) - Get_Price(high, low, bar - 1))) + (0.0007 * ((2 * Get_Price(high, low, bar - 1)) - Get_Price(high, low, bar - 2))) + (0.13785 * ((2 * Get_Price(high, low, bar - 2)) - Get_Price(high, low, bar - 3))) + (1.2103 * ExtLineBuffer[bar - 1]) - (0.4867 * ExtLineBuffer[bar - 2])
        else:
            ExtLineBuffer[bar] = Get_Price(high, low, bar)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ModifiedOptimumEllipticFilter(_MQL5Indicator):
    name = 'modified_optimum_elliptic_filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # сдвиг мувинга по горизонтали в барах
    }

