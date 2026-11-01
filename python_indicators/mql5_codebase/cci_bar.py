"""CCI_Bar — converted from MQL5: MQL5 Indicators/CCI_Bar/CCI_Bar.mq5

CCI Bar indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [16748574], 2: [36095], 3: [32768], 4: [3937500], 5: [14474460]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Up', 2: 'Down', 3: 'Crossing Oversold', 4: 'Crossing Overbought', 5: 'Neutral'}, 'levels': [], 'description': ['CCI Bar indicator'], 'name': 'CCI_Bar', 'source': 'MQL5 Indicators/CCI_Bar/CCI_Bar.mq5', 'folder': 'CCI_Bar', 'inputs': [{'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 45, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 150.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -150.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpLevEntryB', 'py': 'InpLevEntryB', 'param': 'InpLevEntryB', 'type': 'double', 'default': -150.0, 'label': 'Buy entry level', 'sinput': False}, {'mql': 'InpLevEntryS', 'py': 'InpLevEntryS', 'param': 'InpLevEntryS', 'type': 'double', 'default': 150.0, 'label': 'Sell entry level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 16748574  # #property indicator_color1
indicator_color2 = 36095  # #property indicator_color2
indicator_color3 = 32768  # #property indicator_color3
indicator_color4 = 3937500  # #property indicator_color4
indicator_color5 = 14474460  # #property indicator_color5

# ---- inputs and global variables
InpPeriodCCI = _input('InpPeriodCCI', 45)  # CCI period
InpOverbought = _input('InpOverbought', 150.0)  # Overbought
InpOversold = _input('InpOversold', -150.0)  # Oversold
InpLevEntryB = _input('InpLevEntryB', -150.0)  # Buy entry level
InpLevEntryS = _input('InpLevEntryS', 150.0)  # Sell entry level
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferCrossOS = Arr(0, 0.0)
BufferCrossOB = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
prefix = ""
wnd = 0
levB = 0.0
levS = 0.0
overbought = 0.0
oversold = 0.0
period_cci = 0
handle_cci = 0

def OnInit():
    global handle_cci, levB, levS, overbought, oversold, period_cci, prefix, wnd
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    overbought = (0.1 if (fabs(InpOverbought) < 0.1) else fabs(InpOverbought))
    oversold = (-0.1 if ((-fabs(InpOversold)) > -0.1) else (-fabs(InpOversold)))
    levB = (overbought if (InpLevEntryB > overbought) else InpLevEntryB)
    levS = (oversold if (InpLevEntryS < oversold) else InpLevEntryS)
    SizeByScale()
    Descriptions()
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCrossOS, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCrossOB, INDICATOR_DATA)
    SetIndexBuffer(4, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCCI, INDICATOR_CALCULATIONS)
    for i in range(0, 5):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI Bar (' + _str(period_cci) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferCrossOS, True)
    ArraySetAsSeries(BufferCrossOB, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferCCI, True)
    ResetLastError()
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
        ArrayInitialize(BufferCrossOS, EMPTY_VALUE)
        ArrayInitialize(BufferCrossOB, EMPTY_VALUE)
        ArrayInitialize(BufferCCI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        cci0 = BufferCCI[i]
        cci1 = BufferCCI[i + 1]
        BufferCrossOB[i] = EMPTY_VALUE
        BufferCrossOS[i] = BufferCrossOB[i]
        BufferDN[i] = BufferCrossOS[i]
        BufferUP[i] = BufferDN[i]
        BufferNL[i] = 0.5
        crossing = False
        if cci0 > oversold and cci1 <= oversold:
            BufferCrossOS[i] = 0.5
            BufferCrossOB[i] = EMPTY_VALUE
            BufferDN[i] = BufferCrossOB[i]
            BufferUP[i] = BufferDN[i]
            BufferNL[i] = BufferUP[i]
            crossing = True
        if cci0 < overbought and cci1 >= overbought:
            BufferCrossOB[i] = 0.5
            BufferCrossOS[i] = EMPTY_VALUE
            BufferDN[i] = BufferCrossOS[i]
            BufferUP[i] = BufferDN[i]
            BufferNL[i] = BufferUP[i]
            crossing = True
        if not crossing:
            if cci0 > levB and cci0 >= cci1:
                BufferUP[i] = 0.5
                BufferCrossOS[i] = EMPTY_VALUE
                BufferCrossOB[i] = BufferCrossOS[i]
                BufferDN[i] = BufferCrossOB[i]
                BufferNL[i] = BufferDN[i]
            elif cci0 < levS and cci0 <= cci1:
                BufferDN[i] = 0.5
                BufferCrossOS[i] = EMPTY_VALUE
                BufferCrossOB[i] = BufferCrossOS[i]
                BufferUP[i] = BufferCrossOB[i]
                BufferNL[i] = BufferUP[i]
            else:
                BufferNL[i] = 0.5
                BufferCrossOS[i] = EMPTY_VALUE
                BufferCrossOB[i] = BufferCrossOS[i]
                BufferUP[i] = BufferCrossOB[i]
                BufferDN[i] = BufferUP[i]
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        for i in range(0, 5):
            PlotIndexSetInteger(i, PLOT_LINE_WIDTH, SizeByScale())
        Descriptions()
        ChartRedraw()

def SizeByScale():
    scale = _uchar(ChartGetInteger(0, CHART_SCALE))
    size = (1 if (scale < 3) else 2 if (scale == 3) else 5 if (scale == 4) else 8)
    return size

def Descriptions():
    x = 4
    y = 1
    arr_colors = Arr.of([_int(indicator_color1), _int(indicator_color2), _int(indicator_color3), _int(indicator_color4), _int(indicator_color5)], fill=0)
    arr_texts = Arr.of(['Up direction', 'Down direction', 'Crossing to up', 'Crossing to down', 'Neutral'], fill="")
    arr_names = Arr(5, "", dyn=False)
    for i in range(0, 5):
        arr_names[i] = prefix + 'label' + _str(i)
        arr_colors[i] = PlotIndexGetInteger(i, PLOT_LINE_COLOR)
        shift = (i * (90 if (i < 2) else 96 if (i < (5 - 1)) else 100)) - (x if (i > 0) else 0)
        x += shift
        Label(arr_names[i], x, y, CharToString(167), 16, arr_colors[i], 'Wingdings')
        Label(arr_names[i] + '_txt', x + 10, y + 5, arr_texts[i], 10, clrGray, 'Calibri')

def Label(name, x, y, text, size, clr, font):
    if ObjectFind(0, name) != wnd:
        ObjectCreate(0, name, OBJ_LABEL, wnd, 0, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, ANCHOR_LEFT_LOWER)
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, size)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetString(0, name, OBJPROP_FONT, font)
    ObjectSetString(0, name, OBJPROP_TEXT, text)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, '\n')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CCIBar(_MQL5Indicator):
    name = 'CCI_Bar'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodCCI': 45,  # CCI period
        'InpOverbought': 150.0,  # Overbought
        'InpOversold': -150.0,  # Oversold
        'InpLevEntryB': -150.0,  # Buy entry level
        'InpLevEntryS': 150.0,  # Sell entry level
    }

