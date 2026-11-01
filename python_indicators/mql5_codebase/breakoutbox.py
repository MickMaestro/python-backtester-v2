"""BreakOutBox — converted from MQL5: MQL5 Indicators/Consolidation Detector/BreakOutBox.mq5

Link: https://twitter.comDarkRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://twitter.comDarkRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'BreakOutBox', 'source': 'MQL5 Indicators/Consolidation Detector/BreakOutBox.mq5', 'folder': 'Consolidation Detector', 'inputs': [{'mql': 'InpName', 'py': 'InpName', 'param': None, 'type': 'string', 'default': 'Box ', 'label': 'Channel name', 'sinput': False}, {'mql': 'InpColor', 'py': 'InpColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Channel color', 'sinput': False}, {'mql': 'InpStyle', 'py': 'InpStyle', 'param': 'InpStyle', 'type': 'int', 'default': 4, 'label': 'Style of Channel  lines', 'sinput': False}, {'mql': 'InpWidth', 'py': 'InpWidth', 'param': 'InpWidth', 'type': 'int', 'default': 2, 'label': 'Width of Channel  lines', 'sinput': False}, {'mql': 'InpBack', 'py': 'InpBack', 'param': 'InpBack', 'type': 'bool', 'default': True, 'label': 'Background Channel', 'sinput': False}, {'mql': 'InpSelection', 'py': 'InpSelection', 'param': 'InpSelection', 'type': 'bool', 'default': False, 'label': 'Highlight to move', 'sinput': False}, {'mql': 'InpHidden', 'py': 'InpHidden', 'param': 'InpHidden', 'type': 'bool', 'default': True, 'label': 'Hidden in the object list', 'sinput': False}, {'mql': 'InpZOrder', 'py': 'InpZOrder', 'param': 'InpZOrder', 'type': 'long', 'default': 0, 'label': 'Priority for mouse click', 'sinput': False}, {'mql': 'InpFill2', 'py': 'InpFill2', 'param': 'InpFill2', 'type': 'bool', 'default': False, 'label': 'Filling the channel with color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BoxHeight = 30
BoxLength = 140
InpName = _input('InpName', 'Box ')  # Channel name
InpColor = _input('InpColor', clrMagenta)  # Channel color
InpStyle = _input('InpStyle', STYLE_DASHDOTDOT)  # Style of Channel  lines
InpWidth = _input('InpWidth', 2)  # Width of Channel  lines
InpBack = _input('InpBack', True)  # Background Channel
InpSelection = _input('InpSelection', False)  # Highlight to move
InpHidden = _input('InpHidden', True)  # Hidden in the object list
InpZOrder = _input('InpZOrder', 0)  # Priority for mouse click
InpFill2 = _input('InpFill2', False)  # Filling the channel with color
InpRayLeft = False  # Channel 's continuation to the left
InpRayRight = False  # Channel 's continuation to the right
break_out_box = False
break_out_up = False
break_out_down = False
box_start = 0
box_end = 0
highest = 0.0
lowest = 0.0
range_ = 0.0
box_high = 0.0
box_low = 0.0
range_time = 0

def OnInit():
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global box_end, box_high, box_low, box_start, break_out_box, break_out_down, break_out_up, highest, lowest, range_, range_time
    highest = high[0]
    lowest = low[0]
    for i in range(1, rates_total):
        if close[i] > highest:
            highest = close[i]
        if close[i] < lowest:
            lowest = close[i]
        range_ = highest - lowest
        range_time += 1
        if range_ < (BoxHeight * Point() * 10) and range_time >= BoxLength:
            break_out_box = True
            box_high = highest
            box_low = lowest
            box_start = time[MathAbs(i - range_time)]
        elif ((range_ > (BoxHeight * Point() * 10) and range_time >= BoxLength) and break_out_box == True) and box_high < highest:
            break_out_up = True
            break_out_down = False
            break_out_box = False
            box_end = time[i - 1]
            if not ChannelCreate(0, InpName + IntegerToString(i), 0, box_start, box_high, box_end, box_high, box_start, box_low, InpColor, InpStyle, InpWidth, InpFill2, InpBack, InpSelection, InpRayLeft, InpRayRight, InpHidden, InpZOrder):
                return 0
            range_ = 0.0
            range_time = 0
        elif ((range_ > (BoxHeight * Point() * 10) and range_time >= BoxLength) and break_out_box == True) and box_low > lowest:
            break_out_down = True
            break_out_up = False
            break_out_box = False
            box_end = time[i - 1]
            if not ChannelCreate(0, InpName + IntegerToString(i), 0, box_start, box_high, box_end, box_high, box_start, box_low, InpColor, InpStyle, InpWidth, InpFill2, InpBack, InpSelection, InpRayLeft, InpRayRight, InpHidden, InpZOrder):
                return 0
            range_ = 0.0
            range_time = 0
        elif range_ > (BoxHeight * Point() * 10) and range_time <= BoxLength:
            range_ = 0.0
            range_time = 0
            highest = high[i]
            lowest = low[i]
    return rates_total

def OnDeinit(reason):
    ObjectsDeleteAll(0, -1, OBJ_CHANNEL)

def ChannelCreate(chart_ID=0, name='Channel', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, time3=0, price3=0.0, clr=clrRed, style=STYLE_SOLID, width=1, fill=False, back=False, selection=True, ray_left=False, ray_right=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_CHANNEL, sub_window, time1, price1, time2, price2, time3, price3):
        Print('ChannelCreate', ': failed to create an equidistant channel! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_FILL, fill)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_LEFT, ray_left)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BreakOutBox(_MQL5Indicator):
    name = 'BreakOutBox'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Style of Channel  lines
        'InpWidth': 2,  # Width of Channel  lines
        'InpBack': True,  # Background Channel
        'InpSelection': False,  # Highlight to move
        'InpHidden': True,  # Hidden in the object list
        'InpZOrder': 0,  # Priority for mouse click
        'InpFill2': False,  # Filling the channel with color
    }

