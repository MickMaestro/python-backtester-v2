"""Vortex_Trend — converted from MQL5: MQL5 Indicators/Vortex_Trend/Vortex_Trend.mq5

Vortex Trend
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [32768], 2: [255], 3: [14474460]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Up', 2: 'Down', 3: 'Neutral'}, 'levels': [], 'description': ['Vortex Trend'], 'name': 'Vortex_Trend', 'source': 'MQL5 Indicators/Vortex_Trend/Vortex_Trend.mq5', 'folder': 'Vortex_Trend', 'inputs': [{'mql': 'InpPeriodV', 'py': 'InpPeriodV', 'param': 'InpPeriodV', 'type': 'uint', 'default': 14, 'label': 'Vortex period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 110.0, 'label': 'Upper limit of the filtering range', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 90.0, 'label': 'Lower limit of the filtering range', 'sinput': False}, {'mql': 'InpUseSmooth', 'py': 'InpUseSmooth', 'param': 'InpUseSmooth', 'type': 'int', 'default': 1, 'label': 'Use Vortex smoothing', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 20, 'label': 'Smoothing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodV = _input('InpPeriodV', 14)  # Vortex period
InpOverbought = _input('InpOverbought', 110.0)  # Upper limit of the filtering range
InpOversold = _input('InpOversold', 90.0)  # Lower limit of the filtering range
InpUseSmooth = _input('InpUseSmooth', INPUT_YES)  # Use Vortex smoothing
InpPeriodMA = _input('InpPeriodMA', 20)  # Smoothing
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferVPos = Arr(0, 0.0)
BufferVNeg = Arr(0, 0.0)
BufferVHigh = Arr(0, 0.0)
BufferVLow = Arr(0, 0.0)
BufferMAUp = Arr(0, 0.0)
BufferMADn = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
prefix = ""
wnd = 0
overbought = 0.0
oversold = 0.0
period_v = 0
period_ma = 0
handle_atr = 0

def OnInit():
    global handle_atr, overbought, oversold, period_ma, period_v, prefix, wnd
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    SizeByScale()
    Descriptions()
    period_v = (1 if (InpPeriodV < 1) else InpPeriodV)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    overbought = (100.0 if (InpOverbought < 100.0) else InpOverbought)
    oversold = (100.0 if (InpOversold > 100.0) else InpOversold)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferVPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferVNeg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferVHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferVLow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMAUp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMADn, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferATR, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Vortex Trend (' + _str(period_v) + ',' + _str(period_ma) + ',' + _str(overbought) + ',' + _str(oversold) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferVPos, True)
    ArraySetAsSeries(BufferVNeg, True)
    ArraySetAsSeries(BufferVHigh, True)
    ArraySetAsSeries(BufferVLow, True)
    ArraySetAsSeries(BufferMAUp, True)
    ArraySetAsSeries(BufferMADn, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, 1)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_v - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferVHigh[i] = fabs(high[i] - low[i + 1])
        BufferVLow[i] = fabs(low[i] - high[i + 1])
    for i in range(limit, 0 - 1, -1):
        sum_v_high = 0.0
        sum_v_low = 0.0
        sum_atr = 0.0
        for j in range(i + period_v - 1, i - 1, -1):
            sum_v_high += BufferVHigh[j]
            sum_v_low += BufferVLow[j]
            sum_atr += BufferATR[j]
        BufferVPos[i] = ((_fdiv(sum_v_high, sum_atr) * 100.0) if (sum_atr != 0) else 100.0)
        BufferVNeg[i] = ((_fdiv(sum_v_low, sum_atr) * 100.0) if (sum_atr != 0) else 100.0)
        BufferMAUp[i] = GetSMA(rates_total, i, period_ma, BufferVPos)
        BufferMADn[i] = GetSMA(rates_total, i, period_ma, BufferVNeg)
        BufferDN[i] = EMPTY_VALUE
        BufferUP[i] = BufferDN[i]
        BufferNL[i] = 0.5
        if InpUseSmooth:
            if BufferMAUp[i] > overbought and BufferMADn[i] < oversold:
                BufferUP[i] = 0.5
                BufferNL[i] = EMPTY_VALUE
                BufferDN[i] = BufferNL[i]
            elif BufferMADn[i] > overbought and BufferMAUp[i] < oversold:
                BufferDN[i] = 0.5
                BufferNL[i] = EMPTY_VALUE
                BufferUP[i] = BufferNL[i]
            else:
                BufferNL[i] = 0.5
                BufferDN[i] = EMPTY_VALUE
                BufferUP[i] = BufferDN[i]
        else:
            if BufferVPos[i] > overbought and BufferVNeg[i] < oversold:
                BufferUP[i] = 0.5
                BufferNL[i] = EMPTY_VALUE
                BufferDN[i] = BufferNL[i]
            elif BufferVNeg[i] > overbought and BufferVPos[i] < oversold:
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

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)

def SizeByScale():
    scale = _uchar(ChartGetInteger(0, CHART_SCALE))
    size = (1 if (scale < 3) else 2 if (scale == 3) else 5 if (scale == 4) else 8)
    return size

def Descriptions():
    x = 4
    y = 1
    arr_texts = Arr.of(['Up direction', 'Down direction', 'Neutral'], fill="")
    for i in range(0, 3):
        name = prefix + 'label' + _str(i)
        clr = _uint(PlotIndexGetInteger(i, PLOT_LINE_COLOR))
        x = (x if (i == 0) else 110 if (i == 1) else 230)
        Label(name, x, y, CharToString(167), 16, clr, 'Wingdings')
        Label(name + '_txt', x + 10, y + 5, arr_texts[i], 10, clrGray, 'Calibri')

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


class VortexTrend(_MQL5Indicator):
    name = 'Vortex_Trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodV': 14,  # Vortex period
        'InpOverbought': 110.0,  # Upper limit of the filtering range
        'InpOversold': 90.0,  # Lower limit of the filtering range
        'InpUseSmooth': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use Vortex smoothing
        'InpPeriodMA': 20,  # Smoothing
    }

