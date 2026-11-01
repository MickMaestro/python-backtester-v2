"""geo_innerbar — converted from MQL5: MQL5 Indicators/Geo_InnerBar/geo_innerbar.mq5

Copyright: Copyright © 2012, Geokom; Link: geokom2004@yandex.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Geokom', 'link': 'geokom2004@yandex.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_maximum': 1.1, 'indicator_minimum': 0.0}, 'types': {1: 3}, 'colors': {1: [5275647]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Geo_InnerBar'}, 'levels': [], 'description': [], 'name': 'geo_innerbar', 'source': 'MQL5 Indicators/Geo_InnerBar/geo_innerbar.mq5', 'folder': 'Geo_InnerBar', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Geo_InnerBar')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if high[bar] < high[bar + 1] and low[bar] > low[bar + 1]:
            ExtBuffer[bar] = 1.0
        else:
            ExtBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GeoInnerbar(_MQL5Indicator):
    name = 'geo_innerbar'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }
    y_range = (0.0, 1.1)

