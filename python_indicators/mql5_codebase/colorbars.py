"""colorbars — converted from MQL5: MQL5 Indicators/ColorBars/colorbars.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 16}, 'colors': {1: [32768, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'colorbars', 'source': 'MQL5 Indicators/ColorBars/colorbars.mq5', 'folder': 'ColorBars', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    vol_up = True
    if i < prev_calculated:
        i = prev_calculated - 1
    while i < rates_total:
        ExtOpenBuffer[i] = open[i]
        ExtHighBuffer[i] = high[i]
        ExtLowBuffer[i] = low[i]
        ExtCloseBuffer[i] = close[i]
        if i > 0:
            if tick_volume[i] > tick_volume[i - 1]:
                vol_up = True
            if tick_volume[i] < tick_volume[i - 1]:
                vol_up = False
        if vol_up:
            ExtColorsBuffer[i] = 0.0
        else:
            ExtColorsBuffer[i] = 1.0
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorbars(_MQL5Indicator):
    name = 'colorbars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

