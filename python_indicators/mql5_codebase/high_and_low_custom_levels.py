"""High_and_Low_Custom_levels — converted from MQL5: MQL5 Indicators/High and Low Custom levels/High_and_Low_Custom_levels.mq5

Copyright: Copyright 2017, MetaQuotes Software Corp.; Link: https://www.mql5.com; Version: 1.002

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, MetaQuotes Software Corp.', 'link': 'https://www.mql5.com', 'version': '1.002', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'High_and_Low_Custom_levels', 'source': 'MQL5 Indicators/High and Low Custom levels/High_and_Low_Custom_levels.mq5', 'folder': 'High and Low Custom levels', 'inputs': [{'mql': '_0_', 'py': '_0_', 'param': None, 'type': 'string', 'default': '*-*-*-*-*-*', 'label': 'Global parameters', 'sinput': True}, {'mql': 'shift_high', 'py': 'shift_high', 'param': 'shift_high', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'shift_low', 'py': 'shift_low', 'param': 'shift_low', 'type': 'int', 'default': -10, 'label': '', 'sinput': False}, {'mql': 'count_day', 'py': 'count_day', 'param': 'count_day', 'type': 'uchar', 'default': 3, 'label': 'count day "0" -> current day', 'sinput': False}, {'mql': '_1_', 'py': '_1_', 'param': None, 'type': 'string', 'default': '*-*-*-*-*-*', 'label': 'High Level parameters', 'sinput': True}, {'mql': 'InpColorHigh', 'py': 'InpColorHigh', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Line color', 'sinput': False}, {'mql': 'InpStyleHigh', 'py': 'InpStyleHigh', 'param': 'InpStyleHigh', 'type': 'int', 'default': 1, 'label': 'Line style', 'sinput': False}, {'mql': 'InpWidthHigh', 'py': 'InpWidthHigh', 'param': 'InpWidthHigh', 'type': 'int', 'default': 1, 'label': 'Line width', 'sinput': False}, {'mql': '_2_', 'py': '_2_', 'param': None, 'type': 'string', 'default': 'Low Level parameters', 'label': '', 'sinput': True}, {'mql': 'InpColorLow', 'py': 'InpColorLow', 'param': None, 'type': 'color', 'default': 255, 'label': 'Line color', 'sinput': False}, {'mql': 'InpStyleLow', 'py': 'InpStyleLow', 'param': 'InpStyleLow', 'type': 'int', 'default': 1, 'label': 'Line style', 'sinput': False}, {'mql': 'InpWidthLow', 'py': 'InpWidthLow', 'param': 'InpWidthLow', 'type': 'int', 'default': 1, 'label': 'Line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
_0_ = _input('_0_', '*-*-*-*-*-*')  # Global parameters
shift_high = _input('shift_high', 10)
shift_low = _input('shift_low', -10)
count_day = _input('count_day', 3)  # count day "0" -> current day
_1_ = _input('_1_', '*-*-*-*-*-*')  # High Level parameters
InpColorHigh = _input('InpColorHigh', clrBlue)  # Line color
InpStyleHigh = _input('InpStyleHigh', STYLE_DASH)  # Line style
InpWidthHigh = _input('InpWidthHigh', 1)  # Line width
_2_ = _input('_2_', 'Low Level parameters')
InpColorLow = _input('InpColorLow', clrRed)  # Line color
InpStyleLow = _input('InpStyleLow', STYLE_DASH)  # Line style
InpWidthLow = _input('InpWidthLow', 1)  # Line width
name_high = 'High Level'
name_low = 'Low Level'
m_adjusted_point = 0.0  # point value adjusted for 3 or 5 points

def OnInit():
    global m_adjusted_point
    digits_adjust = 1
    if Digits() == 3 or Digits() == 5:
        digits_adjust = 10
    m_adjusted_point = Point() * digits_adjust
    if ObjectFind(0, name_high) < 0:
        HLineCreate(0, name_high, 0, 0.0, InpColorHigh, InpStyleHigh, InpWidthHigh)
    if ObjectFind(0, name_low) < 0:
        HLineCreate(0, name_low, 0, 0.0, InpColorLow, InpStyleLow, InpWidthLow)
    rates_array = Arr(0, 0, factory=MqlRates)
    CopyRates(Symbol(), PERIOD_D1, 0, count_day, rates_array)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Print('OnDeinit', ', ', reason)
    if reason == 1:
        HLineDelete(0, name_high)
        HLineDelete(0, name_low)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_number
    _s_OnCalculate_number += 1
    if _imod(_s_OnCalculate_number, 50) == 0:
        _s_OnCalculate_number = 0
    else:
        return rates_total
    High = Arr(0, 0.0)
    Low = Arr(0, 0.0)
    count = (1 if (count_day == 0) else count_day)
    CopyHigh(Symbol(), PERIOD_D1, 0, count, High)
    CopyLow(Symbol(), PERIOD_D1, 0, count, Low)
    price_high = 0.0
    price_low = 0.0
    if count_day > 0:
        price_high = High[ArrayMaximum(High, 0, WHOLE_ARRAY)]
        price_low = Low[ArrayMinimum(Low, 0, WHOLE_ARRAY)]
    else:
        price_high = High[0]
        price_low = Low[0]
    price_high += shift_high * m_adjusted_point
    price_low += shift_low * m_adjusted_point
    if ObjectFind(0, name_high) < 0:
        HLineCreate(0, name_high, 0, 0.0, InpColorHigh, InpStyleHigh, InpWidthHigh)
    HLineMove(0, name_high, price_high)
    if ObjectFind(0, name_low) < 0:
        HLineCreate(0, name_low, 0, 0.0, InpColorLow, InpStyleLow, InpWidthLow)
    HLineMove(0, name_low, price_low)
    return rates_total

def HLineCreate(chart_ID=0, name='HLine', sub_window=0, price=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, hidden=True, z_order=0):
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_HLINE, sub_window, 0, price):
        Print('HLineCreate', ': failed to create a horizontal line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    return True

def HLineMove(chart_ID=0, name='HLine', price=0.0):
    if not price:
        price = SymbolInfoDouble(Symbol(), SYMBOL_BID)
    ResetLastError()
    if not ObjectMove(chart_ID, name, 0, 0, price):
        Print('HLineMove', ': failed to move the horizontal line! Error code = ', GetLastError())
        return False
    return True

def HLineDelete(chart_ID=0, name='HLine'):
    ResetLastError()
    if not ObjectDelete(chart_ID, name):
        Print('HLineDelete', ': failed to delete a horizontal line! Error code = ', GetLastError())
        return False
    return True

# ---- static local variables
_s_OnCalculate_number = -9


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HighAndLowCustomLevels(_MQL5Indicator):
    name = 'High_and_Low_Custom_levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'shift_high': 10,
        'shift_low': -10,
        'count_day': 3,  # count day "0" -> current day
        'InpStyleHigh': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # Line style
        'InpWidthHigh': 1,  # Line width
        'InpStyleLow': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=1),  # Line style
        'InpWidthLow': 1,  # Line width
    }

