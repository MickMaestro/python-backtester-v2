"""Price increase Indicator — converted from MQL5: MQL5 Indicators/Price increase Indicator/Price increase Indicator.mq5

Copyright: Copyright 2024, Igor Widiger; Link: info@p24m.eu; Version: 3.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Igor Widiger', 'link': 'info@p24m.eu', 'version': '3.00', 'window': 'chart', 'indicator_plots': 1, 'indicator_buffers': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Price increase Indicator', 'source': 'MQL5 Indicators/Price increase Indicator/Price increase Indicator.mq5', 'folder': 'Price increase Indicator', 'inputs': [{'mql': 'RangeShowDays', 'py': 'RangeShowDays', 'param': 'RangeShowDays', 'type': 'int', 'default': 10, 'label': 'Range show in days', 'sinput': False}, {'mql': 'RangeLineWidht', 'py': 'RangeLineWidht', 'param': 'RangeLineWidht', 'type': 'int', 'default': 2, 'label': 'Range line width', 'sinput': False}, {'mql': 'RangeLineHighColor', 'py': 'RangeLineHighColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Range High color', 'sinput': False}, {'mql': 'RangeLineLowColor', 'py': 'RangeLineLowColor', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Range Low color', 'sinput': False}, {'mql': 'Text_font_name', 'py': 'Text_font_name', 'param': None, 'type': 'string', 'default': 'Trebuchet MS', 'label': 'Range text Windows Fonts', 'sinput': False}, {'mql': 'TextSize', 'py': 'TextSize', 'param': 'TextSize', 'type': 'int', 'default': 10, 'label': 'Range text size', 'sinput': False}, {'mql': 'style_line', 'py': 'style_line', 'param': 'style_line', 'type': 'int', 'default': 0, 'label': 'Range Line style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RangeShowDays = _input('RangeShowDays', 10)  # Range show in days
RangeLineWidht = _input('RangeLineWidht', 2)  # Range line width
RangeLineHighColor = _input('RangeLineHighColor', clrDodgerBlue)  # Range High color
RangeLineLowColor = _input('RangeLineLowColor', clrOrangeRed)  # Range Low color
Text_font_name = _input('Text_font_name', 'Trebuchet MS')  # Range text Windows Fonts
TextSize = _input('TextSize', 10)  # Range text size
style_line = _input('style_line', STYLE_SOLID)  # Range Line style

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'HIGH_LINIE_')
    ObjectsDeleteAll(0, 'LOW_LINIE_')
    ObjectsDeleteAll(0, 'TEXT_')
    ObjectsDeleteAll(0, 'TEXT_PROCENT_')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for i in range(0, RangeShowDays):
        DayHigh = iHigh(None, PERIOD_D1, i)
        DayLow = iLow(None, PERIOD_D1, i)
        DaySpanne = NormalizeDouble(_fdiv(DayHigh - DayLow, Point()), Digits())
        SpanneProzent = NormalizeDouble(_fdiv(DayHigh - DayLow, DayHigh) * 100, 2)
        DayCloseI = iClose(None, PERIOD_D1, i + 1)
        DayClose0 = iClose(None, PERIOD_D1, i)
        PCalculate = 0.0
        PCalculate = NormalizeDouble(_fdiv(DayClose0 - DayCloseI, DayClose0) * 100, 2)
        prexix = i
        time_start = iTime(Symbol(), PERIOD_D1, i)
        time_end = iTime(Symbol(), PERIOD_D1, i) + (60 * 60 * 24)
        if DayClose0 > 0:
            TEXT_SHOW('TEXT_PROCENT_' + _str(prexix), 'Price change: => ' + DoubleToString(PCalculate, 2) + ' % ', time_end, DayLow, (RangeLineHighColor if (DoubleToString(PCalculate, 2) > _str(0)) else RangeLineLowColor))
        LINIE_SHOW('HIGH_LINIE_' + _str(prexix), time_start, DayHigh, time_end, DayHigh, RangeLineHighColor)
        LINIE_SHOW('LOW_LINIE_' + _str(prexix), time_start, DayLow, time_end, DayLow, RangeLineLowColor)
        TEXT_SHOW('TEXT_' + _str(prexix), 'Daily range: => ' + DoubleToString(SpanneProzent, 2) + ' % ', time_end, DayHigh, RangeLineHighColor)
        ChartRedraw(0)
    return rates_total

def LINIE_SHOW(NAME, TIME1, PRICE1, TIME2, PRICE2, COLOR):
    back = True
    ray_left = False
    ray_right = False
    ObjectDelete(ChartID(), NAME)
    ObjectCreate(ChartID(), NAME, OBJ_TREND, 0, TIME1, PRICE1, TIME2, PRICE2)
    ObjectSetInteger(ChartID(), NAME, OBJPROP_COLOR, COLOR)
    ObjectSetInteger(ChartID(), NAME, OBJPROP_WIDTH, RangeLineWidht)
    ObjectSetInteger(ChartID(), NAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(ChartID(), NAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(ChartID(), NAME, OBJPROP_STYLE, style_line)
    ObjectSetInteger(ChartID(), NAME, OBJPROP_RAY_RIGHT, ray_right)
    ObjectSetInteger(ChartID(), NAME, OBJPROP_RAY_LEFT, ray_left)
    ObjectSetInteger(ChartID(), NAME, OBJPROP_BACK, back)

def TEXT_SHOW(TEXTNAME, TEXT, TIME1, PRICE, COLOR):
    anchor = ANCHOR_RIGHT_LOWER
    ObjectDelete(ChartID(), TEXTNAME)
    ObjectCreate(ChartID(), TEXTNAME, OBJ_TEXT, 0, TIME1, PRICE)
    ObjectSetString(ChartID(), TEXTNAME, OBJPROP_TEXT, TEXT)
    ObjectSetString(ChartID(), TEXTNAME, OBJPROP_FONT, Text_font_name)
    ObjectSetInteger(ChartID(), TEXTNAME, OBJPROP_FONTSIZE, TextSize)
    ObjectSetInteger(ChartID(), TEXTNAME, OBJPROP_ANCHOR, anchor)
    ObjectSetInteger(ChartID(), TEXTNAME, OBJPROP_COLOR, COLOR)
    ObjectSetInteger(ChartID(), TEXTNAME, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(ChartID(), TEXTNAME, OBJPROP_SELECTED, False)
    ObjectSetInteger(ChartID(), TEXTNAME, OBJPROP_BACK, True)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceIncreaseIndicator(_MQL5Indicator):
    name = 'Price increase Indicator'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangeShowDays': 10,  # Range show in days
        'RangeLineWidht': 2,  # Range line width
        'TextSize': 10,  # Range text size
        'style_line': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Range Line style
    }

