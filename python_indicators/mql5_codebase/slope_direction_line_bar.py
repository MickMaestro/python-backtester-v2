"""Slope_Direction_Line_Bar — converted from MQL5: MQL5 Indicators/Slope_Direction_Line_Bar/Slope_Direction_Line_Bar.mq5

Slope Direction Line / Moving Average confirmation bars indicator
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

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [32768], 2: [255], 3: [14474460]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Up', 2: 'Down', 3: 'Neutral'}, 'levels': [], 'description': ['Slope Direction Line / Moving Average confirmation bars indicator'], 'name': 'Slope_Direction_Line_Bar', 'source': 'MQL5 Indicators/Slope_Direction_Line_Bar/Slope_Direction_Line_Bar.mq5', 'folder': 'Slope_Direction_Line_Bar', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 50, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethodMA', 'py': 'InpMethodMA', 'param': 'InpMethodMA', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPriceMA', 'py': 'InpAppliedPriceMA', 'param': 'InpAppliedPriceMA', 'type': 'int', 'default': 1, 'label': 'MA applied price', 'sinput': False}, {'mql': 'InpPeriodSlope', 'py': 'InpPeriodSlope', 'param': 'InpPeriodSlope', 'type': 'uint', 'default': 50, 'label': 'Slope period', 'sinput': False}, {'mql': 'InpMethodSlope', 'py': 'InpMethodSlope', 'param': 'InpMethodSlope', 'type': 'int', 'default': 0, 'label': 'Slope method', 'sinput': False}, {'mql': 'InpAppliedPriceSlope', 'py': 'InpAppliedPriceSlope', 'param': 'InpAppliedPriceSlope', 'type': 'int', 'default': 1, 'label': 'Slope applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

indicator_color1 = 32768  # #property indicator_color1
indicator_color2 = 255  # #property indicator_color2
indicator_color3 = 14474460  # #property indicator_color3

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 50)  # MA period
InpMethodMA = _input('InpMethodMA', MODE_SMA)  # MA method
InpAppliedPriceMA = _input('InpAppliedPriceMA', PRICE_CLOSE)  # MA applied price
InpPeriodSlope = _input('InpPeriodSlope', 50)  # Slope period
InpMethodSlope = _input('InpMethodSlope', MODE_SMA)  # Slope method
InpAppliedPriceSlope = _input('InpAppliedPriceSlope', PRICE_CLOSE)  # Slope applied price
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferSlope = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferVect = Arr(0, 0.0)
prefix = ""
wnd = 0
UpFr = 0
DnFr = 0
period_slope = 0
period_slope2 = 0
period_sqrt = 0
period_ma = 0
period_max = 0
weight_sum = 0
handle_ma = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_ma, handle_ma1, handle_ma2, period_ma, period_slope, period_slope2, period_sqrt, prefix, wnd
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    SizeByScale()
    Descriptions()
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_slope = (2 if (InpPeriodSlope < 2) else InpPeriodSlope)
    period_slope2 = _int(floor(_idiv(period_slope, 2)))
    period_sqrt = _int(floor(sqrt(period_slope)))
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSlope, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferVect, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Slope/MA bars (' + _str(period_slope) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferSlope, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferVect, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethodMA, InpAppliedPriceMA)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(None, PERIOD_CURRENT, period_slope, 0, InpMethodSlope, InpAppliedPriceSlope)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_slope), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, period_slope2, 0, InpMethodSlope, InpAppliedPriceSlope)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_slope2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_slope, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
        ArrayInitialize(BufferSlope, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferVect, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferMA2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferVect[i] = (2.0 * BufferMA2[i]) - BufferMA1[i]
    _sw1 = InpMethodSlope
    _k2 = 0 if _sw1 == MODE_EMA else 1 if _sw1 == MODE_SMMA else 2 if _sw1 == MODE_LWMA else 3
    try:
        if _k2 <= 0:
            if ExponentialMAOnBuffer(rates_total, prev_calculated, period_slope, period_sqrt, BufferVect, BufferSlope) == 0:
                return 0
        if _k2 <= 1:
            if SmoothedMAOnBuffer(rates_total, prev_calculated, period_slope, period_sqrt, BufferVect, BufferSlope) == 0:
                return 0
        if _k2 <= 2:
            if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_slope, period_sqrt, BufferVect, BufferSlope, _GlobRef(globals(), 'weight_sum')) == 0:
                return 0
        if _k2 <= 3:
            if SimpleMAOnBuffer(rates_total, prev_calculated, period_slope, period_sqrt, BufferVect, BufferSlope) == 0:
                return 0
    except _SwitchBreak:
        pass
    for i in range(limit, 0 - 1, -1):
        BufferUP[i] = EMPTY_VALUE
        BufferDN[i] = BufferUP[i]
        BufferNL[i] = 0.5
        if BufferSlope[i] > BufferSlope[i + 1]:
            if BufferMA[i] > BufferMA[i + 1]:
                BufferUP[i] = 0.5
                BufferNL[i] = EMPTY_VALUE
                BufferDN[i] = BufferNL[i]
        elif BufferSlope[i] < BufferSlope[i + 1]:
            if BufferMA[i] < BufferMA[i + 1]:
                BufferDN[i] = 0.5
                BufferNL[i] = EMPTY_VALUE
                BufferUP[i] = BufferNL[i]
        else:
            BufferNL[i] = 0.5
            BufferDN[i] = EMPTY_VALUE
            BufferUP[i] = BufferDN[i]
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


class SlopeDirectionLineBar(_MQL5Indicator):
    name = 'Slope_Direction_Line_Bar'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 50,  # MA period
        'InpMethodMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpAppliedPriceMA': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA applied price
        'InpPeriodSlope': 50,  # Slope period
        'InpMethodSlope': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Slope method
        'InpAppliedPriceSlope': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Slope applied price
    }

