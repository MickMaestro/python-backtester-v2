"""Wiseman1 — converted from MQL5: MQL5 Indicators/Wiseman1/Wiseman1.mq5

Copyright: Copyright © 2005, Pavel Kulko; Link: polk@alba.dp.ua; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Pavel Kulko', 'link': 'polk@alba.dp.ua', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [65280, 32768, 2763429, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Wiseman1_Open;Wiseman1_High;Wiseman1_Low;Wiseman1_Close'}, 'levels': [], 'description': [], 'name': 'Wiseman1', 'source': 'MQL5 Indicators/Wiseman1/Wiseman1.mq5', 'folder': 'Wiseman1', 'inputs': [{'mql': 'iperiod', 'py': 'iperiod', 'param': 'iperiod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iperiod = _input('iperiod', 5)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 1 + _int(iperiod)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Wiseman1'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    for bar in range(limit, 0 - 1, -1):
        ExtCloseBuffer[bar] = 0.0
        ExtHighBuffer[bar] = ExtCloseBuffer[bar]
        ExtLowBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtLowBuffer[bar]
        ExtColorBuffer[bar] = 4.0
        median = (high[bar] + low[bar]) / 2
        HH = high[ArrayMaximum(high, bar + 1, iperiod)]
        LL = low[ArrayMinimum(low, bar + 1, iperiod)]
        if low[bar] < LL and close[bar] > median:
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            ExtCloseBuffer[bar] = close[bar]
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if high[bar] > HH and close[bar] < median:
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            ExtCloseBuffer[bar] = close[bar]
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wiseman1(_MQL5Indicator):
    name = 'Wiseman1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iperiod': 5,
    }

