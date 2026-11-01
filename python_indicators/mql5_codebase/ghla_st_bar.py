"""GHLA_ST_Bar — converted from MQL5: MQL5 Indicators/GHLA_ST_Bar/GHLA_ST_Bar.mq5

Gann HiLo Activator/SuperTrend Bar indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [32768], 2: [255], 3: [14599344]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'GHLA/ST Up', 2: 'GHLA/ST Down', 3: 'GHLA/ST Neutral'}, 'levels': [], 'description': ['Gann HiLo Activator/SuperTrend Bar indicator'], 'name': 'GHLA_ST_Bar', 'source': 'MQL5 Indicators/GHLA_ST_Bar/GHLA_ST_Bar.mq5', 'folder': 'GHLA_ST_Bar', 'inputs': [{'mql': 'InpPeriodGHLA', 'py': 'InpPeriodGHLA', 'param': 'InpPeriodGHLA', 'type': 'uint', 'default': 10, 'label': 'GHLA period', 'sinput': False}, {'mql': 'InpPeriodST', 'py': 'InpPeriodST', 'param': 'InpPeriodST', 'type': 'uint', 'default': 14, 'label': 'SuperTrend period', 'sinput': False}, {'mql': 'InpShiftST', 'py': 'InpShiftST', 'param': 'InpShiftST', 'type': 'uint', 'default': 20, 'label': 'SuperTrend shift', 'sinput': False}, {'mql': 'InpUseFilterST', 'py': 'InpUseFilterST', 'param': 'InpUseFilterST', 'type': 'int', 'default': 1, 'label': 'Use SuperTrend filter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_color1 = 32768  # #property indicator_color1
indicator_color2 = 255  # #property indicator_color2
indicator_color3 = 14599344  # #property indicator_color3

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodGHLA = _input('InpPeriodGHLA', 10)  # GHLA period
InpPeriodST = _input('InpPeriodST', 14)  # SuperTrend period
InpShiftST = _input('InpShiftST', 20)  # SuperTrend shift
InpUseFilterST = _input('InpUseFilterST', INPUT_YES)  # Use SuperTrend filter
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferNL = Arr(0, 0.0)
BufferGHLA = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
BufferDir = Arr(0, 0.0)
BufferST = Arr(0, 0.0)
BufferFlag = Arr(0, 0.0)
BufferCCI = Arr(0, 0.0)
prefix = ""
wnd = 0
period_ghla = 0
handle_mah = 0
handle_mal = 0
shift = 0.0
period_cci = 0
handle_cci = 0

def OnInit():
    global handle_cci, handle_mah, handle_mal, period_cci, period_ghla, prefix, shift, wnd
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    wnd = ChartWindowFind()
    period_ghla = (1 if (InpPeriodGHLA < 1) else InpPeriodGHLA)
    period_cci = (1 if (InpPeriodST < 1) else InpPeriodST)
    shift = InpShiftST * Point()
    SizeByScale()
    Descriptions()
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferGHLA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMAL, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferDir, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferST, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferFlag, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferCCI, INDICATOR_CALCULATIONS)
    for i in range(0, 3):
        PlotIndexSetInteger(i, PLOT_ARROW, 167)
    IndicatorSetString(INDICATOR_SHORTNAME, 'GHLA/SuperTrend Bar (' + _str(period_ghla) + ',' + _str(period_cci) + ',' + _str(InpShiftST) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)
    IndicatorSetInteger(INDICATOR_HEIGHT, 60)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferNL, True)
    ArraySetAsSeries(BufferGHLA, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ArraySetAsSeries(BufferDir, True)
    ArraySetAsSeries(BufferST, True)
    ArraySetAsSeries(BufferFlag, True)
    ArraySetAsSeries(BufferCCI, True)
    ResetLastError()
    handle_mah = iMA(None, PERIOD_CURRENT, period_ghla, 0, MODE_SMA, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(', _str(period_ghla), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mal = iMA(None, PERIOD_CURRENT, period_ghla, 0, MODE_SMA, PRICE_LOW)
    if handle_mal == INVALID_HANDLE:
        Print('The iMA(', _str(period_ghla), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_ghla, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferNL, EMPTY_VALUE)
        ArrayInitialize(BufferGHLA, 0)
        ArrayInitialize(BufferMAH, 0)
        ArrayInitialize(BufferMAL, 0)
        ArrayInitialize(BufferDir, 0)
        ArrayInitialize(BufferST, 0)
        ArrayInitialize(BufferFlag, 0)
        ArrayInitialize(BufferCCI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        avgH = BufferMAH[i]
        avgL = BufferMAL[i]
        sw = (1 if (close[i] > avgH) else -1 if (close[i] < avgL) else 0)
        BufferDir[i] = (sw if (sw != 0) else BufferDir[i + 1])
        if BufferDir[i] < 0:
            BufferGHLA[i] = avgH
        else:
            BufferGHLA[i] = avgL
        CCI = BufferCCI[i]
        BufferST[i] = BufferST[i + 1]
        BufferFlag[i] = BufferFlag[i + 1]
        if CCI > 0 and BufferFlag[i] <= 0:
            BufferFlag[i] = 1.0
            BufferST[i] = low[i] - shift
        if CCI < 0 and BufferFlag[i] >= 0:
            BufferFlag[i] = -1.0
            BufferST[i] = high[i] + shift
        BufferST[i] = ((low[i] - shift) if (BufferFlag[i] > 0 and (low[i] - shift) > BufferST[i + 1]) else (high[i] + shift) if (BufferFlag[i] < 0 and (high[i] + shift) < BufferST[i + 1]) else BufferST[i])
        if InpUseFilterST:
            if BufferFlag[i] > 0 and BufferST[i] > BufferST[i + 1]:
                if close[i] < open[i]:
                    BufferST[i] = BufferST[i + 1]
                if high[i] < high[i + 1]:
                    BufferST[i] = BufferST[i + 1]
            if BufferFlag[i] < 0 and BufferST[i] < BufferST[i + 1]:
                if close[i] > open[i]:
                    BufferST[i] = BufferST[i + 1]
                if low[i] > low[i + 1]:
                    BufferST[i] = BufferST[i + 1]
        ST = BufferST[i]
        GHLA = BufferGHLA[i]
        BufferNL[i] = EMPTY_VALUE
        BufferDN[i] = BufferNL[i]
        BufferUP[i] = BufferDN[i]
        if close[i] > ST and close[i] > GHLA:
            BufferUP[i] = 0.5
        else:
            if close[i] < ST and close[i] < GHLA:
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


class GHLASTBar(_MQL5Indicator):
    name = 'GHLA_ST_Bar'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodGHLA': 10,  # GHLA period
        'InpPeriodST': 14,  # SuperTrend period
        'InpShiftST': 20,  # SuperTrend shift
        'InpUseFilterST': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use SuperTrend filter
    }

