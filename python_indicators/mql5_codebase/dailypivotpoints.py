"""dailypivotpoints — converted from MQL5: MQL5 Indicators/DailyPivotPoints/dailypivotpoints.mq5

Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [16711935]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 4, 2: 4}, 'labels': {}, 'levels': [], 'description': [], 'name': 'dailypivotpoints', 'source': 'MQL5 Indicators/DailyPivotPoints/dailypivotpoints.mq5', 'folder': 'DailyPivotPoints', 'inputs': [{'mql': 'ExtFormula', 'py': 'ExtFormula', 'param': 'ExtFormula', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ExtHowManyDays', 'py': 'ExtHowManyDays', 'param': 'ExtHowManyDays', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'ExtDraw', 'py': 'ExtDraw', 'param': 'ExtDraw', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Color_R30', 'py': 'Color_R30', 'param': None, 'type': 'color', 'default': 0, 'label': 'R30 level color', 'sinput': False}, {'mql': 'Color_R25', 'py': 'Color_R25', 'param': None, 'type': 'color', 'default': 0, 'label': 'R25 level color', 'sinput': False}, {'mql': 'Color_R20', 'py': 'Color_R20', 'param': None, 'type': 'color', 'default': 0, 'label': 'R20 level color', 'sinput': False}, {'mql': 'Color_R15', 'py': 'Color_R15', 'param': None, 'type': 'color', 'default': 0, 'label': 'R15 level color', 'sinput': False}, {'mql': 'Color_R10', 'py': 'Color_R10', 'param': None, 'type': 'color', 'default': 0, 'label': 'R10 level color', 'sinput': False}, {'mql': 'Color_R05', 'py': 'Color_R05', 'param': None, 'type': 'color', 'default': 0, 'label': 'R05 level color', 'sinput': False}, {'mql': 'Color_P', 'py': 'Color_P', 'param': None, 'type': 'color', 'default': 0, 'label': 'P level color', 'sinput': False}, {'mql': 'Color_S05', 'py': 'Color_S05', 'param': None, 'type': 'color', 'default': 0, 'label': 'S05 level color', 'sinput': False}, {'mql': 'Color_S10', 'py': 'Color_S10', 'param': None, 'type': 'color', 'default': 0, 'label': 'S10 level color', 'sinput': False}, {'mql': 'Color_S15', 'py': 'Color_S15', 'param': None, 'type': 'color', 'default': 0, 'label': 'S15 level color', 'sinput': False}, {'mql': 'Color_S20', 'py': 'Color_S20', 'param': None, 'type': 'color', 'default': 0, 'label': 'S20 level color', 'sinput': False}, {'mql': 'Color_S25', 'py': 'Color_S25', 'param': None, 'type': 'color', 'default': 0, 'label': 'S25 level color', 'sinput': False}, {'mql': 'Color_S30', 'py': 'Color_S30', 'param': None, 'type': 'color', 'default': 0, 'label': 'S30 level color', 'sinput': False}, {'mql': 'Style_R30', 'py': 'Style_R30', 'param': 'Style_R30', 'type': 'int', 'default': 0, 'label': 'R30 level line style', 'sinput': False}, {'mql': 'Style_R25', 'py': 'Style_R25', 'param': 'Style_R25', 'type': 'int', 'default': 4, 'label': 'R25 level line style', 'sinput': False}, {'mql': 'Style_R20', 'py': 'Style_R20', 'param': 'Style_R20', 'type': 'int', 'default': 0, 'label': 'R20 level line style', 'sinput': False}, {'mql': 'Style_R15', 'py': 'Style_R15', 'param': 'Style_R15', 'type': 'int', 'default': 4, 'label': 'R15 level line style', 'sinput': False}, {'mql': 'Style_R10', 'py': 'Style_R10', 'param': 'Style_R10', 'type': 'int', 'default': 0, 'label': 'R10 level line style', 'sinput': False}, {'mql': 'Style_R05', 'py': 'Style_R05', 'param': 'Style_R05', 'type': 'int', 'default': 4, 'label': 'R05 level line style', 'sinput': False}, {'mql': 'Style_P', 'py': 'Style_P', 'param': 'Style_P', 'type': 'int', 'default': 1, 'label': 'P level line style', 'sinput': False}, {'mql': 'Style_S05', 'py': 'Style_S05', 'param': 'Style_S05', 'type': 'int', 'default': 4, 'label': 'S05 level line style', 'sinput': False}, {'mql': 'Style_S10', 'py': 'Style_S10', 'param': 'Style_S10', 'type': 'int', 'default': 0, 'label': 'S10 level line style', 'sinput': False}, {'mql': 'Style_S15', 'py': 'Style_S15', 'param': 'Style_S15', 'type': 'int', 'default': 4, 'label': 'S15 level line style', 'sinput': False}, {'mql': 'Style_S20', 'py': 'Style_S20', 'param': 'Style_S20', 'type': 'int', 'default': 0, 'label': 'S20 level line style', 'sinput': False}, {'mql': 'Style_S25', 'py': 'Style_S25', 'param': 'Style_S25', 'type': 'int', 'default': 4, 'label': 'S25 level line style', 'sinput': False}, {'mql': 'Style_S30', 'py': 'Style_S30', 'param': 'Style_S30', 'type': 'int', 'default': 0, 'label': 'S30 level line style', 'sinput': False}, {'mql': 'Width_R30', 'py': 'Width_R30', 'param': 'Width_R30', 'type': 'int', 'default': 1, 'label': 'R30 level line width', 'sinput': False}, {'mql': 'Width_R25', 'py': 'Width_R25', 'param': 'Width_R25', 'type': 'int', 'default': 1, 'label': 'R25 level line width', 'sinput': False}, {'mql': 'Width_R20', 'py': 'Width_R20', 'param': 'Width_R20', 'type': 'int', 'default': 2, 'label': 'R20 level line width', 'sinput': False}, {'mql': 'Width_R15', 'py': 'Width_R15', 'param': 'Width_R15', 'type': 'int', 'default': 1, 'label': 'R15 level line width', 'sinput': False}, {'mql': 'Width_R10', 'py': 'Width_R10', 'param': 'Width_R10', 'type': 'int', 'default': 3, 'label': 'R10 level line width', 'sinput': False}, {'mql': 'Width_R05', 'py': 'Width_R05', 'param': 'Width_R05', 'type': 'int', 'default': 1, 'label': 'R05 level line width', 'sinput': False}, {'mql': 'Width_P', 'py': 'Width_P', 'param': 'Width_P', 'type': 'int', 'default': 1, 'label': 'P level line width', 'sinput': False}, {'mql': 'Width_S05', 'py': 'Width_S05', 'param': 'Width_S05', 'type': 'int', 'default': 1, 'label': 'S05 level line width', 'sinput': False}, {'mql': 'Width_S10', 'py': 'Width_S10', 'param': 'Width_S10', 'type': 'int', 'default': 3, 'label': 'S10 level line width', 'sinput': False}, {'mql': 'Width_S15', 'py': 'Width_S15', 'param': 'Width_S15', 'type': 'int', 'default': 1, 'label': 'S15 level line width', 'sinput': False}, {'mql': 'Width_S20', 'py': 'Width_S20', 'param': 'Width_S20', 'type': 'int', 'default': 2, 'label': 'S20 level line width', 'sinput': False}, {'mql': 'Width_S25', 'py': 'Width_S25', 'param': 'Width_S25', 'type': 'int', 'default': 1, 'label': 'S25 level line width', 'sinput': False}, {'mql': 'Width_S30', 'py': 'Width_S30', 'param': 'Width_S30', 'type': 'int', 'default': 1, 'label': 'S30 level line width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkOrchid = 0xCC3299  # MQL4 colour name
MediumSeaGreen = 0x71B33C  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum Number
Number_0 = 0
Number_1 = 1
Number_2 = 2
Number_3 = 3
_enum('Number', {0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'})

# enum Width
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('Width', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
ExtFormula = _input('ExtFormula', Number_0)
ExtHowManyDays = _input('ExtHowManyDays', 30)
ExtDraw = _input('ExtDraw', True)
Style_R30 = _input('Style_R30', SOLID_)  # R30 level line style
Style_R25 = _input('Style_R25', DASHDOTDOT_)  # R25 level line style
Style_R20 = _input('Style_R20', SOLID_)  # R20 level line style
Style_R15 = _input('Style_R15', DASHDOTDOT_)  # R15 level line style
Style_R10 = _input('Style_R10', SOLID_)  # R10 level line style
Style_R05 = _input('Style_R05', DASHDOTDOT_)  # R05 level line style
Style_P = _input('Style_P', DASH_)  # P level line style
Style_S05 = _input('Style_S05', DASHDOTDOT_)  # S05 level line style
Style_S10 = _input('Style_S10', SOLID_)  # S10 level line style
Style_S15 = _input('Style_S15', DASHDOTDOT_)  # S15 level line style
Style_S20 = _input('Style_S20', SOLID_)  # S20 level line style
Style_S25 = _input('Style_S25', DASHDOTDOT_)  # S25 level line style
Style_S30 = _input('Style_S30', SOLID_)  # S30 level line style
Width_R30 = _input('Width_R30', Width_1)  # R30 level line width
Width_R25 = _input('Width_R25', Width_1)  # R25 level line width
Width_R20 = _input('Width_R20', Width_2)  # R20 level line width
Width_R15 = _input('Width_R15', Width_1)  # R15 level line width
Width_R10 = _input('Width_R10', Width_3)  # R10 level line width
Width_R05 = _input('Width_R05', Width_1)  # R05 level line width
Width_P = _input('Width_P', Width_1)  # P level line width
Width_S05 = _input('Width_S05', Width_1)  # S05 level line width
Width_S10 = _input('Width_S10', Width_3)  # S10 level line width
Width_S15 = _input('Width_S15', Width_1)  # S15 level line width
Width_S20 = _input('Width_S20', Width_2)  # S20 level line width
Width_S25 = _input('Width_S25', Width_1)  # S25 level line width
Width_S30 = _input('Width_S30', Width_1)  # S30 level line width
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)

def CreateHline(chart_id, name, nwin, price, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)

def iBarShift_u(symbol, timeframe, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    time1 = 0
    time1 = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        size = ArraySize(Arr_)
        return size - 1
    else:
        return -1

def OnInit():
    draw_begin = 0
    if ExtHowManyDays < 1:
        draw_begin = 0
    else:
        draw_begin = ExtHowManyDays
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
    ArraySetAsSeries(ExtMapBuffer1, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, 0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, draw_begin)
    ArraySetAsSeries(ExtMapBuffer2, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if ExtDraw:
        if ExtFormula == Number_0:
            IndicatorSetString(INDICATOR_SHORTNAME, 'Pivot')
            PlotIndexSetString(0, PLOT_LABEL, 'Pivot')
            PlotIndexSetString(1, PLOT_LABEL, None)
        else:
            IndicatorSetString(INDICATOR_SHORTNAME, 'Support&Resistance')
            PlotIndexSetString(0, PLOT_LABEL, 'Resistance')
            PlotIndexSetString(1, PLOT_LABEL, 'Support')
    else:
        PlotIndexSetString(0, PLOT_LABEL, None)
        PlotIndexSetString(1, PLOT_LABEL, None)

def OnDeinit(reason):
    ObjectDelete(0, 'Pivot_Line')
    ObjectDelete(0, 'R0.5_Line')
    ObjectDelete(0, 'R1.0_Line')
    ObjectDelete(0, 'R1.5_Line')
    ObjectDelete(0, 'R2.0_Line')
    ObjectDelete(0, 'R2.5_Line')
    ObjectDelete(0, 'R3.0_Line')
    ObjectDelete(0, 'S0.5_Line')
    ObjectDelete(0, 'S1.0_Line')
    ObjectDelete(0, 'S1.5_Line')
    ObjectDelete(0, 'S2.0_Line')
    ObjectDelete(0, 'S2.5_Line')
    ObjectDelete(0, 'S3.0_Line')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_P, _s_OnCalculate_R05, _s_OnCalculate_R10, _s_OnCalculate_R15, _s_OnCalculate_R20, _s_OnCalculate_R25, _s_OnCalculate_R30, _s_OnCalculate_S05, _s_OnCalculate_S10, _s_OnCalculate_S15, _s_OnCalculate_S20, _s_OnCalculate_S25, _s_OnCalculate_S30, _s_OnCalculate_yesterday_close, _s_OnCalculate_yesterday_high, _s_OnCalculate_yesterday_low
    if Period() >= PERIOD_D1:
        return 0
    if prev_calculated != rates_total:
        begin_bar = 0
        first_bar = 0
        last_bar = 0
        cnt = 0
        copy = 0
        S = 0.0
        R = 0.0
        today_open = 0.0
        iClose_ = Arr(0, 0.0)
        iOpen_ = Arr(0, 0.0)
        iHigh_ = Arr(0, 0.0)
        iLow_ = Arr(0, 0.0)
        iTime_ = Arr(0, 0)
        if ExtHowManyDays < 1:
            begin_bar = Bars(None, PERIOD_D1) - 2
        else:
            begin_bar = ExtHowManyDays - 1
        ArraySetAsSeries(time, True)
        ArraySetAsSeries(iTime_, True)
        ArraySetAsSeries(iClose_, True)
        ArraySetAsSeries(iOpen_, True)
        ArraySetAsSeries(iHigh_, True)
        ArraySetAsSeries(iLow_, True)
        copy = begin_bar + 2
        if CopyTime(None, PERIOD_D1, 0, copy, iTime_) < copy:
            return 0
        if CopyClose(None, PERIOD_D1, 0, copy, iClose_) < copy:
            return 0
        if CopyOpen(None, PERIOD_D1, 0, copy, iOpen_) < copy:
            return 0
        if CopyHigh(None, PERIOD_D1, 0, copy, iHigh_) < copy:
            return 0
        if CopyLow(None, PERIOD_D1, 0, copy, iLow_) < copy:
            return 0
        cnt = 0
        while True:
            if iTime_[0] >= (time[0] - (PERIOD_D1 * 60)):
                break
            cnt += 1
            if cnt > 5:
                return 0
            Sleep(1000)
        if ExtDraw == False or prev_calculated != 0:
            begin_bar = 0
        cnt = begin_bar
        for cnt in range(cnt, 0 - 1, -1):
            if cnt < rates_total:
                ExtMapBuffer1[cnt] = 0.0
                ExtMapBuffer2[cnt] = 0.0
            _s_OnCalculate_yesterday_close = iClose_[cnt + 1]
            today_open = iOpen_[cnt]
            _s_OnCalculate_yesterday_high = iHigh_[cnt + 1]
            _s_OnCalculate_yesterday_low = iLow_[cnt + 1]
            _s_OnCalculate_P = (_s_OnCalculate_yesterday_high + _s_OnCalculate_yesterday_low + _s_OnCalculate_yesterday_close + today_open) / 4
            _sw1 = ExtFormula
            if _sw1 == 1:
                R = _s_OnCalculate_P + _s_OnCalculate_P - _s_OnCalculate_yesterday_low
                S = _s_OnCalculate_P + _s_OnCalculate_P - _s_OnCalculate_yesterday_high
            elif _sw1 == 2:
                R = _s_OnCalculate_P + _s_OnCalculate_yesterday_high - _s_OnCalculate_yesterday_low
                S = _s_OnCalculate_P - _s_OnCalculate_yesterday_high + _s_OnCalculate_yesterday_low
            elif _sw1 == 3:
                R = _s_OnCalculate_P + _s_OnCalculate_P - _s_OnCalculate_yesterday_low - _s_OnCalculate_yesterday_low + _s_OnCalculate_yesterday_high
                S = _s_OnCalculate_P + _s_OnCalculate_P - _s_OnCalculate_yesterday_high - _s_OnCalculate_yesterday_high + _s_OnCalculate_yesterday_low
            if ExtDraw == True:
                first_bar = iBarShift_u("", 0, iTime_[cnt]) - 1
                if cnt > 0:
                    last_bar = iBarShift_u("", 0, iTime_[cnt - 1]) - 1
                else:
                    last_bar = 0
                while first_bar >= last_bar:
                    if (first_bar == last_bar and last_bar > 0) or first_bar < 0:
                        break
                    if ExtFormula == 0:
                        ExtMapBuffer1[first_bar] = _s_OnCalculate_P
                    else:
                        ExtMapBuffer1[first_bar] = R
                        ExtMapBuffer2[first_bar] = S
                    first_bar -= 1
        else:
            cnt = _range_end(cnt, 0 - 1, -1)
        _s_OnCalculate_P = NormalizeDouble((_s_OnCalculate_yesterday_high + _s_OnCalculate_yesterday_low + _s_OnCalculate_yesterday_close) / 3, Digits())
        _s_OnCalculate_R10 = NormalizeDouble((2 * _s_OnCalculate_P) - _s_OnCalculate_yesterday_low, Digits())
        _s_OnCalculate_S10 = NormalizeDouble((2 * _s_OnCalculate_P) - _s_OnCalculate_yesterday_high, Digits())
        _s_OnCalculate_R05 = NormalizeDouble((_s_OnCalculate_P + _s_OnCalculate_R10) / 2, Digits())
        _s_OnCalculate_S05 = NormalizeDouble((_s_OnCalculate_P + _s_OnCalculate_S10) / 2, Digits())
        _s_OnCalculate_R20 = NormalizeDouble(_s_OnCalculate_P + (_s_OnCalculate_yesterday_high - _s_OnCalculate_yesterday_low), Digits())
        _s_OnCalculate_S20 = NormalizeDouble(_s_OnCalculate_P - (_s_OnCalculate_yesterday_high - _s_OnCalculate_yesterday_low), Digits())
        _s_OnCalculate_R15 = NormalizeDouble((_s_OnCalculate_R10 + _s_OnCalculate_R20) / 2, Digits())
        _s_OnCalculate_S15 = NormalizeDouble((_s_OnCalculate_S10 + _s_OnCalculate_S20) / 2, Digits())
        _s_OnCalculate_R30 = NormalizeDouble((2 * _s_OnCalculate_P) + (_s_OnCalculate_yesterday_high - (2 * _s_OnCalculate_yesterday_low)), Digits())
        _s_OnCalculate_S30 = NormalizeDouble((2 * _s_OnCalculate_P) - ((2 * _s_OnCalculate_yesterday_high) - _s_OnCalculate_yesterday_low), Digits())
        _s_OnCalculate_R25 = NormalizeDouble((_s_OnCalculate_R20 + _s_OnCalculate_R30) / 2, Digits())
        _s_OnCalculate_S25 = NormalizeDouble((_s_OnCalculate_S20 + _s_OnCalculate_S30) / 2, Digits())
    SetHline(0, 'R3.0_Line', 0, _s_OnCalculate_R30, Color_R30, Style_R30, Width_R30, 'Pivot ' + DoubleToString(_s_OnCalculate_R30, Digits()))
    SetHline(0, 'R2.5_Line', 0, _s_OnCalculate_R25, Color_R25, Style_R25, Width_R25, 'Pivot ' + DoubleToString(_s_OnCalculate_R25, Digits()))
    SetHline(0, 'R2.0_Line', 0, _s_OnCalculate_R20, Color_R20, Style_R20, Width_R20, 'Pivot ' + DoubleToString(_s_OnCalculate_R20, Digits()))
    SetHline(0, 'R1.5_Line', 0, _s_OnCalculate_R15, Color_R15, Style_R15, Width_R15, 'Pivot ' + DoubleToString(_s_OnCalculate_R15, Digits()))
    SetHline(0, 'R1.0_Line', 0, _s_OnCalculate_R10, Color_R10, Style_R10, Width_R10, 'Pivot ' + DoubleToString(_s_OnCalculate_R10, Digits()))
    SetHline(0, 'R0.5_Line', 0, _s_OnCalculate_R05, Color_R05, Style_R05, Width_R05, 'Pivot ' + DoubleToString(_s_OnCalculate_R05, Digits()))
    SetHline(0, 'Pivot_Line', 0, _s_OnCalculate_P, Color_P, Style_P, Width_P, 'Pivot ' + DoubleToString(_s_OnCalculate_P, Digits()))
    SetHline(0, 'S0.5_Line', 0, _s_OnCalculate_S05, Color_S05, Style_S05, Width_S05, 'Pivot ' + DoubleToString(_s_OnCalculate_S05, Digits()))
    SetHline(0, 'S1.0_Line', 0, _s_OnCalculate_S10, Color_S10, Style_S10, Width_S10, 'Pivot ' + DoubleToString(_s_OnCalculate_S10, Digits()))
    SetHline(0, 'S1.5_Line', 0, _s_OnCalculate_S15, Color_S15, Style_S15, Width_S15, 'Pivot ' + DoubleToString(_s_OnCalculate_S15, Digits()))
    SetHline(0, 'S2.0_Line', 0, _s_OnCalculate_S20, Color_S20, Style_S20, Width_S20, 'Pivot ' + DoubleToString(_s_OnCalculate_S20, Digits()))
    SetHline(0, 'S2.5_Line', 0, _s_OnCalculate_S25, Color_S25, Style_S25, Width_S25, 'Pivot ' + DoubleToString(_s_OnCalculate_S25, Digits()))
    SetHline(0, 'S3.0_Line', 0, _s_OnCalculate_S30, Color_S30, Style_S30, Width_S30, 'Pivot ' + DoubleToString(_s_OnCalculate_S30, Digits()))
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
Color_R30 = _input('Color_R30', _uint(MediumSeaGreen))  # R30 level color
Color_R25 = _input('Color_R25', _uint(MediumSeaGreen))  # R25 level color
Color_R20 = _input('Color_R20', _uint(MediumSeaGreen))  # R20 level color
Color_R15 = _input('Color_R15', _uint(MediumSeaGreen))  # R15 level color
Color_R10 = _input('Color_R10', _uint(MediumSeaGreen))  # R10 level color
Color_R05 = _input('Color_R05', _uint(MediumSeaGreen))  # R05 level color
Color_P = _input('Color_P', _uint(DarkOrchid))  # P level color
Color_S05 = _input('Color_S05', _uint(Red))  # S05 level color
Color_S10 = _input('Color_S10', _uint(Red))  # S10 level color
Color_S15 = _input('Color_S15', _uint(Red))  # S15 level color
Color_S20 = _input('Color_S20', _uint(Red))  # S20 level color
Color_S25 = _input('Color_S25', _uint(Red))  # S25 level color
Color_S30 = _input('Color_S30', _uint(Red))  # S30 level color

# ---- static local variables
_s_OnCalculate_yesterday_high = 0.0
_s_OnCalculate_yesterday_low = 0.0
_s_OnCalculate_yesterday_close = 0.0
_s_OnCalculate_P = 0.0
_s_OnCalculate_S05 = 0.0
_s_OnCalculate_R05 = 0.0
_s_OnCalculate_S10 = 0.0
_s_OnCalculate_R10 = 0.0
_s_OnCalculate_S15 = 0.0
_s_OnCalculate_R15 = 0.0
_s_OnCalculate_S20 = 0.0
_s_OnCalculate_R20 = 0.0
_s_OnCalculate_S25 = 0.0
_s_OnCalculate_R25 = 0.0
_s_OnCalculate_S30 = 0.0
_s_OnCalculate_R30 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dailypivotpoints(_MQL5Indicator):
    name = 'dailypivotpoints'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtFormula': _Choice({0: 'Number_0', 1: 'Number_1', 2: 'Number_2', 3: 'Number_3'}, default=0),
        'ExtHowManyDays': 30,
        'ExtDraw': True,
        'Style_R30': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # R30 level line style
        'Style_R25': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # R25 level line style
        'Style_R20': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # R20 level line style
        'Style_R15': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # R15 level line style
        'Style_R10': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # R10 level line style
        'Style_R05': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # R05 level line style
        'Style_P': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # P level line style
        'Style_S05': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # S05 level line style
        'Style_S10': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # S10 level line style
        'Style_S15': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # S15 level line style
        'Style_S20': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # S20 level line style
        'Style_S25': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # S25 level line style
        'Style_S30': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=0),  # S30 level line style
        'Width_R30': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # R30 level line width
        'Width_R25': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # R25 level line width
        'Width_R20': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # R20 level line width
        'Width_R15': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # R15 level line width
        'Width_R10': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # R10 level line width
        'Width_R05': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # R05 level line width
        'Width_P': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # P level line width
        'Width_S05': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # S05 level line width
        'Width_S10': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # S10 level line width
        'Width_S15': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # S15 level line width
        'Width_S20': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=2),  # S20 level line width
        'Width_S25': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # S25 level line width
        'Width_S30': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # S30 level line width
    }

