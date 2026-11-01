"""geo_showopendaylevel — converted from MQL5: MQL5 Indicators/Geo_ShowOpenDayLevel/geo_showopendaylevel.mq5

Copyright: Copyright © 2012, Geokom; Link: geokom2004@yandex.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Geokom', 'link': 'geokom2004@yandex.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Geo_ShowOpenDayLevel'}, 'levels': [], 'description': [], 'name': 'geo_showopendaylevel', 'source': 'MQL5 Indicators/Geo_ShowOpenDayLevel/geo_showopendaylevel.mq5', 'folder': 'Geo_ShowOpenDayLevel', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 3
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 2)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Geo_ShowOpenDayLevel( Shift = ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or Period() > PERIOD_H12:
        return 0
    limit = 0
    bar = 0
    DOpen = Arr(1, 0.0, dyn=False)
    DTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        _s_OnCalculate_LastCountBar = bar
        IndBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), PERIOD_D1, _DT(time[bar]), 1, DTime) <= 0:
            return 0
        if time[bar] >= DTime[0] and time[bar + 1] < DTime[0]:
            if CopyOpen(Symbol(), PERIOD_D1, _DT(time[bar]), 1, DOpen) <= 0:
                return 0
            IndBuffer[bar] = DOpen[0]
        if IndBuffer[bar + 1] != EMPTY_VALUE and IndBuffer[bar] == EMPTY_VALUE:
            IndBuffer[bar] = IndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GeoShowopendaylevel(_MQL5Indicator):
    name = 'geo_showopendaylevel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

