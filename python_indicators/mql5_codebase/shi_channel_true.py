"""shi_channel_true — converted from MQL5: MQL5 Indicators/SHI Channel true (NB-channel)/shi_channel_true.mq5

Copyright: Copyright © 2004, Shurka & Kevin; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, Shurka & Kevin', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SHI Channel true'}, 'levels': [], 'description': [], 'name': 'shi_channel_true', 'source': 'MQL5 Indicators/SHI Channel true (NB-channel)/shi_channel_true.mq5', 'folder': 'SHI Channel true (NB-channel)', 'inputs': [{'mql': 'AllBars', 'py': 'AllBars', 'param': 'AllBars', 'type': 'int', 'default': 240, 'label': '', 'sinput': False}, {'mql': 'BarsForFract', 'py': 'BarsForFract', 'param': 'BarsForFract', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'UpChannelColor', 'py': 'UpChannelColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MdChannelColor', 'py': 'MdChannelColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'DnChannelColor', 'py': 'DnChannelColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
AllBars = _input('AllBars', 240)
BarsForFract = _input('BarsForFract', 0)
ExtBuffer = Arr(0, 0.0)
count = 0
BFF = 0
StartBars = 0

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

def OnInit():
    global BFF, StartBars, count
    if BarsForFract > 0:
        BFF = BarsForFract
    else:
        _sw1 = Period()
        if _sw1 == PERIOD_M1:
            BFF = 12
        elif _sw1 == PERIOD_M2:
            BFF = 24
        elif _sw1 == PERIOD_M3:
            BFF = 36
        elif _sw1 == PERIOD_M4:
            BFF = 40
        elif _sw1 == PERIOD_M5:
            BFF = 48
        elif _sw1 == PERIOD_M6:
            BFF = 12
        elif _sw1 == PERIOD_M10:
            BFF = 15
        elif _sw1 == PERIOD_M12:
            BFF = 20
        elif _sw1 == PERIOD_M15:
            BFF = 24
        elif _sw1 == PERIOD_M20:
            BFF = 24
        elif _sw1 == PERIOD_M30:
            BFF = 24
        elif _sw1 == PERIOD_H1:
            BFF = 12
        elif _sw1 == PERIOD_H2:
            BFF = 12
        elif _sw1 == PERIOD_H3:
            BFF = 12
        elif _sw1 == PERIOD_H4:
            BFF = 15
        elif _sw1 == PERIOD_H6:
            BFF = 12
        elif _sw1 == PERIOD_H8:
            BFF = 12
        elif _sw1 == PERIOD_H12:
            BFF = 12
        elif _sw1 == PERIOD_D1:
            BFF = 10
        elif _sw1 == PERIOD_W1:
            BFF = 6
        elif _sw1 == PERIOD_MN1:
            BFF = 6
    count = (BFF * 2) + 1
    StartBars = MathMax(BFF - 1, AllBars)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    ArraySetAsSeries(ExtBuffer, True)
    shortname = 'SHI Channel true'
    PlotIndexSetString(0, PLOT_LABEL, shortname)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def DelObj():
    ObjectDelete(0, 'Upper SHI')
    ObjectDelete(0, 'Lower SHI')
    ObjectDelete(0, 'Middle SHI')
    Comment('')

def OnDeinit(reason):
    DelObj()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    Step = 0.0
    iprice = 0.0
    P1 = 0.0
    P2 = 0.0
    PP = 0.0
    nbar = 0
    bar = 0
    B1 = 0
    B2 = 0
    UpDown = 0
    ishift = 0
    i = 0
    AB = 0
    T1 = 0
    T2 = 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArrayInitialize(ExtBuffer, 0.0)
    if AllBars == 0 or rates_total < AllBars:
        AB = rates_total
    else:
        AB = AllBars
    bar = 2
    B1 = -1
    B2 = -1
    UpDown = 0
    while (B1 == -1 or B2 == -1) and bar < AB:
        ExtBuffer[bar] = 0.0
        nbar = bar - BFF
        if nbar < 0:
            nbar = 0
        if UpDown < 1 and bar == ArrayMinimum(low, nbar, count):
            if UpDown == 0:
                UpDown = -1
                B1 = bar
                P1 = low[B1]
            else:
                B2 = bar
                P2 = low[B2]
        if UpDown > -1 and bar == ArrayMaximum(high, nbar, count):
            if UpDown == 0:
                UpDown = 1
                B1 = bar
                P1 = high[B1]
            else:
                B2 = bar
                P2 = high[B2]
        bar += 1
    if B1 == -1 or B2 == -1:
        DelObj()
        return 0
    Step = _fdiv(P2 - P1, B2 - B1)
    P1 = P1 - (B1 * Step)
    B1 = 0
    ishift = 0
    iprice = 0.0
    if UpDown == 1:
        PP = low[2] - (2 * Step)
        i = 3
        for i in range(i, B2 + 1):
            if low[i] < (PP + (Step * i)):
                PP = low[i] - (i * Step)
        else:
            i = _range_end(i, B2 + 1, 1)
        if low[0] < PP:
            ishift = 0
            iprice = PP
        if low[1] < (PP + Step):
            ishift = 1
            iprice = PP + Step
        if high[0] > P1:
            ishift = 0
            iprice = P1
        if low[1] > (P1 + Step):
            ishift = 1
            iprice = P1 + Step
    else:
        PP = high[2] - (2 * Step)
        i = 3
        for i in range(i, B2 + 1):
            if high[i] > (PP + (Step * i)):
                PP = high[i] - (i * Step)
        else:
            i = _range_end(i, B2 + 1, 1)
        if low[0] < P1:
            ishift = 0
            iprice = P1
        if low[1] < (P1 + Step):
            ishift = 1
            iprice = P1 + Step
        if high[0] > PP:
            ishift = 0
            iprice = PP
        if high[1] > (PP + Step):
            ishift = 1
            iprice = PP + Step
    P2 = P1 + (AB * Step)
    T1 = time[B1]
    T2 = time[AB]
    if iprice != 0:
        ExtBuffer[ishift] = iprice
    else:
        ExtBuffer[ishift] = 0.0
    SetTline(0, 'Upper SHI', 0, T2, PP + (Step * AB), T1, PP, UpChannelColor, STYLE_SOLID, 2, 'Upper SHI')
    SetTline(0, 'Lower SHI', 0, T2, P2, T1, P1, DnChannelColor, STYLE_SOLID, 2, 'Lower SHI')
    SetTline(0, 'Middle SHI', 0, T2, (P2 + PP + (Step * AB)) / 2, T1, (P1 + PP) / 2, MdChannelColor, STYLE_DOT, 1, 'Middle SHI')
    Comment(' Channel size = ', DoubleToString(_fdiv(MathAbs(PP - P1), Point()), 0), ' Slope = ', DoubleToString(_fdiv(-Step, Point()), 2))
    return rates_total

# ---- global variables initialised from expressions
UpChannelColor = _input('UpChannelColor', _uint(Lime))
MdChannelColor = _input('MdChannelColor', _uint(Blue))
DnChannelColor = _input('DnChannelColor', _uint(Red))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ShiChannelTrue(_MQL5Indicator):
    name = 'shi_channel_true'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AllBars': 240,
        'BarsForFract': 0,
    }

