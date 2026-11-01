"""extrend — converted from MQL5: MQL5 Indicators/ExTrend/extrend.mq5

Copyright: Copyright © 2006, Alex Sidd (Executer)k; Link: mailto:work_st@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alex Sidd (Executer)k', 'link': 'mailto:work_st@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [65280], 2: [16711935]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up Line', 2: 'Down Line'}, 'levels': [0.0], 'description': [], 'name': 'extrend', 'source': 'MQL5 Indicators/ExTrend/extrend.mq5', 'folder': 'ExTrend', 'inputs': [{'mql': 'UpLineColor', 'py': 'UpLineColor', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'upper fractals trend color', 'sinput': False}, {'mql': 'DnLineColor', 'py': 'DnLineColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'lower fractals trend color', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpLineColor = _input('UpLineColor', clrTeal)  # upper fractals trend color
DnLineColor = _input('DnLineColor', clrMagenta)  # lower fractals trend color
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
FRA_Handle = 0
min_rates_total = 0
Up_level_name = ""
Dn_level_name = ""
FractUp1 = 0.0
FractUp2 = 0.0
FractDn1 = 0.0
FractDn2 = 0.0
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

def OnInit():
    global Dn_level_name, FRA_Handle, FractDn1, FractDn2, FractUp1, FractUp2, Up_level_name, min_rates_total
    min_rates_total = 10
    FractUp1 = 0.0
    FractUp2 = 0.0
    FractDn1 = 0.0
    FractDn2 = 0.0
    FRA_Handle = iFractals(None, 0)
    if FRA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFractals')
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnBuffer, True)
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
    global FTimeDn1, FTimeDn2, FTimeUp1, FTimeUp2, FractDn1, FractDn2, FractUp1, FractUp2
    if BarsCalculated(FRA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    UpFr = Arr(0, 0.0)
    DnFr = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - min_rates_total - 1
    else:
        to_copy = rates_total - prev_calculated + 6
        limit = rates_total - prev_calculated + 2
    if CopyBuffer(FRA_Handle, 0, 0, to_copy, UpFr) <= 0:
        return 0
    if CopyBuffer(FRA_Handle, 1, 0, to_copy, DnFr) <= 0:
        return 0
    ArraySetAsSeries(UpFr, True)
    ArraySetAsSeries(DnFr, True)
    ArraySetAsSeries(time, True)
    for bar in range(2, 0 - 1, -1):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
    for bar in range(limit, 0 - 1, -1):
        negative = 0.0
        positive = 0.0
        Fup = UpFr[bar + 3]
        Fdn = DnFr[bar + 3]
        if Fup and Fup != EMPTY_VALUE:
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
        if Fdn and Fdn != EMPTY_VALUE:
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
            y = _fdiv(FTimeUp2 - FTimeUp1, 240 * 60.0)
            x = (FractUp2 - FractUp1) * 240.0
            if not y:
                y = _fdiv(1, 240 * 60.0)
            positive = MathArctan(_fdiv(x, y))
        if FractDn1 and FractDn2:
            SetTline(0, Dn_level_name, 0, FTimeDn1, FractDn1, FTimeDn2, FractDn2, DnLineColor, 0, 1, Dn_level_name)
            a = _fdiv(FTimeDn2 - FTimeDn1, 240 * 60.0)
            b = (FractDn2 - FractDn1) * 240.0
            if not a:
                a = _fdiv(1, 240 * 60.0)
            negative = MathArctan(_fdiv(b, a))
        UpBuffer[bar + 3] = positive
        DnBuffer[bar + 3] = negative
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Extrend(_MQL5Indicator):
    name = 'extrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

