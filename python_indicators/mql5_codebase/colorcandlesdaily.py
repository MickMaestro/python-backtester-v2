"""colorcandlesdaily — converted from MQL5: MQL5 Indicators/ColorCandlesDaily/colorcandlesdaily.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'colorcandlesdaily', 'source': 'MQL5 Indicators/ColorCandlesDaily/colorcandlesdaily.mq5', 'folder': 'ColorCandlesDaily', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

BlueViolet = 0xE22B8A  # MQL4 colour name
DarkGoldenrod = 0x0B86B8  # MQL4 colour name
ForestGreen = 0x228B22  # MQL4 colour name
MediumSlateBlue = 0xEE687B  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

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
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 6)
    for i in range(1, 6):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, ExtColorOfDay[i])
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    printf('We have %u colors of days', PlotIndexGetInteger(0, PLOT_COLOR_INDEXES))

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    tstruct = MqlDateTime()
    if prev_calculated < 1:
        i = 0
    else:
        i = prev_calculated - 1
    while i < rates_total:
        ExtOpenBuffer[i] = open[i]
        ExtHighBuffer[i] = high[i]
        ExtLowBuffer[i] = low[i]
        ExtCloseBuffer[i] = close[i]
        TimeToStruct(time[i], tstruct)
        ExtColorsBuffer[i] = tstruct.day_of_week
        i += 1
    return rates_total

# ---- global variables initialised from expressions
ExtColorOfDay = Arr.of([CLR_NONE, _uint(MediumSlateBlue), _uint(DarkGoldenrod), _uint(ForestGreen), _uint(BlueViolet), _uint(Red)], fill=0, dyn=False, size=6)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorcandlesdaily(_MQL5Indicator):
    name = 'colorcandlesdaily'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

