"""XBarClearCloseTrend — converted from MQL5: MQL5 Indicators/XBarClearCloseTrend/XBarClearCloseTrend.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [32768], 2: [3329330], 3: [10025880], 4: [255], 5: [4678655], 6: [9234160]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Strongly up', 2: 'Up', 3: 'Uncertainly up', 4: 'Strongly down', 5: 'Down', 6: 'Uncertainly down'}, 'levels': [], 'description': [], 'name': 'XBarClearCloseTrend', 'source': 'MQL5 Indicators/XBarClearCloseTrend/XBarClearCloseTrend.mq5', 'folder': 'XBarClearCloseTrend', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 5, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 32768  # #property indicator_color1
indicator_color2 = 3329330  # #property indicator_color2
indicator_color3 = 10025880  # #property indicator_color3
indicator_color4 = 255  # #property indicator_color4
indicator_color5 = 4678655  # #property indicator_color5
indicator_color6 = 9234160  # #property indicator_color6

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 5)  # Period
BufferArr0 = Arr(0, 0.0)
BufferArr1 = Arr(0, 0.0)
BufferArr2 = Arr(0, 0.0)
BufferArr3 = Arr(0, 0.0)
BufferArr4 = Arr(0, 0.0)
BufferArr5 = Arr(0, 0.0)
BufferTrend = Arr(0, 0.0)
prefix = ""
period = 0
wnd = 0

def OnInit():
    global period, prefix, wnd
    period = (1 if (InpPeriod < 1) else InpPeriod)
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    SizeByScale()
    Descriptions()
    SetIndexBuffer(0, BufferArr0, INDICATOR_DATA)
    SetIndexBuffer(1, BufferArr1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferArr2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferArr3, INDICATOR_DATA)
    SetIndexBuffer(4, BufferArr4, INDICATOR_DATA)
    SetIndexBuffer(5, BufferArr5, INDICATOR_DATA)
    SetIndexBuffer(6, BufferTrend, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XBarClearCloseTrend(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    for i in range(0, 6):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    ArraySetAsSeries(BufferArr0, True)
    ArraySetAsSeries(BufferArr1, True)
    ArraySetAsSeries(BufferArr2, True)
    ArraySetAsSeries(BufferArr3, True)
    ArraySetAsSeries(BufferArr4, True)
    ArraySetAsSeries(BufferArr5, True)
    ArraySetAsSeries(BufferTrend, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferArr0, EMPTY_VALUE)
        ArrayInitialize(BufferArr1, EMPTY_VALUE)
        ArrayInitialize(BufferArr2, EMPTY_VALUE)
        ArrayInitialize(BufferArr3, EMPTY_VALUE)
        ArrayInitialize(BufferArr4, EMPTY_VALUE)
        ArrayInitialize(BufferArr5, EMPTY_VALUE)
        ArrayInitialize(BufferTrend, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferTrend[i] = BufferTrend[i + 1]
        BufferArr0[i] = EMPTY_VALUE
        BufferArr1[i] = EMPTY_VALUE
        BufferArr2[i] = EMPTY_VALUE
        BufferArr3[i] = EMPTY_VALUE
        BufferArr4[i] = EMPTY_VALUE
        BufferArr5[i] = EMPTY_VALUE
        if BufferTrend[i + 1] == 1:
            if IsBarUp(high, close, i):
                BufferArr0[i] = 1.0
            else:
                if IsBarDn(low, close, i):
                    BufferArr3[i] = 1.0
                else:
                    if close[i] >= close[i + 1]:
                        BufferArr1[i] = 1.0
                        BufferTrend[i] = -1.0
                    else:
                        BufferArr2[i] = 1.0
        else:
            if IsBarDn(low, close, i):
                BufferArr3[i] = 1.0
            else:
                if IsBarUp(high, close, i):
                    BufferArr0[i] = 1.0
                    BufferTrend[i] = 1.0
                else:
                    if close[i] <= close[i + 1]:
                        BufferArr4[i] = 1.0
                    else:
                        BufferArr5[i] = 1.0
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        for i in range(0, 6):
            PlotIndexSetInteger(i, PLOT_LINE_WIDTH, SizeByScale())
        Descriptions()
        ChartRedraw()

def SizeByScale():
    scale = _uchar(ChartGetInteger(0, CHART_SCALE))
    size = (1 if (scale < 3) else 2 if (scale == 3) else 5 if (scale == 4) else 8)
    return size

def IsBarUp(high, close, index):
    for i in range(1, period):
        if high[index + i] >= close[index]:
            return False
    return True

def IsBarDn(low, close, index):
    for i in range(1, period):
        if low[index + i] <= close[index]:
            return False
    return True

def Descriptions():
    x = 4
    y = 1
    arr_colors = Arr.of([_int(indicator_color1), _int(indicator_color2), _int(indicator_color3), _int(indicator_color4), _int(indicator_color5), _int(indicator_color6)], fill=0)
    arr_texts = Arr.of(['Strongly up', 'Up', 'Uncertainly up', 'Strongly down', 'Down', 'Uncertainly down'], fill="")
    arr_names = Arr(6, "", dyn=False)
    for i in range(0, 6):
        arr_names[i] = prefix + 'label' + _str(i)
        arr_colors[i] = PlotIndexGetInteger(i, PLOT_LINE_COLOR)
        x = (x if (i == 0) else 80 if (i == 1) else 110 if (i == 2) else 210 if (i == 3) else 300 if (i == 4) else 346)
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


class XBarClearCloseTrend(_MQL5Indicator):
    name = 'XBarClearCloseTrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 5,  # Period
    }

