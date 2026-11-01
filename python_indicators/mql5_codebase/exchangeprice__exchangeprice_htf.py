"""ExchangePrice — converted from MQL5: MQL5 Indicators/ExchangePrice_HTF/ExchangePrice.mq5

ExchangePrice
Copyright: Copyright 2013, papaklass; Link: http://www.mql4.com/ru/users/papaklass; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, papaklass', 'link': 'http://www.mql4.com/ru/users/papaklass', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711680, 6053069]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ExchangePrice'}, 'levels': [], 'description': ['ExchangePrice'], 'name': 'ExchangePrice', 'source': 'MQL5 Indicators/ExchangePrice_HTF/ExchangePrice.mq5', 'folder': 'ExchangePrice_HTF', 'inputs': [{'mql': 'countBarsS', 'py': 'countBarsS', 'param': 'countBarsS', 'type': 'int', 'default': 96, 'label': '', 'sinput': False}, {'mql': 'countBarsL', 'py': 'countBarsL', 'param': 'countBarsL', 'type': 'int', 'default': 288, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
countBarsS = _input('countBarsS', 96)
countBarsL = _input('countBarsL', 288)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
Ind_Handle = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(countBarsS, countBarsL)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ExchangePrice')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    current = 0.0
    historyL = 0.0
    historyS = 0.0
    limit = 0
    bar = 0
    ArraySetAsSeries(price, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1 - begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        current = price[bar]
        historyS = price[bar + countBarsS]
        historyL = price[bar + countBarsL]
        UpBuffer[bar] = _fdiv(current - historyS, Point())
        DnBuffer[bar] = _fdiv(current - historyL, Point())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExchangePrice(_MQL5Indicator):
    name = 'ExchangePrice'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'countBarsS': 96,
        'countBarsL': 288,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

