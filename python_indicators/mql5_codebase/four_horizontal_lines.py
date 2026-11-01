"""Four horizontal lines — converted from MQL5: MQL5 Indicators/Four horizontal lines/Four horizontal lines.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [''], 'name': 'Four horizontal lines', 'source': 'MQL5 Indicators/Four horizontal lines/Four horizontal lines.mq5', 'folder': 'Four horizontal lines', 'inputs': [{'mql': 'InpColorHighLow', 'py': 'InpColorHighLow', 'param': None, 'type': 'color', 'default': 255, 'label': 'HighLow: Line color', 'sinput': False}, {'mql': 'InpColorDifference', 'py': 'InpColorDifference', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Difference: Line color', 'sinput': False}, {'mql': 'InpStyle', 'py': 'InpStyle', 'param': 'InpStyle', 'type': 'int', 'default': 0, 'label': 'Line style', 'sinput': False}, {'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'int', 'default': 2, 'label': 'Line width', 'sinput': False}, {'mql': 'InpBack', 'py': 'InpBack', 'param': 'InpBack', 'type': 'bool', 'default': False, 'label': 'Background line', 'sinput': False}, {'mql': 'InpSelection', 'py': 'InpSelection', 'param': 'InpSelection', 'type': 'bool', 'default': False, 'label': 'Highlight to move', 'sinput': False}, {'mql': 'InpHidden', 'py': 'InpHidden', 'param': 'InpHidden', 'type': 'bool', 'default': True, 'label': 'Hidden in the object list', 'sinput': False}, {'mql': 'InpZOrder', 'py': 'InpZOrder', 'param': 'InpZOrder', 'type': 'long', 'default': 0, 'label': 'Priority for mouse click', 'sinput': False}, {'mql': 'InpBarNumber', 'py': 'InpBarNumber', 'param': 'InpBarNumber', 'type': 'int', 'default': 1, 'label': 'Bar number', 'sinput': False}, {'mql': 'InpShiftHighLowUP', 'py': 'InpShiftHighLowUP', 'param': 'InpShiftHighLowUP', 'type': 'int', 'default': 20, 'label': 'Shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpColorHighLow = _input('InpColorHighLow', clrRed)  # HighLow: Line color
InpColorDifference = _input('InpColorDifference', clrLimeGreen)  # Difference: Line color
InpStyle = _input('InpStyle', STYLE_SOLID)  # Line style
InpWidth = _input('InpWidth', 2)  # Line width
InpBack = _input('InpBack', False)  # Background line
InpSelection = _input('InpSelection', False)  # Highlight to move
InpHidden = _input('InpHidden', True)  # Hidden in the object list
InpZOrder = _input('InpZOrder', 0)  # Priority for mouse click
InpBarNumber = _input('InpBarNumber', 1)  # Bar number
InpShiftHighLowUP = _input('InpShiftHighLowUP', 20)  # Shift
ExtNameHighLowUP = 'HighLowUP'  # HighLowUP: Line name
ExtNameHighLowDOWN = 'HighLowDOWN'  # HighLowDOWN: Line name
ExtNameDifferenceUP = 'DifferenceUP'  # DifferenceUP: Line name
ExtNameDifferenceDOWN = 'DifferenceDOWN'  # DifferenceDOWN: Line name
ExtInpShiftHighLowUP = 0.0

def OnInit():
    global ExtInpShiftHighLowUP
    HLineCreate(0, ExtNameHighLowUP, 0, 0.0, InpColorHighLow, InpStyle, InpWidth, InpBack, InpSelection, InpHidden, InpZOrder)
    HLineCreate(0, ExtNameHighLowDOWN, 0, 0.0, InpColorHighLow, InpStyle, InpWidth, InpBack, InpSelection, InpHidden, InpZOrder)
    HLineCreate(0, ExtNameDifferenceUP, 0, 0.0, InpColorDifference, InpStyle, InpWidth, InpBack, InpSelection, InpHidden, InpZOrder)
    HLineCreate(0, ExtNameDifferenceDOWN, 0, 0.0, InpColorDifference, InpStyle, InpWidth, InpBack, InpSelection, InpHidden, InpZOrder)
    ExtInpShiftHighLowUP = InpShiftHighLowUP * Point()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    HLineDelete(0, ExtNameHighLowUP)
    HLineDelete(0, ExtNameHighLowDOWN)
    HLineDelete(0, ExtNameDifferenceUP)
    HLineDelete(0, ExtNameDifferenceDOWN)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == 0 or rates_total != prev_calculated:
        high_1 = high[rates_total - 1 - InpBarNumber]
        low_1 = low[rates_total - 1 - InpBarNumber]
        HLineMove(0, ExtNameHighLowUP, high_1 + ExtInpShiftHighLowUP)
        HLineMove(0, ExtNameHighLowDOWN, low_1 - ExtInpShiftHighLowUP)
        HLineMove(0, ExtNameDifferenceUP, high_1 + (high_1 - low_1) - (ExtInpShiftHighLowUP / 2.0))
        HLineMove(0, ExtNameDifferenceDOWN, low_1 - (high_1 - low_1) + (ExtInpShiftHighLowUP / 2.0))
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
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FourHorizontalLines(_MQL5Indicator):
    name = 'Four horizontal lines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Line style
        'InpWidth': 2,  # Line width
        'InpBack': False,  # Background line
        'InpSelection': False,  # Highlight to move
        'InpHidden': True,  # Hidden in the object list
        'InpZOrder': 0,  # Priority for mouse click
        'InpBarNumber': 1,  # Bar number
        'InpShiftHighLowUP': 20,  # Shift
    }

