"""DailyVerticalLines — converted from MQL5: MQL5 Indicators/Daily Vertical Lines/DailyVerticalLines.mq5

Draw daily vertical lines plus the day of week labels on the chart.
Copyright: Copyright © 2018, Amr Ali; Link: https://www.mql5.com/en/users/amrali; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Amr Ali', 'link': 'https://www.mql5.com/en/users/amrali', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Draw daily vertical lines plus the day of week labels on the chart.'], 'name': 'DailyVerticalLines', 'source': 'MQL5 Indicators/Daily Vertical Lines/DailyVerticalLines.mq5', 'folder': 'Daily Vertical Lines', 'inputs': [{'mql': 'InpMaxDays', 'py': 'InpMaxDays', 'param': 'InpMaxDays', 'type': 'int', 'default': 20, 'label': 'Maximum daily lines to show', 'sinput': False}, {'mql': 'InpVLineStyle', 'py': 'InpVLineStyle', 'param': 'InpVLineStyle', 'type': 'int', 'default': 4, 'label': 'Daily vertical lines style', 'sinput': False}, {'mql': 'InpVLineColor', 'py': 'InpVLineColor', 'param': None, 'type': 'color', 'default': 65535, 'label': 'Daily vertical lines color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMaxDays = _input('InpMaxDays', 20)  # Maximum daily lines to show
InpVLineStyle = _input('InpVLineStyle', STYLE_DASHDOTDOT)  # Daily vertical lines style
InpVLineColor = _input('InpVLineColor', clrYellow)  # Daily vertical lines color
obj_name_prefix = '5days_'

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, obj_name_prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    P = Period()
    if P > PERIOD_D1:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(low, True)
    if rates_total > prev_calculated:
        cnt = MathMin(rates_total, _idiv(PeriodSeconds(PERIOD_D1), PeriodSeconds(P)) * InpMaxDays)
        for i in range(0, cnt):
            if TimeDayOfWeek_u(time[i]) != TimeDayOfWeek_u(time[i + 1]):
                wkday = EnumToString(TimeDayOfWeek_u(time[i]), 'ENUM_DAY_OF_WEEK')
                name = obj_name_prefix + wkday + '_' + TimeToString(time[i])
                VLineCreate(name, time[i], InpVLineColor, InpVLineStyle)
                TextCreate(name + '_lbl', wkday, time[i], low[i] - (50 * Point()), InpVLineColor)
    return rates_total

def VLineCreate(name, time, clr, style=STYLE_SOLID, width=1):
    ObjectCreate(0, name, OBJ_VLINE, 0, time, 0)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, name, OBJPROP_STYLE, style)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(0, name, OBJPROP_BACK, False)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_SELECTED, False)

def TextCreate(name, text, time, price, clr=clrWhiteSmoke):
    ObjectCreate(0, name, OBJ_TEXT, 0, time, price)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT)
    ObjectSetDouble(0, name, OBJPROP_ANGLE, 0.0)
    ObjectSetString(0, name, OBJPROP_FONT, 'Lucida Console')
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(0, name, OBJPROP_BACK, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_SELECTED, False)

def TimeDayOfWeek_u(t):
    st = MqlDateTime()
    TimeToStruct(t, st)
    return st.day_of_week


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailyVerticalLines(_MQL5Indicator):
    name = 'DailyVerticalLines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMaxDays': 20,  # Maximum daily lines to show
        'InpVLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Daily vertical lines style
    }

