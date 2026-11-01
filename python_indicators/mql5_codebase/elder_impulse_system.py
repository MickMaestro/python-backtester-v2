"""Elder_Impulse_System — converted from MQL5: MQL5 Indicators/Elder_Impulse_System/Elder_Impulse_System.mq5

Elder Impulse System indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [32768], 2: [255], 3: [11119017]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'EIS Up', 2: 'EIS Down', 3: 'EIS Neutral'}, 'levels': [], 'description': ['Elder Impulse System indicator'], 'name': 'Elder_Impulse_System', 'source': 'MQL5 Indicators/Elder_Impulse_System/Elder_Impulse_System.mq5', 'folder': 'Elder_Impulse_System', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'uint', 'default': 13, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'MACD fast EMA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 26, 'label': 'MACD slow EMA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 32768  # #property indicator_color1
indicator_color2 = 255  # #property indicator_color2
indicator_color3 = 11119017  # #property indicator_color3

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 13)  # EMA period
InpPeriodFast = _input('InpPeriodFast', 12)  # MACD fast EMA period
InpPeriodSlow = _input('InpPeriodSlow', 26)  # MACD slow EMA period
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
BufferMACD = Arr(0, 0.0)
prefix = ""
wnd = 0
period_ema = 0
period_fma = 0
period_sma = 0
period_max = 0
handle_ema = 0
handle_macd = 0

def OnInit():
    global handle_ema, handle_macd, period_ema, period_fma, period_max, period_sma, prefix, wnd
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    period_fma = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_sma = ((period_fma + 1) if (InpPeriodSlow == period_fma) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_ema = (1 if (InpPeriodEMA < 1) else InpPeriodEMA)
    period_max = fmax(period_ema, fmax(period_fma, period_sma))
    SizeByScale()
    Descriptions()
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferEMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMACD, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Elder Impulse System (' + _str(period_ema) + ',' + _str(period_fma) + ',' + _str(period_sma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferEMA, True)
    ArraySetAsSeries(BufferMACD, True)
    ResetLastError()
    handle_ema = iMA(None, PERIOD_CURRENT, period_ema, 0, MODE_EMA, PRICE_CLOSE)
    if handle_ema == INVALID_HANDLE:
        Print('The iMA(', _str(period_ema), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_macd = iMACD(None, PERIOD_CURRENT, period_fma, period_sma, 1, PRICE_CLOSE)
    if handle_macd == INVALID_HANDLE:
        Print('The iMA(', _str(period_fma), ',', _str(period_sma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
        ArrayInitialize(BufferEMA, 0)
        ArrayInitialize(BufferMACD, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ema, 0, 0, count, BufferEMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_macd, MAIN_LINE, 0, count, BufferMACD)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferNL[i] = 0.5
        BufferDN[i] = EMPTY_VALUE
        BufferUP[i] = BufferDN[i]
        if BufferEMA[i] > BufferEMA[i + 1] and BufferMACD[i] > BufferMACD[i + 1]:
            BufferUP[i] = 0.5
            BufferNL[i] = EMPTY_VALUE
        else:
            BufferUP[i] = EMPTY_VALUE
        if BufferEMA[i] < BufferEMA[i + 1] and BufferMACD[i] < BufferMACD[i + 1]:
            BufferDN[i] = 0.5
            BufferNL[i] = EMPTY_VALUE
        else:
            BufferDN[i] = EMPTY_VALUE
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
    arr_texts = Arr.of(['Long or stand aside, no shorting', 'Short or stand aside, no buying', 'Either long or short'], fill="")
    arr_names = Arr(3, "", dyn=False)
    for i in range(0, 3):
        arr_names[i] = prefix + 'label' + _str(i)
        arr_colors[i] = PlotIndexGetInteger(i, PLOT_LINE_COLOR)
        x = (x if (i == 0) else 200 if (i == 1) else 390)
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


class ElderImpulseSystem(_MQL5Indicator):
    name = 'Elder_Impulse_System'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 13,  # EMA period
        'InpPeriodFast': 12,  # MACD fast EMA period
        'InpPeriodSlow': 26,  # MACD slow EMA period
    }

