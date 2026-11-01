"""dailyrangeprojections_full — converted from MQL5: MQL5 Indicators/Daily Range Projections Full/dailyrangeprojections_full.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [65280], 2: [13382297], 3: [255]}, 'widths': {1: 3, 2: 1, 3: 3}, 'styles': {}, 'labels': {1: "Tomorrow's anticipated high price", 2: "Tomorrow's anticipated average price", 3: "Tomorrow's anticipated low price"}, 'levels': [], 'description': [], 'name': 'dailyrangeprojections_full', 'source': 'MQL5 Indicators/Daily Range Projections Full/dailyrangeprojections_full.mq5', 'folder': 'Daily Range Projections Full', 'inputs': [{'mql': 'Symbol_MAX', 'py': 'Symbol_MAX', 'param': 'Symbol_MAX', 'type': 'int', 'default': 119, 'label': 'High price label for tomorrow', 'sinput': False}, {'mql': 'Symbol_MID', 'py': 'Symbol_MID', 'param': 'Symbol_MID', 'type': 'int', 'default': 167, 'label': 'Average price label for tomorrow', 'sinput': False}, {'mql': 'Symbol_MIN', 'py': 'Symbol_MIN', 'param': 'Symbol_MIN', 'type': 'int', 'default': 119, 'label': 'Low price label for tomorrow', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Symbol_MAX = _input('Symbol_MAX', 119)  # High price label for tomorrow
Symbol_MID = _input('Symbol_MID', 167)  # Average price label for tomorrow
Symbol_MIN = _input('Symbol_MIN', 119)  # Low price label for tomorrow
ExtMaxBuffer = Arr(0, 0.0)
ExtMinBuffer = Arr(0, 0.0)
ExtMidBuffer = Arr(0, 0.0)

def CreateHline(chart_id, name, nwin, price, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)

def OnInit():
    SetIndexBuffer(0, ExtMaxBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMidBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMinBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, Symbol_MAX)
    PlotIndexSetInteger(1, PLOT_ARROW, Symbol_MID)
    PlotIndexSetInteger(2, PLOT_ARROW, Symbol_MIN)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ExtMaxBuffer, True)
    ArraySetAsSeries(ExtMidBuffer, True)
    ArraySetAsSeries(ExtMinBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Daily Range Projections')

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() >= PERIOD_D1 or rates_total < 1:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        X = 0.0
        rates = Arr(2, 0, dyn=False, factory=MqlRates)
        if CopyRates(Symbol(), PERIOD_D1, _DT(time[bar]), 2, rates) <= 0:
            return 0
        if rates[1].close < rates[1].open:
            X = (rates[0].high + rates[0].low + rates[0].close + rates[0].low) / 2.0
        if rates[1].close > rates[1].open:
            X = (rates[0].high + rates[0].low + rates[0].close + rates[0].high) / 2.0
        if rates[1].close == rates[1].open:
            X = (rates[0].high + rates[0].low + rates[0].close + rates[0].close) / 2.0
        ExtMaxBuffer[bar] = NormalizeDouble(X - rates[0].low, Digits())
        ExtMinBuffer[bar] = NormalizeDouble(X - rates[0].high, Digits())
        ExtMidBuffer[bar] = NormalizeDouble((ExtMaxBuffer[bar] + ExtMinBuffer[bar]) / 2.0, Digits())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyrangeprojectionsFull(_MQL5Indicator):
    name = 'dailyrangeprojections_full'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Symbol_MAX': 119,  # High price label for tomorrow
        'Symbol_MID': 167,  # Average price label for tomorrow
        'Symbol_MIN': 119,  # Low price label for tomorrow
    }

