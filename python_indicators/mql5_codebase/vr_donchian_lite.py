"""VR Donchian Lite — converted from MQL5: MQL5 Indicators/VR Donchian Lite MT5/VR Donchian Lite.mq5

A simple standard Donchian indicator
Copyright: Copyright 2018, Trading-go Project.; Link: http://trading-go.ru; Version: 18.100

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Trading-go Project.', 'link': 'http://trading-go.ru', 'version': '18.100', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['A simple standard Donchian indicator'], 'name': 'VR Donchian Lite', 'source': 'MQL5 Indicators/VR Donchian Lite MT5/VR Donchian Lite.mq5', 'folder': 'VR Donchian Lite MT5', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'int', 'default': 24, 'label': 'Period Donchian', 'sinput': False}, {'mql': 'UpperLine', 'py': 'UpperLine', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Color Upper Line', 'sinput': False}, {'mql': 'LowerLine', 'py': 'LowerLine', 'param': None, 'type': 'color', 'default': 255, 'label': 'Color Lower Line', 'sinput': False}, {'mql': 'AverageLine', 'py': 'AverageLine', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Color Average Line', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_ = _input('Period_', 24)  # Period Donchian
UpperLine = _input('UpperLine', clrBlue)  # Color Upper Line
LowerLine = _input('LowerLine', clrRed)  # Color Lower Line
AverageLine = _input('AverageLine', clrGreen)  # Color Average Line
upper_line = Arr(0, 0.0)
lower_line = Arr(0, 0.0)
awera_line = Arr(0, 0.0)

def OnInit():
    Comment('')
    IndicatorSetString(INDICATOR_SHORTNAME, 'VR Donchian Lite(' + _str(Period_) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, upper_line, INDICATOR_DATA)
    ArraySetAsSeries(upper_line, True)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, UpperLine)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper Line')
    SetIndexBuffer(1, lower_line, INDICATOR_DATA)
    ArraySetAsSeries(lower_line, True)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(1, PLOT_LINE_STYLE, STYLE_SOLID)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, LowerLine)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 2)
    PlotIndexSetString(1, PLOT_LABEL, 'Lower Line')
    SetIndexBuffer(2, awera_line, INDICATOR_DATA)
    ArraySetAsSeries(awera_line, True)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(2, PLOT_LINE_STYLE, STYLE_DOT)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, AverageLine)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, 1)
    PlotIndexSetString(2, PLOT_LABEL, 'Average Line')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total <= Period_ or Period_ <= 0:
        return 0
    limit = rates_total - prev_calculated - 1
    if limit < 0:
        limit = 0
    for i in range(limit, 0 - 1, -1):
        upper_line[i] = high[iHighest(Symbol(), PERIOD_CURRENT, MODE_HIGH, Period_, i)]
        lower_line[i] = low[iLowest(Symbol(), PERIOD_CURRENT, MODE_LOW, Period_, i)]
        awera_line[i] = (upper_line[i] + lower_line[i]) / 2
    return rates_total

def OnDeinit(reason):
    pass


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VRDonchianLite(_MQL5Indicator):
    name = 'VR Donchian Lite'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 24,  # Period Donchian
    }

