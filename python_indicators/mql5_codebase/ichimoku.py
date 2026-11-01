"""ichimoku — converted from MQL5: MQL5 Indicators/Ichimoku Kinko Hyo/ichimoku.mq5

Ichimoku Kinko Hyo
Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 7, 4: 1}, 'colors': {1: [255], 2: [16711680], 3: [6333684, 14204888], 4: [65280]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Tenkan-sen', 2: 'Kijun-sen', 3: 'Senkou Span A;Senkou Span B', 4: 'Chikou Span'}, 'levels': [], 'description': ['Ichimoku Kinko Hyo'], 'name': 'ichimoku', 'source': 'MQL5 Indicators/Ichimoku Kinko Hyo/ichimoku.mq5', 'folder': 'Ichimoku Kinko Hyo', 'inputs': [{'mql': 'InpTenkan', 'py': 'InpTenkan', 'param': 'InpTenkan', 'type': 'int', 'default': 9, 'label': 'Tenkan-sen', 'sinput': False}, {'mql': 'InpKijun', 'py': 'InpKijun', 'param': 'InpKijun', 'type': 'int', 'default': 26, 'label': 'Kijun-sen', 'sinput': False}, {'mql': 'InpSenkou', 'py': 'InpSenkou', 'param': 'InpSenkou', 'type': 'int', 'default': 52, 'label': 'Senkou Span B', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTenkan = _input('InpTenkan', 9)  # Tenkan-sen
InpKijun = _input('InpKijun', 26)  # Kijun-sen
InpSenkou = _input('InpSenkou', 52)  # Senkou Span B
ExtTenkanBuffer = Arr(0, 0.0)
ExtKijunBuffer = Arr(0, 0.0)
ExtSpanABuffer = Arr(0, 0.0)
ExtSpanBBuffer = Arr(0, 0.0)
ExtChikouBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtTenkanBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtKijunBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtSpanABuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtSpanBBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtChikouBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpTenkan)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpKijun)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpSenkou - 1)
    PlotIndexSetInteger(2, PLOT_SHIFT, InpKijun)
    PlotIndexSetInteger(3, PLOT_SHIFT, -InpKijun)
    PlotIndexSetString(0, PLOT_LABEL, 'Tenkan-sen(' + _str(InpTenkan) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Kijun-sen(' + _str(InpKijun) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Senkou Span A;Senkou Span B(' + _str(InpSenkou) + ')')

def Highest(array, range_, fromIndex):
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res < array[i]:
            res = array[i]
        i -= 1
    return res

def Lowest(array, range_, fromIndex):
    res = 0.0
    res = array[fromIndex]
    i = fromIndex
    while i > (fromIndex - range_) and i >= 0:
        if res > array[i]:
            res = array[i]
        i -= 1
    return res

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        ExtChikouBuffer[i] = Close[i]
        high = Highest(High, InpTenkan, i)
        low = Lowest(Low, InpTenkan, i)
        ExtTenkanBuffer[i] = (high + low) / 2.0
        high = Highest(High, InpKijun, i)
        low = Lowest(Low, InpKijun, i)
        ExtKijunBuffer[i] = (high + low) / 2.0
        ExtSpanABuffer[i] = (ExtTenkanBuffer[i] + ExtKijunBuffer[i]) / 2.0
        high = Highest(High, InpSenkou, i)
        low = Lowest(Low, InpSenkou, i)
        ExtSpanBBuffer[i] = (high + low) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ichimoku(_MQL5Indicator):
    name = 'ichimoku'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpTenkan': 9,  # Tenkan-sen
        'InpKijun': 26,  # Kijun-sen
        'InpSenkou': 52,  # Senkou Span B
    }

