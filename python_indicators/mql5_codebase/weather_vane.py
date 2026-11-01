"""weather_vane — converted from MQL5: MQL5 Indicators/Weather Vane/weather_vane.mq5

Copyright: Copyright 2012, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Section'}, 'levels': [], 'description': [], 'name': 'weather_vane', 'source': 'MQL5 Indicators/Weather Vane/weather_vane.mq5', 'folder': 'Weather Vane', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LineBuffer = Arr(0, 0.0)
VALUE = 0.0
SUMM = 0.0

def OnInit():
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global SUMM, VALUE, _s_OnCalculate_ticks
    timeInfo = SymbolInfoInteger(Symbol(), SYMBOL_TIME)
    str_ = MqlDateTime()
    TimeToStruct(timeInfo, str_)
    time_min = str_.min
    if not GlobalVariableCheck('min'):
        GlobalVariableTemp('min')
        GlobalVariableSet('min', time_min)
    if time_min != GlobalVariableGet('min'):
        GlobalVariableSet('min', time_min)
        _s_OnCalculate_ticks = 1
        VALUE = SymbolInfoDouble(Symbol(), SYMBOL_BID)
        SUMM = VALUE
    else:
        _s_OnCalculate_ticks += 1
        VALUE += SymbolInfoDouble(Symbol(), SYMBOL_BID)
        SUMM = NormalizeDouble(_fdiv(VALUE, _s_OnCalculate_ticks), 8)
    LineBuffer[rates_total - 1] = SUMM
    if ((high[rates_total - 1] + low[rates_total - 1]) / 2) < SUMM:
        Wingdings(time[rates_total - 1], high[rates_total - 1] + (2 * Point()), 241, clrBlue)
    else:
        Wingdings(time[rates_total - 1], low[rates_total - 1] - (2 * Point()), 242, clrRed)
    Comment(Symbol(), '\n', TimeToString(timeInfo), ' - ', _s_OnCalculate_ticks)
    return rates_total

def Wingdings(time, last, wings, colr):
    ObjectCreate(0, 'arrow', OBJ_ARROW, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, 'arrow', OBJPROP_ARROWCODE, wings)
    ObjectSetInteger(0, 'arrow', OBJPROP_COLOR, colr)
    ObjectSetInteger(0, 'arrow', OBJPROP_TIME, time)
    ObjectSetDouble(0, 'arrow', OBJPROP_PRICE, last)

# ---- static local variables
_s_OnCalculate_ticks = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WeatherVane(_MQL5Indicator):
    name = 'weather_vane'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

