"""wd.Multi_LineMA — converted from MQL5: MQL5 Indicators/wd.Multi_LineMA/wd.Multi_LineMA.mq5

Provides valuable insights into Moving Average values from a higher timeframe.
It features visual elements for streamlines analysis, including customizable trails and a dynamic MA horizontal price line.
The Multi-Timeframe Moving Average adapts to different timeframes, displaying values from higher timeframes if applicable.
A customizable Moving Average trail simplifies historical analysis.
The real-time dynamic MA Horizontal Price Line facilitating effective support and resistance identification.
Copyright: Copyright © 2023, Karya Prima Rajasa Mediavestama.; Link: https://www.mql5.com/en/code/47513; Version: 2.23

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2023, Karya Prima Rajasa Mediavestama.', 'link': 'https://www.mql5.com/en/code/47513', 'version': '2.23', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15631086]}, 'widths': {1: 1}, 'styles': {1: 2}, 'labels': {}, 'levels': [], 'description': ['Provides valuable insights into Moving Average values from a higher timeframe.', 'It features visual elements for streamlines analysis, including customizable trails and a dynamic MA horizontal price line.', 'The Multi-Timeframe Moving Average adapts to different timeframes, displaying values from higher timeframes if applicable.', 'A customizable Moving Average trail simplifies historical analysis.', 'The real-time dynamic MA Horizontal Price Line facilitating effective support and resistance identification.'], 'name': 'wd.Multi_LineMA', 'source': 'MQL5 Indicators/wd.Multi_LineMA/wd.Multi_LineMA.mq5', 'folder': 'wd.Multi_LineMA', 'inputs': [{'mql': 'ma_Trail', 'py': 'ma_Trail', 'param': 'ma_Trail', 'type': 'int', 'default': 35, 'label': 'MA Trail', 'sinput': False}, {'mql': 'MTF_period', 'py': 'MTF_period', 'param': 'MTF_period', 'type': 'int', 'default': 16385, 'label': 'MA TimeFrame', 'sinput': False}, {'mql': 'Comment1', 'py': 'Comment1', 'param': None, 'type': 'string', 'default': '===== Moving Average Settings =======', 'label': '=======================', 'sinput': False}, {'mql': 'ma_period', 'py': 'ma_period', 'param': 'ma_period', 'type': 'int', 'default': 3, 'label': 'MA Period', 'sinput': False}, {'mql': 'ma_shift', 'py': 'ma_shift', 'param': 'ma_shift', 'type': 'int', 'default': 0, 'label': 'MA Shift', 'sinput': False}, {'mql': 'ma_method', 'py': 'ma_method', 'param': 'ma_method', 'type': 'int', 'default': 1, 'label': 'MA Method', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'MA Applied price', 'sinput': False}, {'mql': 'ma_color', 'py': 'ma_color', 'param': None, 'type': 'color', 'default': 15631086, 'label': 'MA Color', 'sinput': False}, {'mql': 'ma_style', 'py': 'ma_style', 'param': 'ma_style', 'type': 'int', 'default': 4, 'label': 'MA Style', 'sinput': False}, {'mql': 'ma_width', 'py': 'ma_width', 'param': 'ma_width', 'type': 'int', 'default': 3, 'label': 'MA width', 'sinput': False}, {'mql': 'Comment2', 'py': 'Comment2', 'param': None, 'type': 'string', 'default': '===== MA Horizontal Price Line Settings =====', 'label': '=======================', 'sinput': False}, {'mql': 'hl_color', 'py': 'hl_color', 'param': None, 'type': 'color', 'default': 15631086, 'label': 'MA Price line color', 'sinput': False}, {'mql': 'hl_style', 'py': 'hl_style', 'param': 'hl_style', 'type': 'int', 'default': 0, 'label': 'MA Price line style', 'sinput': False}, {'mql': 'hl_width', 'py': 'hl_width', 'param': 'hl_width', 'type': 'int', 'default': 2, 'label': 'MA Price line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ma_Trail = _input('ma_Trail', 35)  # MA Trail
MTF_period = _input('MTF_period', PERIOD_H1)  # MA TimeFrame
Comment1 = _input('Comment1', '===== Moving Average Settings =======')  # =======================
ma_period = _input('ma_period', 3)  # MA Period
ma_shift = _input('ma_shift', 0)  # MA Shift
ma_method = _input('ma_method', MODE_EMA)  # MA Method
applied_price = _input('applied_price', PRICE_CLOSE)  # MA Applied price
ma_color = _input('ma_color', clrViolet)  # MA Color
ma_style = _input('ma_style', STYLE_DASHDOTDOT)  # MA Style
ma_width = _input('ma_width', 3)  # MA width
Comment2 = _input('Comment2', '===== MA Horizontal Price Line Settings =====')  # =======================
hl_color = _input('hl_color', clrViolet)  # MA Price line color
hl_style = _input('hl_style', STYLE_SOLID)  # MA Price line style
hl_width = _input('hl_width', 2)  # MA Price line width
ma_Buffer = Arr(0, 0.0)
ma_Handle = 0
short_name = ""
name_maHzLine = 'MA Horizontal Price Line'

def OnInit():
    global ma_Handle, name_maHzLine, short_name
    SetIndexBuffer(0, ma_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, ma_shift)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, ma_color)
    PlotIndexSetInteger(0, PLOT_LINE_STYLE, ma_style)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, ma_width)
    ma_Handle = iMA(Symbol(), MTF_period, ma_period, ma_shift, ma_method, applied_price)
    MTF = (Period() if (MTF_period == PERIOD_CURRENT) else MTF_period)
    short_name = StringSubstr(EnumToString(MTF, 'ENUM_TIMEFRAMES'), 7) + StringFormat('(%s,%d)', StringSubstr(EnumToString(ma_method, 'ENUM_MA_METHOD'), 5), ma_period)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA ' + short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)
    name_maHzLine = StringSubstr(EnumToString(MTF, 'ENUM_TIMEFRAMES'), 7) + StringFormat('(%d)', ma_period)
    ObjectCreate(0, name_maHzLine, OBJ_HLINE, 0, 0, SymbolInfoDouble(Symbol(), SYMBOL_BID))
    ObjectSetInteger(0, name_maHzLine, OBJPROP_COLOR, hl_color)
    ObjectSetInteger(0, name_maHzLine, OBJPROP_STYLE, hl_style)
    ObjectSetInteger(0, name_maHzLine, OBJPROP_WIDTH, hl_width)
    ObjectSetInteger(0, name_maHzLine, OBJPROP_BACK, False)
    ObjectSetInteger(0, name_maHzLine, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name_maHzLine, OBJPROP_SELECTED, False)
    ObjectSetInteger(0, name_maHzLine, OBJPROP_HIDDEN, True)
    ObjectSetString(0, name_maHzLine, OBJPROP_TEXT, name_maHzLine)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    val_HigherTF = Arr(0, 0.0)
    h = Bars(Symbol(), MTF_period, time[0], time[rates_total - 1])
    CopyBuffer(ma_Handle, 0, 0, h, val_HigherTF)
    ma_Price = Arr(0, 0.0)
    CopyBuffer(ma_Handle, 0, -ma_shift, 1, ma_Price)
    if not ma_Price[0]:
        ma_Price[0] = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ObjectMove(0, name_maHzLine, 0, 0, ma_Price[0])
    for i in range(0, rates_total - 1 + 1):
        PrevShift = iBarShift(Symbol(), MTF_period, time[i], True)
        ma_Buffer[i] = (val_HigherTF[h - PrevShift - 1] if ((PrevShift != -1 and PrevShift < h) and i >= (rates_total - ma_Trail)) else EMPTY_VALUE)
    if Period() < MTF_period:
        i = rates_total - ma_Trail
        while i <= 0:
            ma_Buffer[i] = iMA(Symbol(), MTF_period, ma_period, ma_shift, ma_method, applied_price)
            i -= 1
    else:
        for i in range(rates_total - ma_Trail, 0 - 1, -1):
            ma_Buffer[i] = EMPTY_VALUE
    return rates_total

def OnDeinit(reason):
    ObjectDelete(0, name_maHzLine)
    IndicatorRelease(ma_Handle)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WdMultiLineMA(_MQL5Indicator):
    name = 'wd.Multi_LineMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ma_Trail': 35,  # MA Trail
        'MTF_period': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # MA TimeFrame
        'ma_period': 3,  # MA Period
        'ma_shift': 0,  # MA Shift
        'ma_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA Method
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA Applied price
        'ma_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # MA Style
        'ma_width': 3,  # MA width
        'hl_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # MA Price line style
        'hl_width': 2,  # MA Price line width
    }

