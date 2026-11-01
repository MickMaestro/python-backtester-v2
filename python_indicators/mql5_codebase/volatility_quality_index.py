"""Volatility_Quality_Index — converted from MQL5: MQL5 Indicators/Volatility_Quality_Index/Volatility_Quality_Index.mq5

Volatility Quality Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'VQI Up', 2: 'VQI Down'}, 'levels': [], 'description': ['Volatility Quality Index indicator'], 'name': 'Volatility_Quality_Index', 'source': 'MQL5 Indicators/Volatility_Quality_Index/Volatility_Quality_Index.mq5', 'folder': 'Volatility_Quality_Index', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 7, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpSmoothing', 'py': 'InpSmoothing', 'param': 'InpSmoothing', 'type': 'uint', 'default': 1, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpFilter', 'py': 'InpFilter', 'param': 'InpFilter', 'type': 'uint', 'default': 5, 'label': 'Filter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 32768  # #property indicator_color1
indicator_color2 = 255  # #property indicator_color2

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 7)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpSmoothing = _input('InpSmoothing', 1)  # Smoothing
InpFilter = _input('InpFilter', 5)  # Filter
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferVQ = Arr(0, 0.0)
BufferMAO = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
BufferMAC = Arr(0, 0.0)
prefix = ""
wnd = 0
period = 0
period_sm = 0
filter_ = 0
handle_maO = 0
handle_maH = 0
handle_maL = 0
handle_maC = 0

def OnInit():
    global filter_, handle_maC, handle_maH, handle_maL, handle_maO, period, period_sm, prefix, wnd
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    period = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (1 if (InpSmoothing < 1) else InpSmoothing)
    filter_ = _int(InpFilter)
    SizeByScale()
    Descriptions()
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferVQ, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMAL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferMAC, INDICATOR_CALCULATIONS)
    for i in range(0, 2):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility Quality Index (' + _str(period) + ',' + _str(period_sm) + ',' + _str(filter_) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferVQ, True)
    ArraySetAsSeries(BufferMAO, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ArraySetAsSeries(BufferMAC, True)
    ResetLastError()
    handle_maO = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_OPEN)
    if handle_maO == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_OPEN object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maH = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_HIGH)
    if handle_maH == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maL = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_LOW)
    if handle_maL == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maC = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_CLOSE)
    if handle_maC == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_CLOSE object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_sm, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_sm - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferVQ, 0)
        ArrayInitialize(BufferMAO, 0)
        ArrayInitialize(BufferMAH, 0)
        ArrayInitialize(BufferMAL, 0)
        ArrayInitialize(BufferMAC, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_maO, 0, 0, count, BufferMAO)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maH, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maL, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maC, 0, 0, count, BufferMAC)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        o = BufferMAO[i]
        h = BufferMAH[i]
        l = BufferMAL[i]
        c = BufferMAC[i]
        c2 = BufferMAC[i + period_sm]
        BufferUP[i] = EMPTY_VALUE
        BufferDN[i] = BufferUP[i]
        max_ = fmax(h - l, fmax(h - c2, c2 - l))
        if max_ != 0 and (h - l) != 0:
            VQnew = fabs((_fdiv(c - c2, max_) + _fdiv(c - o, h - l)) * 0.5) * ((c - c2 + (c - o)) * 0.5)
            BufferVQ[i] = (BufferVQ[i + 1] if (fabs(VQnew) < (filter_ * Point())) else VQnew)
            if BufferVQ[i] > 0:
                BufferUP[i] = 0.5
                BufferDN[i] = EMPTY_VALUE
            else:
                BufferDN[i] = 0.5
                BufferUP[i] = EMPTY_VALUE
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        for i in range(0, 2):
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
    arr_colors = Arr.of([_int(indicator_color1), _int(indicator_color2)], fill=0)
    arr_texts = Arr.of(['Up direction', 'Down direction'], fill="")
    arr_names = Arr(2, "", dyn=False)
    for i in range(0, 2):
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


class VolatilityQualityIndex(_MQL5Indicator):
    name = 'Volatility_Quality_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 7,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpSmoothing': 1,  # Smoothing
        'InpFilter': 5,  # Filter
    }

