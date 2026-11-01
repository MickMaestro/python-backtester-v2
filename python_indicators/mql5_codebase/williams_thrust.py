"""Williams_Thrust — converted from MQL5: MQL5 Indicators/Williams_Thrust/Williams_Thrust.mq5

Williams Thrust indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [16711680], 2: [255], 3: [12632256]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'WT Up', 2: 'WT Down', 3: 'WT Neutral'}, 'levels': [], 'description': ['Williams Thrust indicator'], 'name': 'Williams_Thrust', 'source': 'MQL5 Indicators/Williams_Thrust/Williams_Thrust.mq5', 'folder': 'Williams_Thrust', 'inputs': [{'mql': 'InpPeriodLW1', 'py': 'InpPeriodLW1', 'param': 'InpPeriodLW1', 'type': 'uint', 'default': 250, 'label': 'First WPR period', 'sinput': False}, {'mql': 'InpPeriodMA1', 'py': 'InpPeriodMA1', 'param': 'InpPeriodMA1', 'type': 'uint', 'default': 50, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpPeriodLW2', 'py': 'InpPeriodLW2', 'param': 'InpPeriodLW2', 'type': 'uint', 'default': 50, 'label': 'Second WPR period', 'sinput': False}, {'mql': 'InpPeriodMA2', 'py': 'InpPeriodMA2', 'param': 'InpPeriodMA2', 'type': 'uint', 'default': 10, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

indicator_color1 = 16711680  # #property indicator_color1
indicator_color2 = 255  # #property indicator_color2
indicator_color3 = 12632256  # #property indicator_color3

# ---- inputs and global variables
InpPeriodLW1 = _input('InpPeriodLW1', 250)  # First WPR period
InpPeriodMA1 = _input('InpPeriodMA1', 50)  # First MA period
InpPeriodLW2 = _input('InpPeriodLW2', 50)  # Second WPR period
InpPeriodMA2 = _input('InpPeriodMA2', 10)  # Second MA period
InpMethod = _input('InpMethod', MODE_EMA)  # MA method
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferWPR1 = Arr(0, 0.0)
BufferWPR2 = Arr(0, 0.0)
BufferAvgWPR1 = Arr(0, 0.0)
BufferAvgWPR2 = Arr(0, 0.0)
prefix = ""
period_lw1 = 0
period_ma1 = 0
period_lw2 = 0
period_ma2 = 0
period_max = 0
handle_wpr1 = 0
handle_wpr2 = 0
weight_sum1 = 0
weight_sum2 = 0
wnd = 0

def OnInit():
    global handle_wpr1, handle_wpr2, period_lw1, period_lw2, period_ma1, period_ma2, prefix, wnd
    period_lw1 = (1 if (InpPeriodLW1 < 1) else InpPeriodLW1)
    period_ma1 = (2 if (InpPeriodMA1 < 2) else InpPeriodMA1)
    period_lw2 = (1 if (InpPeriodLW2 < 1) else InpPeriodLW2)
    period_ma2 = (2 if (InpPeriodMA2 < 2) else InpPeriodMA2)
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    SizeByScale()
    Descriptions()
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferWPR1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferWPR2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAvgWPR1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgWPR2, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Williams Thrust (' + _str(period_lw1) + ',' + _str(period_ma1) + ',' + _str(period_lw2) + ',' + _str(period_ma2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferWPR1, True)
    ArraySetAsSeries(BufferWPR2, True)
    ArraySetAsSeries(BufferAvgWPR1, True)
    ArraySetAsSeries(BufferAvgWPR2, True)
    ResetLastError()
    handle_wpr1 = iWPR(None, PERIOD_CURRENT, period_lw1)
    if handle_wpr1 == INVALID_HANDLE:
        Print('The iWPR(', _str(period_lw1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_wpr2 = iWPR(None, PERIOD_CURRENT, period_lw2)
    if handle_wpr2 == INVALID_HANDLE:
        Print('The iWPR(', _str(period_lw2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
        ArrayInitialize(BufferWPR1, 0)
        ArrayInitialize(BufferWPR2, 0)
        ArrayInitialize(BufferAvgWPR1, 0)
        ArrayInitialize(BufferAvgWPR2, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_wpr1, 0, 0, count, BufferWPR1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_wpr2, 0, 0, count, BufferWPR2)
    if copied != count:
        return 0
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_lw1, period_ma1, BufferWPR1, BufferAvgWPR1) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_lw1, period_ma2, BufferWPR1, BufferAvgWPR2) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_lw1, period_ma1, BufferWPR1, BufferAvgWPR1) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_lw1, period_ma2, BufferWPR1, BufferAvgWPR2) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_lw1, period_ma1, BufferWPR1, BufferAvgWPR1, _GlobRef(globals(), 'weight_sum1')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_lw1, period_ma2, BufferWPR1, BufferAvgWPR2, _GlobRef(globals(), 'weight_sum2')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_lw1, period_ma1, BufferWPR1, BufferAvgWPR1) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_lw1, period_ma2, BufferWPR1, BufferAvgWPR2) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferNL[i] = EMPTY_VALUE
        BufferDN[i] = BufferNL[i]
        BufferUP[i] = BufferDN[i]
        if BufferWPR1[i] > BufferAvgWPR1[i] and BufferWPR2[i] > BufferAvgWPR2[i]:
            BufferUP[i] = 0.5
        else:
            if BufferWPR1[i] < BufferAvgWPR1[i] and BufferWPR2[i] < BufferAvgWPR2[i]:
                BufferDN[i] = 0.5
            else:
                BufferNL[i] = 0.5
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        for i in range(0, 3):
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
    arr_colors = Arr.of([_int(indicator_color1), _int(indicator_color2), _int(indicator_color3)], fill=0)
    arr_texts = Arr.of(['Up direction', 'Down direction', 'Neutral'], fill="")
    arr_names = Arr(3, "", dyn=False)
    for i in range(0, 3):
        arr_names[i] = prefix + 'label' + _str(i)
        arr_colors[i] = PlotIndexGetInteger(i, PLOT_LINE_COLOR)
        x = (x if (i == 0) else 110 if (i == 1) else 230)
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


class WilliamsThrust(_MQL5Indicator):
    name = 'Williams_Thrust'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodLW1': 250,  # First WPR period
        'InpPeriodMA1': 50,  # First MA period
        'InpPeriodLW2': 50,  # Second WPR period
        'InpPeriodMA2': 10,  # Second MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA method
    }

