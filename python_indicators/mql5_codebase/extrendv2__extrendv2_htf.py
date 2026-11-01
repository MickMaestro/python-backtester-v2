"""ExTrendV2 — converted from MQL5: MQL5 Indicators/ExTrendV2_HTF/ExTrendV2.mq5

Copyright: Copyright © 2006, Alex Sidd (Executer)k; Link: mailto:work_st@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alex Sidd (Executer)k', 'link': 'mailto:work_st@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [2263842, 11823615]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Up Line'}, 'levels': [0.0], 'description': [], 'name': 'ExTrendV2', 'source': 'MQL5 Indicators/ExTrendV2_HTF/ExTrendV2.mq5', 'folder': 'ExTrendV2_HTF', 'inputs': [{'mql': 'UpLineColor', 'py': 'UpLineColor', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'цвет тренда верхних фракталов', 'sinput': False}, {'mql': 'DnLineColor', 'py': 'DnLineColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'цвет тренда нижних фракталов', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpLineColor = _input('UpLineColor', clrTeal)  # цвет тренда верхних фракталов
DnLineColor = _input('DnLineColor', clrMagenta)  # цвет тренда нижних фракталов
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
Up_level_name = ""
Dn_level_name = ""
FractUp1 = 0.0
FractUp2 = 0.0
FractDn1 = 0.0
FractDn2 = 0.0
Res1 = 0.0
Res2 = 0.0
FTimeUp1 = 0
FTimeUp2 = 0
FTimeDn1 = 0
FTimeDn2 = 0
curTime = 0

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

def LevelCalculate(Price1, Time1, Price2, Time2, NewTime):
    if Time2 != Time1:
        return _fdiv((NewTime - Time1) * (Price2 - Price1), Time2 - Time1) + Price1
    return Price2

def isUpFract(High, index):
    if ((High[index + 3] > High[index + 2] and High[index + 3] > High[index + 4]) and High[index + 4] > High[index + 5]) and High[index + 2] > High[index + 1]:
        return High[index + 3]
    return 0.0

def isDnFract(Low, index):
    if ((Low[index + 3] < Low[index + 2] and Low[index + 3] < Low[index + 4]) and Low[index + 4] < Low[index + 5]) and Low[index + 2] < Low[index + 1]:
        return Low[index + 3]
    return 0.0

def OnInit():
    global Dn_level_name, FractDn1, FractDn2, FractUp1, FractUp2, Res1, Res2, Up_level_name, min_rates_total
    min_rates_total = 10
    FractUp1 = 0.0
    FractUp2 = 0.0
    FractDn1 = 0.0
    FractDn2 = 0.0
    Res1 = 240 * 60.0
    Res2 = _fdiv(1.0, Res1)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'ExTrend(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    Up_level_name = shortname.v + ' Up_level'
    Dn_level_name = shortname.v + ' Dn_level'
    if ObjectFind(0, Up_level_name) == -1:
        SetTline(0, Up_level_name, 0, 0, 0.0, 0, 0.0, UpLineColor, 0, 1, Up_level_name)
    if ObjectFind(0, Dn_level_name) == -1:
        SetTline(0, Dn_level_name, 0, 0, 0.0, 0, 0.0, DnLineColor, 0, 1, Dn_level_name)

def OnDeinit(reason):
    ObjectDelete(0, Up_level_name)
    ObjectDelete(0, Dn_level_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global FTimeDn1, FTimeDn2, FTimeUp1, FTimeUp2, FractDn1, FractDn2, FractUp1, FractUp2, _s_OnCalculate_negative_, _s_OnCalculate_positive_
    if rates_total < min_rates_total:
        return 0
    limit = 0
    Fup = 0.0
    Fdn = 0.0
    positive = 0.0
    negative = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        UpBuffer[limit + 1] = 1e-09
        DnBuffer[limit + 1] = 1e-09
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    positive = _s_OnCalculate_positive_
    negative = _s_OnCalculate_negative_
    for bar in range(limit, 0 - 1, -1):
        negative = 0.0
        positive = 0.0
        Fup = isUpFract(high, bar)
        Fdn = isDnFract(low, bar)
        if Fup:
            if (not FractUp1) and (not FractUp2):
                FractUp1 = Fup
                FTimeUp1 = time[bar + 3]
            if (FractUp1 and (not FractUp2)) and FTimeUp1 != time[bar + 3]:
                FractUp2 = Fup
                FTimeUp2 = time[bar + 3]
            if (FractUp1 and FractUp2) and FTimeUp2 != time[bar + 3]:
                FractUp1 = FractUp2
                FTimeUp1 = FTimeUp2
                FractUp2 = Fup
                FTimeUp2 = time[bar + 3]
        if Fdn:
            if (not FractDn1) and (not FractDn2):
                FractDn1 = Fdn
                FTimeDn1 = time[bar + 3]
            if (FractDn1 and (not FractDn2)) and FTimeDn1 != time[bar + 3]:
                FractDn2 = Fdn
                FTimeDn2 = time[bar + 3]
            if (FractDn1 and FractDn2) and FTimeDn2 != time[bar + 3]:
                FractDn1 = FractDn2
                FTimeDn1 = FTimeDn2
                FractDn2 = Fdn
                FTimeDn2 = time[bar + 3]
        if FractUp1 and FractUp2:
            SetTline(0, Up_level_name, 0, FTimeUp1, FractUp1, FTimeUp2, FractUp2, UpLineColor, 0, 1, Up_level_name)
            y = _fdiv(FTimeUp2 - FTimeUp1, Res1)
            x = (FractUp2 - FractUp1) * 240.0
            if not y:
                y = Res2
            positive = MathArctan(_fdiv(x, y))
        if FractDn1 and FractDn2:
            SetTline(0, Dn_level_name, 0, FTimeDn1, FractDn1, FTimeDn2, FractDn2, DnLineColor, 0, 1, Dn_level_name)
            y = _fdiv(FTimeDn2 - FTimeDn1, Res1)
            x = (FractDn2 - FractDn1) * 240.0
            if not y:
                y = Res2
            negative = MathArctan(_fdiv(x, y))
        UpBuffer[bar] = positive
        DnBuffer[bar] = negative
        if bar == 1:
            _s_OnCalculate_positive_ = positive
            _s_OnCalculate_negative_ = negative
    return rates_total

# ---- static local variables
_s_OnCalculate_positive_ = 0.0
_s_OnCalculate_negative_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExTrendV2(_MQL5Indicator):
    name = 'ExTrendV2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

