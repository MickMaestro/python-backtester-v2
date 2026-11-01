"""dynamicrs_channel — converted from MQL5: MQL5 Indicators/DynamicRS_Channel_HTF/dynamicrs_channel.mq5

Канал, построенный без усреднения
Copyright: Copyright © 2007, Nick A. Zhilin; Link: rebus58@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Nick A. Zhilin', 'link': 'rebus58@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [255], 3: [7451452]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'DynamicRS Middle', 2: 'DynamicRS Upper', 3: 'DynamicRS Lower'}, 'levels': [], 'description': ['Канал, построенный без усреднения'], 'name': 'dynamicrs_channel', 'source': 'MQL5 Indicators/DynamicRS_Channel_HTF/dynamicrs_channel.mq5', 'folder': 'DynamicRS_Channel_HTF', 'inputs': [{'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 150, 'label': 'Ширина', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Filter = _input('Filter', 150)  # Ширина
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
dFilter = 0.0
min_rates_total = 0

def OnInit():
    global dFilter, min_rates_total
    min_rates_total = 2
    dFilter = Filter * Point()
    SetIndexBuffer(0, MiddleBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HighestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(MiddleBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'DynamicRS_Channel(', Filter, ')')
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
        if high[bar] < high[bar + 1] and high[bar] < (MiddleBuffer[bar + 1] - dFilter):
            MiddleBuffer[bar] = high[bar]
        elif low[bar] > low[bar + 1] and low[bar] > (MiddleBuffer[bar + 1] + dFilter):
            MiddleBuffer[bar] = low[bar]
        else:
            MiddleBuffer[bar] = MiddleBuffer[bar + 1]
        HighestBuffer[bar] = MiddleBuffer[bar] + dFilter
        LowestBuffer[bar] = MiddleBuffer[bar] - dFilter
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicrsChannel(_MQL5Indicator):
    name = 'dynamicrs_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Filter': 150,  # Ширина
    }

