"""reversesymbol — converted from MQL5: MQL5 Indicators/ReverseSymbol/reversesymbol.mq5

Reverse Symbol
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {2: 17}, 'colors': {2: [32768, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {2: 'ReverseSymbol Open;ReverseSymbol High;ReverseSymbol Low;ReverseSymbol Close'}, 'levels': [], 'description': ['Reverse Symbol'], 'name': 'reversesymbol', 'source': 'MQL5 Indicators/ReverseSymbol/reversesymbol.mq5', 'folder': 'ReverseSymbol', 'inputs': [{'mql': 'BidColor', 'py': 'BidColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Bid line color', 'sinput': False}, {'mql': 'BidStyle', 'py': 'BidStyle', 'param': 'BidStyle', 'type': 'int', 'default': 0, 'label': 'Bid line style', 'sinput': False}, {'mql': 'IndicatorDigits', 'py': 'IndicatorDigits_v', 'param': 'IndicatorDigits_v', 'type': 'int', 'default': 3, 'label': 'Indicator display accuracy format', 'sinput': False}, {'mql': 'ratio', 'py': 'ratio', 'param': 'ratio', 'type': 'double', 'default': 1.0, 'label': 'Compensation factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
BidStyle = _input('BidStyle', STYLE_SOLID)  # Bid line style
IndicatorDigits_v = _input('IndicatorDigits_v', 3)  # Indicator display accuracy format
ratio = _input('ratio', 1.0)  # Compensation factor
ExtBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = 1
    SetIndexBuffer(1, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    IndicatorSetInteger(INDICATOR_DIGITS, IndicatorDigits_v)
    CrossIndex_ = ""
    Symb = Symbol()
    if StringLen(Symbol()) == 6:
        CrossIndex_ = StringSubstr(Symb, 3, 3) + StringSubstr(Symb, 0, 3)
    else:
        CrossIndex_ = Symb
    short_name = Box("")
    StringConcatenate(short_name, 'ReverseSymbol(', CrossIndex_, ',', StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1), 'x', ratio, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, short_name.v)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, BidColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, BidStyle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtOpenBuffer[bar] = _fdiv(ratio, open[bar])
        ExtCloseBuffer[bar] = _fdiv(ratio, close[bar])
        ExtHighBuffer[bar] = _fdiv(ratio, low[bar])
        ExtLowBuffer[bar] = _fdiv(ratio, high[bar])
        ExtBuffer[bar] = ExtCloseBuffer[bar]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtCloseBuffer[rates_total - 1])
    return rates_total

# ---- global variables initialised from expressions
BidColor = _input('BidColor', _uint(Red))  # Bid line color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Reversesymbol(_MQL5Indicator):
    name = 'reversesymbol'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BidStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Bid line style
        'IndicatorDigits_v': 3,  # Indicator display accuracy format
        'ratio': 1.0,  # Compensation factor
    }

