"""morningflat — converted from MQL5: MQL5 Indicators/MorningFlat/morningflat.mq5

Morning flat
Copyright: Copyright © 2006, Scriptong; Link:  ; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Scriptong', 'link': ' ', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680], 2: [255], 3: [8421376], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Line', 2: 'Lower Line', 3: 'Target Upper Line', 4: 'Target Lower Line'}, 'levels': [], 'description': ['Morning flat'], 'name': 'morningflat', 'source': 'MQL5 Indicators/MorningFlat/morningflat.mq5', 'folder': 'MorningFlat', 'inputs': [{'mql': 'BarsTotal', 'py': 'BarsTotal', 'param': 'BarsTotal', 'type': 'uint', 'default': 500, 'label': '', 'sinput': False}, {'mql': 'StartHour', 'py': 'StartHour', 'param': 'StartHour', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'EndHour', 'py': 'EndHour', 'param': 'EndHour', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'TargetLevel', 'py': 'TargetLevel', 'param': 'TargetLevel', 'type': 'double', 'default': 161.8, 'label': '', 'sinput': False}, {'mql': 'UpColor', 'py': 'UpColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'DnColor', 'py': 'DnColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'TargetUpColor', 'py': 'TargetUpColor', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}, {'mql': 'TargetDnColor', 'py': 'TargetDnColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Hour
H00 = 0
H01 = 1
H02 = 2
H03 = 3
H04 = 4
H05 = 5
H06 = 6
H07 = 7
H08 = 8
H09 = 9
H10 = 10
H11 = 11
H12 = 12
H13 = 13
H14 = 14
H15 = 15
H16 = 16
H17 = 17
H18 = 18
H19 = 19
H20 = 20
H21 = 21
H22 = 22
H23 = 23
_enum('Hour', {0: 'H00', 1: 'H01', 2: 'H02', 3: 'H03', 4: 'H04', 5: 'H05', 6: 'H06', 7: 'H07', 8: 'H08', 9: 'H09', 10: 'H10', 11: 'H11', 12: 'H12', 13: 'H13', 14: 'H14', 15: 'H15', 16: 'H16', 17: 'H17', 18: 'H18', 19: 'H19', 20: 'H20', 21: 'H21', 22: 'H22', 23: 'H23'})

# ---- inputs and global variables
BarsTotal = _input('BarsTotal', 500)
StartHour = _input('StartHour', H00)
EndHour = _input('EndHour', H08)
TargetLevel = _input('TargetLevel', 161.8)
UpColor = _input('UpColor', clrBlue)
DnColor = _input('DnColor', clrRed)
TargetUpColor = _input('TargetUpColor', clrTeal)
TargetDnColor = _input('TargetDnColor', clrMagenta)
Up = Arr(0, 0.0)
Down = Arr(0, 0.0)
TargetUp = Arr(0, 0.0)
TargetDn = Arr(0, 0.0)
LastDay = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    if Period() > PERIOD_H1:
        Comment('The indicator works at all timeframes less than H2!')
        return
    min_rates_total = _idiv(2 * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT))
    SetIndexBuffer(0, Up, INDICATOR_DATA)
    SetIndexBuffer(1, Down, INDICATOR_DATA)
    SetIndexBuffer(2, TargetUp, INDICATOR_DATA)
    SetIndexBuffer(3, TargetDn, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Up, True)
    ArraySetAsSeries(Down, True)
    ArraySetAsSeries(TargetUp, True)
    ArraySetAsSeries(TargetDn, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MorningFlat')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    Comment('')
    total = 0
    name = ""
    sirname = ""
    total = ObjectsTotal(0, 0, -1) - 1
    for numb in range(total, 0 - 1, -1):
        name = ObjectName(0, numb, 0, -1)
        sirname = StringSubstr(name, 0, StringLen('Lab'))
        if sirname == 'Lab':
            ObjectDelete(0, name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global LastDay
    if rates_total < min_rates_total or Period() > PERIOD_H1:
        return 0
    Comment('')
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = 0
    Name = ""
    Text = ""
    LastDay = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        for bar in range(rates_total - 1, 0 - 1, -1):
            TargetUp[bar] = 0.0
            TargetDn[bar] = 0.0
            Up[bar] = 0.0
            Down[bar] = 0.0
        limit = rates_total - 1 - min_rates_total
        limit = _int(MathMin(BarsTotal, limit))
    else:
        limit = rates_total - prev_calculated
    for bar in range(limit, 0 - 1, -1):
        tqq = MqlDateTime()
        TimeToStruct(time[bar], tqq)
        if tqq.hour >= EndHour:
            iTime_ = Arr(1, 0, dyn=False)
            if CopyTime(Symbol(), PERIOD_D1, _DT(time[bar]), 1, iTime_) <= 0:
                return 0
            BeginDay = iTime_[0]
            NextDay = BeginDay + 86400
            if LastDay >= BeginDay:
                continue
            maxbar = rates_total - 1 - min_rates_total
            StartBar = MathMin(maxbar, iBarShift_u(Symbol(), 0, BeginDay + (StartHour * 3600)))
            FinishBar = MathMin(maxbar, iBarShift_u(Symbol(), 0, BeginDay + (EndHour * 3600)) + 1)
            BarX = MathMin(StartBar - FinishBar + 1, maxbar)
            if _int(BarX + FinishBar) > (rates_total - 1):
                continue
            LowV = NormalizeDouble(low[MathMax(0, ArrayMinimum(low, FinishBar, BarX))], Digits())
            HighV = NormalizeDouble(high[MathMax(0, ArrayMaximum(high, FinishBar, BarX))], Digits())
            TargetU = NormalizeDouble((((HighV - LowV) * (TargetLevel - 100)) / 100) + HighV, Digits())
            TargetD = NormalizeDouble(LowV - (((HighV - LowV) * (TargetLevel - 100)) / 100), Digits())
            for kkk in range(StartBar, FinishBar - 1, -1):
                Up[kkk] = HighV
                Down[kkk] = LowV
                TargetUp[kkk] = 0.0
                TargetDn[kkk] = 0.0
            fff = FinishBar
            while fff >= 0 and time[fff] < NextDay:
                TargetUp[fff] = TargetU
                TargetDn[fff] = TargetD
                Up[fff] = 0.0
                Down[fff] = 0.0
                fff -= 1
            TB = time[iBarShift_u(Symbol(), 0, BeginDay)]
            Name = 'Lab' + DoubleToString(TB, 0) + 'U'
            SetArrowLeftPrice(0, Name, 0, TB, HighV, UpColor, 1)
            Name = 'Lab' + DoubleToString(TB, 0) + 'D'
            SetArrowLeftPrice(0, Name, 0, TB, LowV, DnColor, 1)
            Name = 'Lab' + DoubleToString(TB, 0) + 'U1'
            SetArrowLeftPrice(0, Name, 0, time[FinishBar], TargetU, TargetUpColor, 1)
            Name = 'Lab' + DoubleToString(TB, 0) + 'D1'
            SetArrowLeftPrice(0, Name, 0, time[FinishBar], TargetD, TargetDnColor, 1)
            Name = 'LabWidth' + _str(TB)
            Text = DoubleToString(MathRound(_fdiv(HighV - LowV, Point())), 0)
            CreateText(0, Name, 0, _idiv(time[FinishBar] - TB, 2) + TB, HighV, Text, clrMagenta, 'Georgia', 10, ANCHOR_UPPER)
    ChartRedraw(0)
    return rates_total

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

def CreateArrowLeftPrice(chart_id, name, nwin, Time, Price, Color, Size):
    ObjectCreate(chart_id, name, OBJ_ARROW_LEFT_PRICE, nwin, Time, Price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, Size)

def SetArrowLeftPrice(chart_id, name, nwin, Time, Price, Color, Size):
    if ObjectFind(chart_id, name) == -1:
        CreateArrowLeftPrice(chart_id, name, nwin, Time, Price, Color, Size)
    else:
        ObjectMove(chart_id, name, 0, Time, Price)

def CreateText(chart_id, name, nwin, time, price, text, Color, Font, Size, point):
    ObjectCreate(chart_id, name, OBJ_TEXT, nwin, time, price)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetString(chart_id, name, OBJPROP_FONT, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, Size)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_ANCHOR, point)

def SetText(chart_id, name, nwin, time, price, text, Color, Font, Size, point):
    if ObjectFind(chart_id, name) == -1:
        CreateText(chart_id, name, nwin, time, price, text, Color, Font, Size, point)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time, price)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Morningflat(_MQL5Indicator):
    name = 'morningflat'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'BarsTotal': 500,
        'StartHour': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=0),
        'EndHour': _Choice({0: '00', 1: '01', 2: '02', 3: '03', 4: '04', 5: '05', 6: '06', 7: '07', 8: '08', 9: '09', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=8),
        'TargetLevel': 161.8,
    }

