"""ichimoku — converted from MQL5: MQL5 Indicators/Ichimoku/ichimoku.mq5

Ichimoku Kinko Hyo
Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 7, 4: 1, 5: 11}, 'colors': {1: [255], 2: [16711680], 3: [15658671, 16118015], 4: [65280], 5: [255, 16711680]}, 'widths': {5: 1}, 'styles': {5: 4}, 'labels': {1: 'Tenkan-sen', 2: 'Kijun-sen', 3: 'Senkou Span A;Senkou Span B', 4: 'Chinkou Span', 5: 'Sen'}, 'levels': [], 'description': ['Ichimoku Kinko Hyo'], 'name': 'ichimoku', 'source': 'MQL5 Indicators/Ichimoku/ichimoku.mq5', 'folder': 'Ichimoku', 'inputs': [{'mql': 'InpTenkan', 'py': 'InpTenkan', 'param': 'InpTenkan', 'type': 'int', 'default': 9, 'label': 'Tenkan-sen', 'sinput': False}, {'mql': 'InpKijun', 'py': 'InpKijun', 'param': 'InpKijun', 'type': 'int', 'default': 26, 'label': 'Kijun-sen', 'sinput': False}, {'mql': 'InpSenkou', 'py': 'InpSenkou', 'param': 'InpSenkou', 'type': 'int', 'default': 52, 'label': 'Senkou Span B', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTenkan = _input('InpTenkan', 9)  # Tenkan-sen
InpKijun = _input('InpKijun', 26)  # Kijun-sen
InpSenkou = _input('InpSenkou', 52)  # Senkou Span B
ExtTenkanBuffer = Arr(0, 0.0)
ExtKijunBuffer = Arr(0, 0.0)
ExtSpanABuffer = Arr(0, 0.0)
ExtSpanBBuffer = Arr(0, 0.0)
ExtChinkouBuffer = Arr(0, 0.0)
ExtTenkanBuffer1 = Arr(0, 0.0)
ExtKijunBuffer1 = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtTenkanBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtKijunBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtSpanABuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtSpanBBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtChinkouBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtTenkanBuffer1, INDICATOR_DATA)
    SetIndexBuffer(6, ExtKijunBuffer1, INDICATOR_DATA)
    SetIndexBuffer(7, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtTenkanBuffer, True)
    ArraySetAsSeries(ExtKijunBuffer, True)
    ArraySetAsSeries(ExtSpanABuffer, True)
    ArraySetAsSeries(ExtSpanBBuffer, True)
    ArraySetAsSeries(ExtChinkouBuffer, True)
    ArraySetAsSeries(ExtTenkanBuffer1, True)
    ArraySetAsSeries(ExtKijunBuffer1, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpTenkan)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpKijun)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpSenkou - 1)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, InpTenkan)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, InpKijun)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, MathMax(InpTenkan, InpKijun))
    PlotIndexSetInteger(2, PLOT_SHIFT, InpKijun)
    PlotIndexSetInteger(3, PLOT_SHIFT, -InpKijun)
    PlotIndexSetString(0, PLOT_LABEL, 'Tenkan-sen(' + _str(InpTenkan) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Kijun-sen(' + _str(InpKijun) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Senkou Span A;Senkou Span B(' + _str(InpSenkou) + ')')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    limit = 0
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        ExtChinkouBuffer[i] = Close[i]
        high = High[ArrayMaximum(High, i, InpTenkan)]
        low = Low[ArrayMinimum(Low, i, InpTenkan)]
        ExtTenkanBuffer1[i] = (high + low) / 2.0
        ExtTenkanBuffer[i] = ExtTenkanBuffer1[i]
        high = High[ArrayMaximum(High, i, InpKijun)]
        low = Low[ArrayMinimum(Low, i, InpKijun)]
        ExtKijunBuffer1[i] = (high + low) / 2.0
        ExtKijunBuffer[i] = ExtKijunBuffer1[i]
        ExtSpanABuffer[i] = (ExtTenkanBuffer[i] + ExtKijunBuffer[i]) / 2.0
        high = High[ArrayMaximum(High, i, InpSenkou)]
        low = Low[ArrayMinimum(Low, i, InpSenkou)]
        ExtSpanBBuffer[i] = (high + low) / 2.0
        if ExtKijunBuffer[i] < ExtTenkanBuffer[i]:
            ExtColorBuffer[i] = 1.0
        else:
            ExtColorBuffer[i] = 0.0
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

