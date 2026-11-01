"""rchannel — converted from MQL5: MQL5 Indicators/RChannel/rchannel.mq5

Copyright: Copyright © 2005, Gosha Shmel; Link: http://www.system32.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Gosha Shmel', 'link': 'http://www.system32.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65280], 2: [16711680], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper RChannel', 2: 'Middle RChannel', 3: 'Lower RChannel'}, 'levels': [], 'description': [], 'name': 'rchannel', 'source': 'MQL5 Indicators/RChannel/rchannel.mq5', 'folder': 'RChannel', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper RChannel')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(1, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'Middle RChannel')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MiddleBuffer, True)
    SetIndexBuffer(2, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(2, PLOT_LABEL, 'Lower RChannel')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'RChannel(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_AverLine, _s_OnCalculate_HighLine, _s_OnCalculate_LowLine, _s_OnCalculate_ww
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_ww = False
        _s_OnCalculate_LowLine = 999999.0
        _s_OnCalculate_HighLine = 0.0
        _s_OnCalculate_AverLine = EMPTY_VALUE
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, 0 - 1, -1):
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        if (tm.hour == 23 and tm.min < 59) or ((tm.day_of_week == 5 and tm.hour == 22) and tm.min < 59):
            _s_OnCalculate_ww = False
        if ((tm.hour == 0 and tm.min >= 0) and tm.min <= 30) and (not _s_OnCalculate_ww):
            _s_OnCalculate_LowLine = low[bar]
            _s_OnCalculate_HighLine = high[bar]
            _s_OnCalculate_ww = True
        else:
            _s_OnCalculate_LowLine = MathMin(low[bar], _s_OnCalculate_LowLine)
            _s_OnCalculate_HighLine = MathMax(high[bar], _s_OnCalculate_HighLine)
        _s_OnCalculate_AverLine = _s_OnCalculate_LowLine + ((_s_OnCalculate_HighLine - _s_OnCalculate_LowLine) / 2)
        UpperBuffer[bar] = _s_OnCalculate_HighLine
        LowerBuffer[bar] = _s_OnCalculate_LowLine
        MiddleBuffer[bar] = _s_OnCalculate_AverLine
    Comment('High - ', _s_OnCalculate_HighLine, '; Low - ', _s_OnCalculate_LowLine, '; Average - ', _s_OnCalculate_AverLine, '; Channel width=', _int(_fdiv(_s_OnCalculate_HighLine - _s_OnCalculate_LowLine, Point())))
    return rates_total

# ---- static local variables
_s_OnCalculate_LowLine = 0.0
_s_OnCalculate_HighLine = 0.0
_s_OnCalculate_AverLine = 0.0
_s_OnCalculate_ww = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Rchannel(_MQL5Indicator):
    name = 'rchannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

