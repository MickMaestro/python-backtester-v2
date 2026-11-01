"""i-drprojections — converted from MQL5: MQL5 Indicators/i-DRProjections/i-drprojections.mq5

The indicator predicts daily price ranges
Copyright: Copyright © 2005, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [15658671]}, 'widths': {}, 'styles': {}, 'labels': {1: 'i-DRProjections'}, 'levels': [], 'description': ['The indicator predicts daily price ranges'], 'name': 'i-drprojections', 'source': 'MQL5 Indicators/i-DRProjections/i-drprojections.mq5', 'folder': 'i-DRProjections', 'inputs': [{'mql': 'level_name', 'py': 'level_name', 'param': None, 'type': 'string', 'default': 'i-DRProjections', 'label': 'The name of the trigger level', 'sinput': False}, {'mql': 'ShowTomorrow', 'py': 'ShowTomorrow', 'param': 'ShowTomorrow', 'type': 'bool', 'default': True, 'label': 'Show tomorrow', 'sinput': False}, {'mql': 'up_level_color', 'py': 'up_level_color', 'param': None, 'type': 'color', 'default': 65280, 'label': 'The color of the resistance level', 'sinput': False}, {'mql': 'up_level_style', 'py': 'up_level_style', 'param': 'up_level_style', 'type': 'int', 'default': 0, 'label': 'The style of the resistance level', 'sinput': False}, {'mql': 'up_level_width', 'py': 'up_level_width', 'param': 'up_level_width', 'type': 'int', 'default': 2, 'label': 'The width of the resistance level', 'sinput': False}, {'mql': 'dn_level_color', 'py': 'dn_level_color', 'param': None, 'type': 'color', 'default': 255, 'label': 'The color of the resistance level', 'sinput': False}, {'mql': 'dn_level_style', 'py': 'dn_level_style', 'param': 'dn_level_style', 'type': 'int', 'default': 0, 'label': 'The style of the resistance level', 'sinput': False}, {'mql': 'dn_level_width', 'py': 'dn_level_width', 'param': 'dn_level_width', 'type': 'int', 'default': 2, 'label': 'The width of the resistance level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
level_name = _input('level_name', 'i-DRProjections')  # The name of the trigger level
ShowTomorrow = _input('ShowTomorrow', True)  # Show tomorrow
up_level_color = _input('up_level_color', clrLime)  # The color of the resistance level
up_level_style = _input('up_level_style', STYLE_SOLID)  # The style of the resistance level
up_level_width = _input('up_level_width', w_2)  # The width of the resistance level
dn_level_color = _input('dn_level_color', clrRed)  # The color of the resistance level
dn_level_style = _input('dn_level_style', STYLE_SOLID)  # The style of the resistance level
dn_level_width = _input('dn_level_width', w_2)  # The width of the resistance level
upname = ""
dnname = ""
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)

def OnInit():
    global dnname, min_rates_total, upname
    if not TimeFramesCheck(Period()):
        return INIT_FAILED
    min_rates_total = 10
    upname = level_name + ' upper'
    dnname = level_name + ' lower'
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-DRProjections')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, upname)
    ObjectDelete(0, dnname)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    x = 0.0
    iOpen_ = Arr(1, 0.0, dyn=False)
    iLow_ = Arr(1, 0.0, dyn=False)
    iHigh_ = Arr(1, 0.0, dyn=False)
    iClose_ = Arr(1, 0.0, dyn=False)
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = _s_OnCalculate_LastCountBar + rates_total - prev_calculated
    ArraySetAsSeries(Time, True)
    for bar in range(limit, 0 - 1, -1):
        bar1 = bar + 1
        tm0 = MqlDateTime()
        tm1 = MqlDateTime()
        TimeToStruct(Time[bar], tm0)
        TimeToStruct(Time[bar1], tm1)
        if tm1.day_of_week != tm0.day_of_week:
            _s_OnCalculate_LastCountBar = bar
            ExtABuffer[bar1] = 0.0
            ExtBBuffer[bar1] = 0.0
            if CopyOpen(Symbol(), PERIOD_D1, _DT(Time[bar1]), 1, iOpen_) <= 0:
                return 0
            if CopyHigh(Symbol(), PERIOD_D1, _DT(Time[bar1]), 1, iHigh_) <= 0:
                return 0
            if CopyLow(Symbol(), PERIOD_D1, _DT(Time[bar1]), 1, iLow_) <= 0:
                return 0
            if CopyClose(Symbol(), PERIOD_D1, _DT(Time[bar1]), 1, iClose_) <= 0:
                return 0
            x = (iHigh_[0] + iLow_[0] + iClose_[0]) / 2
            if iClose_[0] < iOpen_[0]:
                x += iLow_[0] / 2
            if iClose_[0] > iOpen_[0]:
                x += iHigh_[0] / 2
            if iClose_[0] == iOpen_[0]:
                x += iClose_[0] / 2
            ExtABuffer[bar] = x - iLow_[0]
            ExtBBuffer[bar] = x - iHigh_[0]
        else:
            ExtABuffer[bar] = ExtABuffer[bar1]
            ExtBBuffer[bar] = ExtBBuffer[bar1]
    if ShowTomorrow:
        if CopyOpen(Symbol(), PERIOD_D1, _DT(Time[0]), 1, iOpen_) <= 0:
            return 0
        if CopyHigh(Symbol(), PERIOD_D1, _DT(Time[0]), 1, iHigh_) <= 0:
            return 0
        if CopyLow(Symbol(), PERIOD_D1, _DT(Time[0]), 1, iLow_) <= 0:
            return 0
        if CopyClose(Symbol(), PERIOD_D1, _DT(Time[0]), 1, iClose_) <= 0:
            return 0
        x = (iHigh_[0] + iLow_[0] + iClose_[0]) / 2
        if iClose_[0] < iOpen_[0]:
            x += iLow_[0] / 2
        if iClose_[0] > iOpen_[0]:
            x += iHigh_[0] / 2
        if iClose_[0] == iOpen_[0]:
            x += iClose_[0] / 2
        Min = x - iLow_[0]
        Max = x - iHigh_[0]
        SetTline(0, upname, 0, Time[1], Min, TimeCurrent(), Min, up_level_color, up_level_style, up_level_width, upname)
        SetTline(0, dnname, 0, Time[1], Max, TimeCurrent(), Max, dn_level_color, dn_level_style, dn_level_width, dnname)
    ChartRedraw(0)
    return rates_total

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, True)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def TimeFramesCheck(TFrame):
    if TFrame > PERIOD_H12:
        Print('Chart period cannot be greater than H12!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    return True

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IDrprojections(_MQL5Indicator):
    name = 'i-drprojections'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ShowTomorrow': True,  # Show tomorrow
        'up_level_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # The style of the resistance level
        'up_level_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # The width of the resistance level
        'dn_level_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # The style of the resistance level
        'dn_level_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # The width of the resistance level
    }

