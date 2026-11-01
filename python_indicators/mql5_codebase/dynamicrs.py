"""dynamicrs — converted from MQL5: MQL5 Indicators/DynamicRS/dynamicrs.mq5

A moving drawn without averaging
Copyright: Copyright © 2007, Nick A. Zhilin; Link: rebus58@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Nick A. Zhilin', 'link': 'rebus58@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'DynamicRS'}, 'levels': [], 'description': ['A moving drawn without averaging'], 'name': 'dynamicrs', 'source': 'MQL5 Indicators/DynamicRS/dynamicrs.mq5', 'folder': 'DynamicRS', 'inputs': [{'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 15, 'label': 'Width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Filter = _input('Filter', 15)  # Width
IndBuffer = Arr(0, 0.0)
dFilter = 0.0
min_rates_total = 0

def OnInit():
    global dFilter, min_rates_total
    min_rates_total = 2
    dFilter = Filter * Point()
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'DynamicRS(', Filter, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if high[bar] < high[bar + 1] and high[bar] < (IndBuffer[bar + 1] - dFilter):
            IndBuffer[bar] = high[bar]
        elif low[bar] > low[bar + 1] and low[bar] > (IndBuffer[bar + 1] + dFilter):
            IndBuffer[bar] = low[bar]
        else:
            IndBuffer[bar] = IndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dynamicrs(_MQL5Indicator):
    name = 'dynamicrs'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Filter': 15,  # Width
    }

