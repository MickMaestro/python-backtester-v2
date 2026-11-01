"""colorline — converted from MQL5: MQL5 Indicators/ColorLine/colorline.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [255, 32768, 16711680]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ColorLine'}, 'levels': [], 'description': [], 'name': 'colorline', 'source': 'MQL5 Indicators/ColorLine/colorline.mq5', 'folder': 'ColorLine', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Green = 0x008000  # MQL4 colour name
LightGoldenrod = 0xD2FAFA  # MQL4 colour name
LightSlateGray = 0x998877  # MQL4 colour name
LimeGreen = 0x32CD32  # MQL4 colour name
Orchid = 0xD670DA  # MQL4 colour name
Pink = 0xCBC0FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name
Yellow = 0x00FFFF  # MQL4 colour name

# ---- inputs and global variables
ExtColorLineBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
ExtMAHandle = 0

def OnInit():
    global ExtMAHandle
    SetIndexBuffer(0, ExtColorLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    ExtMAHandle = iMA(Symbol(), 0, 10, 0, MODE_EMA, PRICE_CLOSE)

def getIndexOfColor(i):
    j = _imod(i, 300)
    if j < 100:
        return 0
    if j < 200:
        return 1
    return 2

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_modified, _s_OnCalculate_ticks
    limit = 0
    calculated = BarsCalculated(ExtMAHandle)
    if calculated < rates_total:
        Print('Not all data of ExtMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    if prev_calculated == 0:
        if False:
            return 0
        if CopyBuffer(ExtMAHandle, 0, 0, rates_total, ExtColorLineBuffer) <= 0:
            return 0
        for i in range(0, rates_total):
            ExtColorsBuffer[i] = getIndexOfColor(i)
    else:
        to_copy = 0
        if prev_calculated > rates_total or prev_calculated < 0:
            to_copy = rates_total
        else:
            to_copy = rates_total - prev_calculated
            if prev_calculated > 0:
                to_copy += 1
        if False:
            return 0
        copied = CopyBuffer(ExtMAHandle, 0, 0, rates_total, ExtColorLineBuffer)
        if copied <= 0:
            return 0
        _s_OnCalculate_ticks += 1
        if _s_OnCalculate_ticks >= 5:
            _s_OnCalculate_ticks = 0
            _s_OnCalculate_modified += 1
            if _s_OnCalculate_modified >= 3:
                _s_OnCalculate_modified = 0
            ResetLastError()
            _sw1 = _s_OnCalculate_modified
            if _sw1 == 0:
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Red)
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Blue)
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, Green)
            elif _sw1 == 1:
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, Yellow)
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Pink)
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, LightSlateGray)
            else:
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, LightGoldenrod)
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, Orchid)
                PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, LimeGreen)
        else:
            limit = prev_calculated - 1
            for i in range(limit, rates_total):
                ExtColorsBuffer[i] = getIndexOfColor(i)
    return rates_total

# ---- static local variables
_s_OnCalculate_ticks = 0
_s_OnCalculate_modified = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorline(_MQL5Indicator):
    name = 'colorline'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

