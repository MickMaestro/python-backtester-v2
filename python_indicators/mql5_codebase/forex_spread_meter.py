"""Forex_Spread_Meter — converted from MQL5: MQL5 Indicators/Forex_Spread_Meter/Forex_Spread_Meter.mq5

Display the spread meter on the chart.
Copyright: Copyright © 2018, Amr Ali; Link: https://www.mql5.com/en/users/amrali; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Amr Ali', 'link': 'https://www.mql5.com/en/users/amrali', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Display the spread meter on the chart.'], 'name': 'Forex_Spread_Meter', 'source': 'MQL5 Indicators/Forex_Spread_Meter/Forex_Spread_Meter.mq5', 'folder': 'Forex_Spread_Meter', 'inputs': [{'mql': 'ColorSpread', 'py': 'ColorSpread', 'param': None, 'type': 'color', 'default': 36095, 'label': '', 'sinput': False}, {'mql': 'ColorMax', 'py': 'ColorMax', 'param': None, 'type': 'color', 'default': 17919, 'label': '', 'sinput': False}, {'mql': 'ColorAvg', 'py': 'ColorAvg', 'param': None, 'type': 'color', 'default': 36095, 'label': '', 'sinput': False}, {'mql': 'ColorMin', 'py': 'ColorMin', 'param': None, 'type': 'color', 'default': 55295, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ColorSpread = _input('ColorSpread', clrDarkOrange)
ColorMax = _input('ColorMax', clrOrangeRed)
ColorAvg = _input('ColorAvg', clrDarkOrange)
ColorMin = _input('ColorMin', clrGold)
max_spread = DBL_MIN
min_spread = DBL_MAX
avg_spread = 0.0
sum_spread = 0.0
cnt_spread = 0.0
buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, buffer, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Forex Spread Meter')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    UpdateSpreadMeter()
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'spread_meter_')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    UpdateSpreadMeter()
    buffer[0] = -1.0
    return rates_total

def UpdateSpreadMeter():
    global avg_spread, cnt_spread, max_spread, min_spread, sum_spread
    spread = _int(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD))
    max_spread = MathMax(spread, max_spread)
    min_spread = MathMin(spread, min_spread)
    cnt_spread += 1
    sum_spread = sum_spread + spread
    avg_spread = _fdiv(sum_spread, cnt_spread)
    LabelCreate(0, 'spread_meter_max', 0, 10, 24, CORNER_RIGHT_LOWER, DoubleToString(max_spread, 2), 'Arial', 8, ColorMax, 0.0, ANCHOR_RIGHT_LOWER)
    LabelCreate(0, 'spread_meter_max_label', 0, 43, 24, CORNER_RIGHT_LOWER, 'max:', 'Arial', 8, ColorMax, 0.0, ANCHOR_RIGHT_LOWER)
    LabelCreate(0, 'spread_meter_avg', 0, 10, 13, CORNER_RIGHT_LOWER, DoubleToString(avg_spread, 2), 'Arial', 8, ColorAvg, 0.0, ANCHOR_RIGHT_LOWER)
    LabelCreate(0, 'spread_meter_avg_label', 0, 43, 13, CORNER_RIGHT_LOWER, 'avg:', 'Arial', 8, ColorAvg, 0.0, ANCHOR_RIGHT_LOWER)
    LabelCreate(0, 'spread_meter_min', 0, 10, 2, CORNER_RIGHT_LOWER, DoubleToString(min_spread, 2), 'Arial', 8, ColorMin, 0.0, ANCHOR_RIGHT_LOWER)
    LabelCreate(0, 'spread_meter_min_label', 0, 43, 2, CORNER_RIGHT_LOWER, 'min:', 'Arial', 8, ColorMin, 0.0, ANCHOR_RIGHT_LOWER)
    LabelCreate(0, 'spread_meter_current', 0, 100, 5, CORNER_RIGHT_LOWER, DoubleToString(spread, 0), 'Arial', 18, ColorSpread, 0.0, ANCHOR_RIGHT_LOWER)
    LabelCreate(0, 'spread_meter_current_label', 0, 140, 5, CORNER_RIGHT_LOWER, 'Spread:', 'Arial', 18, ColorSpread, 0.0, ANCHOR_RIGHT_LOWER)

def LabelCreate(chart_ID=0, name='Label', sub_window=0, x=0, y=0, corner=CORNER_LEFT_UPPER, text='Label', font='Arial', font_size=10, clr=clrRed, angle=0.0, anchor=ANCHOR_LEFT_UPPER, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_LABEL, sub_window, 0, 0):
        Print('LabelCreate', ': failed to create text label! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
    ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
    ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
    ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
    ObjectSetDouble(chart_ID, name, OBJPROP_ANGLE, angle)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ForexSpreadMeter(_MQL5Indicator):
    name = 'Forex_Spread_Meter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

