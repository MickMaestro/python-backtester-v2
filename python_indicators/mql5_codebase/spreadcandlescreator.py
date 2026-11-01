"""spreadcandlescreator — converted from MQL5: MQL5 Indicators/SpreadCandlesCreator/spreadcandlescreator.mq5

Spread Candles Creator
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2, 'indicator_minimum': 0.0}, 'types': {1: 1, 2: 17}, 'colors': {1: [16711680], 2: [255, 65280]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Spread Line', 2: 'SpreadOpen; SpreadHigh; SpreadLow; SpreadClose'}, 'levels': [], 'description': ['Spread Candles Creator'], 'name': 'spreadcandlescreator', 'source': 'MQL5 Indicators/SpreadCandlesCreator/spreadcandlescreator.mq5', 'folder': 'SpreadCandlesCreator', 'inputs': [{'mql': 'BidColor', 'py': 'BidColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Last spread line color', 'sinput': False}, {'mql': 'BidStyle', 'py': 'BidStyle', 'param': 'BidStyle', 'type': 'int', 'default': 0, 'label': 'Last spread line style', 'sinput': False}, {'mql': 'Recount', 'py': 'Recount', 'param': 'Recount', 'type': 'bool', 'default': True, 'label': 'History deletion flag', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Gray = 0x808080  # MQL4 colour name

# ---- inputs and global variables
BidStyle = _input('BidStyle', STYLE_SOLID)  # Last spread line style
Recount = _input('Recount', True)  # History deletion flag
ExtBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
prev_calculated_old = 0
lastbar = -1
spread_high = 0
spread_low = 0
StartBars = 0

def OnInit():
    global StartBars
    StartBars = 1
    SetIndexBuffer(1, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Spread Candles Creator(' + _str(Recount) + ')')
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, BidColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, BidStyle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lastbar, prev_calculated_old, spread_high, spread_low
    if rates_total < StartBars:
        return 0
    first = 0
    bar = 0
    prev_calculated_ = 0
    spread0 = 0
    if Recount:
        prev_calculated_ = prev_calculated
    else:
        prev_calculated_ = prev_calculated_old
    if prev_calculated_ > rates_total or prev_calculated_ <= 0:
        first = 1
    else:
        first = prev_calculated_ - 1
    bar = first
    for bar in range(bar, rates_total):
        if spread[bar]:
            spread0 = spread[bar]
        else:
            spread0 = spread[bar - 1]
        if lastbar != bar:
            ExtOpenBuffer[bar] = spread0
            spread_high = spread0
            spread_low = spread0
        else:
            spread_high = MathMax(spread_high, spread0)
            spread_low = MathMin(spread_low, spread0)
        ExtCloseBuffer[bar] = spread0
        ExtHighBuffer[bar] = spread_high
        ExtLowBuffer[bar] = spread_low
        ExtBuffer[bar] = spread0
        lastbar = bar
        if ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    prev_calculated_old = rates_total
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtCloseBuffer[rates_total - 1])
    return rates_total

# ---- global variables initialised from expressions
BidColor = _input('BidColor', _uint(Gray))  # Last spread line color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Spreadcandlescreator(_MQL5Indicator):
    name = 'spreadcandlescreator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BidStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Last spread line style
        'Recount': True,  # History deletion flag
    }

