"""Specified_Time_Range_Candles — converted from MQL5: MQL5 Indicators/Specified_Time_Range_Candles/Specified_Time_Range_Candles.mq5

Specified time range candles indicator
Colored candles depending on specific time range.
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [5737262, 17919, 6908265, 11119017]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Specified time range candles indicator', 'Colored candles depending on specific time range.'], 'name': 'Specified_Time_Range_Candles', 'source': 'MQL5 Indicators/Specified_Time_Range_Candles/Specified_Time_Range_Candles.mq5', 'folder': 'Specified_Time_Range_Candles', 'inputs': [{'mql': 'InpStartHour', 'py': 'InpStartHour', 'param': 'InpStartHour', 'type': 'uint', 'default': 8, 'label': 'Start hour of the trading session', 'sinput': False}, {'mql': 'InpHours', 'py': 'InpHours', 'param': 'InpHours', 'type': 'uint', 'default': 5, 'label': 'Session length', 'sinput': False}, {'mql': 'InpChartMode', 'py': 'InpChartMode', 'param': 'InpChartMode', 'type': 'int', 'default': 0, 'label': 'Chart mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CANDLE_TYPE
CANDLE_TYPE_BULLISH = 0
CANDLE_TYPE_BEARISH = 1
CANDLE_TYPE_NEUTRAL = 2
CANDLE_TYPE_NONE = 3
_enum('ENUM_CANDLE_TYPE', {0: 'CANDLE_TYPE_BULLISH', 1: 'CANDLE_TYPE_BEARISH', 2: 'CANDLE_TYPE_NEUTRAL', 3: 'CANDLE_TYPE_NONE'})

# ---- inputs and global variables
InpStartHour = _input('InpStartHour', 8)  # Start hour of the trading session
InpHours = _input('InpHours', 5)  # Session length
InpChartMode = _input('InpChartMode', CHART_BARS)  # Chart mode
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
start_hour = 0
hours = 0
current_candle = False
prev_mode = 0

def OnInit():
    global current_candle, hours, prev_mode, start_hour
    start_hour = (23 if (InpStartHour > 23) else InpStartHour)
    diff = 24 - start_hour
    hours = (diff if (_int(InpHours) > diff) else InpHours)
    current_candle = True
    prev_mode = ChartGetInteger(0, CHART_MODE)
    ChartSetInteger(0, CHART_MODE, InpChartMode)
    ChartRedraw()
    SetIndexBuffer(0, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Specified time range candles (' + _str(start_hour) + ',' + _str(hours) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ChartSetInteger(0, CHART_MODE, prev_mode)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < fmax(hours, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 3)
    for i in range(limit, 0 - 1, -1):
        BufferCandleClose[i] = EMPTY_VALUE
        BufferCandleLow[i] = BufferCandleClose[i]
        BufferCandleHigh[i] = BufferCandleLow[i]
        BufferCandleOpen[i] = BufferCandleHigh[i]
        type_ = CandleType(i, open, close, time)
        BufferColors[i] = 3.0
        if type_ == CANDLE_TYPE_BULLISH:
            BufferCandleOpen[i] = iOpen(None, PERIOD_CURRENT, i)
            BufferCandleHigh[i] = iHigh(None, PERIOD_CURRENT, i)
            BufferCandleLow[i] = iLow(None, PERIOD_CURRENT, i)
            BufferCandleClose[i] = iClose(None, PERIOD_CURRENT, i)
            BufferColors[i] = 0.0
        elif type_ == CANDLE_TYPE_BEARISH:
            BufferCandleOpen[i] = iOpen(None, PERIOD_CURRENT, i)
            BufferCandleHigh[i] = iHigh(None, PERIOD_CURRENT, i)
            BufferCandleLow[i] = iLow(None, PERIOD_CURRENT, i)
            BufferCandleClose[i] = iClose(None, PERIOD_CURRENT, i)
            BufferColors[i] = 1.0
        elif type_ == CANDLE_TYPE_NEUTRAL:
            BufferCandleOpen[i] = iOpen(None, PERIOD_CURRENT, i)
            BufferCandleHigh[i] = iHigh(None, PERIOD_CURRENT, i)
            BufferCandleLow[i] = iLow(None, PERIOD_CURRENT, i)
            BufferCandleClose[i] = iClose(None, PERIOD_CURRENT, i)
            BufferColors[i] = 2.0
    return rates_total

def CandleType(shift, open, close, time):
    total = start_hour + hours
    for j in range(start_hour, total):
        hour = (0 if (j == 24) else (j - 24) if (j > 24) else j)
        if TimeHour_u(time[shift]) == hour or (current_candle and shift == 0):
            return (CANDLE_TYPE_BULLISH if (close[shift] > open[shift]) else CANDLE_TYPE_BEARISH if (close[shift] < open[shift]) else CANDLE_TYPE_NEUTRAL)
    return CANDLE_TYPE_NONE

def TimeHour_u(time):
    tm = MqlDateTime()
    if not TimeToStruct(time, tm):
        return WRONG_VALUE
    return tm.hour


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpecifiedTimeRangeCandles(_MQL5Indicator):
    name = 'Specified_Time_Range_Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpStartHour': 8,  # Start hour of the trading session
        'InpHours': 5,  # Session length
        'InpChartMode': _Choice({0: 'CHART_BARS', 1: 'CHART_CANDLES', 2: 'CHART_LINE'}, default=0),  # Chart mode
    }

