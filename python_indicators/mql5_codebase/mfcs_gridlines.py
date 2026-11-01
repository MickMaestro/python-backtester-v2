"""mfcs_gridlines — converted from MQL5: MQL5 Indicators/Horizontal GridLines/mfcs_gridlines.mq5

Copyright: Copyright 2015, Mansukh Patidar, All rights reserved.; Link: http://www.mansukhpatidar.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, Mansukh Patidar, All rights reserved.', 'link': 'http://www.mansukhpatidar.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'mfcs_gridlines', 'source': 'MQL5 Indicators/Horizontal GridLines/mfcs_gridlines.mq5', 'folder': 'Horizontal GridLines', 'inputs': [{'mql': 'lines', 'py': 'lines', 'param': 'lines', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'interval', 'py': 'interval', 'param': 'interval', 'type': 'int', 'default': 200, 'label': '', 'sinput': False}, {'mql': 'line_style', 'py': 'line_style', 'param': 'line_style', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'line_width', 'py': 'line_width', 'param': 'line_width', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'line_color', 'py': 'line_color', 'param': None, 'type': 'color', 'default': 3289728, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
lines = _input('lines', 100)
interval = _input('interval', 200)
line_style = _input('line_style', STYLE_DOT)
line_width = _input('line_width', 1)
line_color = _input('line_color', 0x323280)

def ClearExistingGridLines():
    index = 0
    index = 0
    for index in range(index, lines * 5):
        n1 = Symbol() + '_MFCS_GRID_LINES_ABOVE_' + _str(index)
        n2 = Symbol() + '_MFCS_GRID_LINES_BELOW_' + _str(index)
        ObjectDelete(0, n1)
        e1 = ObjectFind(0, n1)
        ObjectDelete(0, n2)
        e2 = ObjectFind(0, n1)
        if e1 >= 0 or e2 >= 0:
            printf('error in removing gridlines')
    else:
        index = _range_end(index, lines * 5, 1)

def OnDeinit(reason):
    ClearExistingGridLines()

def OnInit():
    ClearExistingGridLines()
    last_tick = MqlTick()
    SymbolInfoTick(Symbol(), last_tick)
    base_price = last_tick.ask
    pip_value = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
    multipler = _int(pow(10, SymbolInfoInteger(Symbol(), SYMBOL_DIGITS)))
    temp_price = _long(base_price * multipler)
    temp_price = temp_price - _imod(temp_price, 1000)
    base_price = temp_price * pip_value
    index = 0
    index = 0
    for index in range(index, lines):
        p1 = base_price + (index * interval * pip_value)
        p2 = base_price - (index * interval * pip_value)
        n1 = Symbol() + '_MFCS_GRID_LINES_ABOVE_' + _str(index)
        n2 = Symbol() + '_MFCS_GRID_LINES_BELOW_' + _str(index)
        ObjectCreate(0, n1, OBJ_HLINE, 0, 0, p1)
        ObjectCreate(0, n2, OBJ_HLINE, 0, 0, p2)
        back = False
        ObjectSetInteger(0, n1, OBJPROP_COLOR, line_color)
        ObjectSetInteger(0, n1, OBJPROP_STYLE, line_style)
        ObjectSetInteger(0, n1, OBJPROP_WIDTH, line_width)
        ObjectSetInteger(0, n1, OBJPROP_BACK, back)
        ObjectSetInteger(0, n2, OBJPROP_COLOR, line_color)
        ObjectSetInteger(0, n2, OBJPROP_STYLE, line_style)
        ObjectSetInteger(0, n2, OBJPROP_WIDTH, line_width)
        ObjectSetInteger(0, n2, OBJPROP_BACK, back)
    else:
        index = _range_end(index, lines, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MfcsGridlines(_MQL5Indicator):
    name = 'mfcs_gridlines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'lines': 100,
        'interval': 200,
        'line_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),
        'line_width': 1,
    }

