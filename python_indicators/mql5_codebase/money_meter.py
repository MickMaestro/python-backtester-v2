"""Money-Meter — converted from MQL5: MQL5 Indicators/Money-Meter/Money-Meter.mq5

Chart evaluation in deposit currency
Copyright: Money-Meter (by Transcendreamer)

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Money-Meter (by Transcendreamer)', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Chart evaluation in deposit currency'], 'name': 'Money-Meter', 'source': 'MQL5 Indicators/Money-Meter/Money-Meter.mq5', 'folder': 'Money-Meter', 'inputs': [{'mql': 'grid_step_value', 'py': 'grid_step_value', 'param': 'grid_step_value', 'type': 'double', 'default': 100.0, 'label': '', 'sinput': False}, {'mql': 'lot_size', 'py': 'lot_size', 'param': 'lot_size', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'lot_divider', 'py': 'lot_divider', 'param': 'lot_divider', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'total_levels', 'py': 'total_levels', 'param': 'total_levels', 'type': 'double', 'default': 50.0, 'label': '', 'sinput': False}, {'mql': 'zero_price', 'py': 'zero_price', 'param': 'zero_price', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'progression', 'py': 'progression', 'param': 'progression', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'multiplicator', 'py': 'multiplicator', 'param': 'multiplicator', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'lines_color', 'py': 'lines_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}, {'mql': 'lines_width', 'py': 'lines_width', 'param': 'lines_width', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'lines_style', 'py': 'lines_style', 'param': 'lines_style', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'lines_prices', 'py': 'lines_prices', 'param': 'lines_prices', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'text_shift_bars', 'py': 'text_shift_bars', 'param': 'text_shift_bars', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'info_corner', 'py': 'info_corner', 'param': 'info_corner', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'info_shift_pixels', 'py': 'info_shift_pixels', 'param': 'info_shift_pixels', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum PROGRESSION
none = 0
equal = 1
linear = 2
fibo = 3
martin = 4
_enum('PROGRESSION', {0: 'none', 1: 'equal', 2: 'linear', 3: 'fibo', 4: 'martin'})

# ---- inputs and global variables
grid_step_value = _input('grid_step_value', 100.0)
lot_size = _input('lot_size', 0.1)
lot_divider = _input('lot_divider', 1.0)
total_levels = _input('total_levels', 50.0)
zero_price = _input('zero_price', 0.0)
progression = _input('progression', none)
multiplicator = _input('multiplicator', 2.0)
lines_color = _input('lines_color', clrMagenta)
lines_width = _input('lines_width', 1)
lines_style = _input('lines_style', STYLE_SOLID)
lines_prices = _input('lines_prices', False)
text_shift_bars = _input('text_shift_bars', 0)
info_corner = _input('info_corner', CORNER_LEFT_UPPER)
info_shift_pixels = _input('info_shift_pixels', 0)

def OnInit():
    clean_all()
    make_grid()
    put_info()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    clean_all()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def clean_all():
    ObjectDelete(0, 'INFOTEXT')
    for k in range(ObjectsTotal(0, 0, OBJ_HLINE) - 1, 0 - 1, -1):
        name = ObjectName(0, k, 0, OBJ_HLINE)
        if StringFind(name, 'GRID_LEVEL_') != -1:
            ObjectDelete(0, name)
    for k in range(ObjectsTotal(0, 0, OBJ_TEXT) - 1, 0 - 1, -1):
        name = ObjectName(0, k, 0, OBJ_TEXT)
        if StringFind(name, 'GRID_TEXT_') != -1:
            ObjectDelete(0, name)

def make_grid():
    ts = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_SIZE)
    tv = SymbolInfoDouble(Symbol(), SYMBOL_TRADE_TICK_VALUE)
    step = ((_fdiv(grid_step_value, tv) * ts) / lot_size) / lot_divider
    zero = (zero_price if zero_price else iClose(None, 0, 0))
    time = 0
    if text_shift_bars >= 0:
        time = iTime(None, 0, text_shift_bars)
    else:
        time = iTime(None, 0, 0) - (PeriodSeconds(PERIOD_CURRENT) * text_shift_bars)
    put_level('GRID_LEVEL_ZERO', zero, '(ZERO)')
    put_text('GRID_TEXT_ZERO', zero, time, '(ZERO)')
    n = 1
    while n <= total_levels:
        value = grid_step_value * get_progression(n)
        text = DoubleToString(value, 2)
        put_level('GRID_LEVEL_UP' + _str(n), zero + (step * n), '+' + text)
        put_level('GRID_LEVEL_DN' + _str(n), zero - (step * n), '-' + text)
        put_text('GRID_TEXT_UP' + _str(n), zero + (step * n), time, '+' + text)
        put_text('GRID_TEXT_DN' + _str(n), zero - (step * n), time, '-' + text)
        n += 1

def get_progression(n):
    if progression == none:
        return n
    sum_ = 0.0
    for k in range(1, n + 1):
        sum_ += (n - k + 1) * get_member(k)
    return sum_

def get_member(k):
    if progression == equal:
        return 1.0
    elif progression == fibo:
        if k < 3:
            return 1.0
        f = 1
        s = 1
        while k > 2:
            f = f + (s * 2)
            s = f - s
            f = f - s
            k -= 1
        return s
    elif progression == martin:
        return MathPow(multiplicator, k - 1)
    elif progression == linear:
        return k
    return 1.0

def put_info():
    ObjectCreate(0, 'INFOTEXT', OBJ_LABEL, 0, 0, 0)
    ObjectSetInteger(0, 'INFOTEXT', OBJPROP_XDISTANCE, 5)
    ObjectSetInteger(0, 'INFOTEXT', OBJPROP_YDISTANCE, 17 + info_shift_pixels)
    ObjectSetInteger(0, 'INFOTEXT', OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, 'INFOTEXT', OBJPROP_SELECTED, False)
    anchor = 0
    if info_corner == CORNER_LEFT_LOWER:
        anchor = ANCHOR_LEFT_LOWER
    if info_corner == CORNER_LEFT_UPPER:
        anchor = ANCHOR_LEFT_UPPER
    if info_corner == CORNER_RIGHT_LOWER:
        anchor = ANCHOR_RIGHT_LOWER
    if info_corner == CORNER_RIGHT_UPPER:
        anchor = ANCHOR_RIGHT_UPPER
    ObjectSetInteger(0, 'INFOTEXT', OBJPROP_CORNER, info_corner)
    ObjectSetInteger(0, 'INFOTEXT', OBJPROP_ANCHOR, anchor)
    text = 'LOT:' + DoubleToString(lot_size / lot_divider, 2)
    if progression == none:
        text += '  MODE:NONE'
    if progression == equal:
        text += '  MODE:EQUAL'
    if progression == linear:
        text += '  MODE:LINEAR'
    if progression == fibo:
        text += '  MODE:FIBO'
    if progression == martin:
        text += '  MODE:MARTIN *' + DoubleToString(multiplicator, 2)
    ObjectSetString(0, 'INFOTEXT', OBJPROP_TEXT, text)
    ObjectSetString(0, 'INFOTEXT', OBJPROP_FONT, 'Verdana')
    ObjectSetInteger(0, 'INFOTEXT', OBJPROP_COLOR, lines_color)

def put_level(name, price, text):
    ObjectCreate(0, name, OBJ_HLINE, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, price)
    ObjectSetInteger(0, name, OBJPROP_COLOR, lines_color)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, lines_width)
    ObjectSetInteger(0, name, OBJPROP_STYLE, lines_style)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_SELECTED, False)
    ObjectSetInteger(0, name, OBJPROP_BACK, not lines_prices)
    ObjectSetString(0, name, OBJPROP_TEXT, text)

def put_text(name, price, time, text):
    ObjectCreate(0, name, OBJ_TEXT, 0, 0, 0)
    ObjectSetDouble(0, name, OBJPROP_PRICE, price)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetString(0, name, OBJPROP_FONT, 'Verdana')
    ObjectSetInteger(0, name, OBJPROP_COLOR, lines_color)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_RIGHT_UPPER)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_SELECTED, False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MoneyMeter(_MQL5Indicator):
    name = 'Money-Meter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'grid_step_value': 100.0,
        'lot_size': 0.1,
        'lot_divider': 1.0,
        'total_levels': 50.0,
        'zero_price': 0.0,
        'progression': _Choice({0: 'none', 1: 'equal', 2: 'linear', 3: 'fibo', 4: 'martin'}, default=0),
        'multiplicator': 2.0,
        'lines_width': 1,
        'lines_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'lines_prices': False,
        'text_shift_bars': 0,
        'info_corner': _Choice({0: 'CORNER_LEFT_UPPER', 1: 'CORNER_LEFT_LOWER', 2: 'CORNER_RIGHT_LOWER', 3: 'CORNER_RIGHT_UPPER'}, default=0),
        'info_shift_pixels': 0,
    }

