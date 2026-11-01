"""Advanced_Fractal_Overlay — converted from MQL5: MQL5 Indicators/Advanced_Fractal_Overlay/Advanced_Fractal_Overlay.mq5

Advanced Fractal Overlay
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 17919, 8421504]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Advanced Fractal Overlay'], 'name': 'Advanced_Fractal_Overlay', 'source': 'MQL5 Indicators/Advanced_Fractal_Overlay/Advanced_Fractal_Overlay.mq5', 'folder': 'Advanced_Fractal_Overlay', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_TREND_TYPE
TREND_TYPE_BULLISH = 0
TREND_TYPE_BEARISH = 1
_enum('ENUM_TREND_TYPE', {0: 'TREND_TYPE_BULLISH', 1: 'TREND_TYPE_BEARISH'})

# ---- inputs and global variables
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFractUP = Arr(0, 0.0)
BufferFractDN = Arr(0, 0.0)
handle_fr = 0
current = 0
prev_fgnd = False

def OnInit():
    global current, handle_fr, prev_fgnd
    current = TREND_TYPE_BULLISH
    prev_fgnd = (ChartGetInteger(0, CHART_FOREGROUND) != 0)
    ChartSetInteger(0, CHART_FOREGROUND, False)
    ChartRedraw()
    SetIndexBuffer(0, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BufferFractUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferFractDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Advanced Fractal Overlay')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFractUP, True)
    ArraySetAsSeries(BufferFractDN, True)
    ResetLastError()
    handle_fr = iFractals(None, PERIOD_CURRENT)
    if handle_fr == INVALID_HANDLE:
        Print('The iFractals object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ChartSetInteger(0, CHART_FOREGROUND, prev_fgnd)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferFractUP, 0)
        ArrayInitialize(BufferFractDN, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fr, UPPER_LINE, 0, count, BufferFractUP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_fr, LOWER_LINE, 0, count, BufferFractDN)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        SettingCandle(i, open, high, low, close)
        trend_type = TrendType(rates_total, i, close)
        BufferColors[i] = (0 if (trend_type == TREND_TYPE_BULLISH) else 1 if (trend_type == TREND_TYPE_BEARISH) else 2)
    return rates_total

def SettingCandle(shift, open, high, low, close):
    BufferCandleOpen[shift] = open[shift]
    BufferCandleHigh[shift] = high[shift]
    BufferCandleLow[shift] = low[shift]
    BufferCandleClose[shift] = close[shift]

def TrendType(rates_total, shift, close):
    global current
    last_fractal_up = 0.0
    last_fractal_dn = 0.0
    found_up = False
    found_dn = False
    i = shift + 1
    while (not found_up) and i < (rates_total - 1):
        if BufferFractUP[i] > 0 and BufferFractUP[i] < EMPTY_VALUE:
            last_fractal_up = BufferFractUP[i]
            found_up = True
        i += 1
    i = shift + 1
    while (not found_dn) and i < (rates_total - 1):
        if BufferFractDN[i] > 0 and BufferFractDN[i] < EMPTY_VALUE:
            last_fractal_dn = BufferFractDN[i]
            found_dn = True
        i += 1
    if current == TREND_TYPE_BEARISH:
        if close[shift] > last_fractal_up:
            current = TREND_TYPE_BULLISH
    if current == TREND_TYPE_BULLISH:
        if close[shift] < last_fractal_dn:
            current = TREND_TYPE_BEARISH
    return current


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AdvancedFractalOverlay(_MQL5Indicator):
    name = 'Advanced_Fractal_Overlay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

