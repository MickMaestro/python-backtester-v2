"""i-onethird — converted from MQL5: MQL5 Indicators/i-OneThird/i-onethird.mq5

Bullish and bearish patterns in the style of HeikenAshi
Copyright: Copyright © 2007, RickD; Link: www.e2e-fx.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, RickD', 'link': 'www.e2e-fx.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [8421376, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'open;high;low;close'}, 'levels': [], 'description': ['Bullish and bearish patterns in the style of HeikenAshi'], 'name': 'i-onethird', 'source': 'MQL5 Indicators/i-OneThird/i-onethird.mq5', 'folder': 'i-OneThird', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 1
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'i-OneThird'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

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
        ExtLowBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtOpenBuffer[bar] = 0.0
        ExtCloseBuffer[bar] = 0.0
        third = (high[bar] - low[bar]) / 3
        if close[bar] > (high[bar] - third):
            ExtLowBuffer[bar] = low[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtOpenBuffer[bar] = MathMin(open[bar], close[bar])
            ExtCloseBuffer[bar] = MathMax(open[bar], close[bar])
        if close[bar] < (low[bar] + third):
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            ExtOpenBuffer[bar] = MathMax(open[bar], close[bar])
            ExtCloseBuffer[bar] = MathMin(open[bar], close[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IOnethird(_MQL5Indicator):
    name = 'i-onethird'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

