"""Custom_Day_Candles — converted from MQL5: MQL5 Indicators/Custom Daily Candlesticks/Custom_Day_Candles.mq5

Draws of custom day candles
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [7451452, 42495, 8421504]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Candle'}, 'levels': [], 'description': ['Draws of custom day candles'], 'name': 'Custom_Day_Candles', 'source': 'MQL5 Indicators/Custom Daily Candlesticks/Custom_Day_Candles.mq5', 'folder': 'Custom Daily Candlesticks', 'inputs': [{'mql': 'InpBeginDayHour', 'py': 'InpBeginDayHour', 'param': 'InpBeginDayHour', 'type': 'int', 'default': 0, 'label': 'Hour of begin day', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'int', 'default': 500, 'label': 'Candles vertical shift', 'sinput': False}, {'mql': 'InpBullishColor', 'py': 'InpBullishColor', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'Color of bullish candle', 'sinput': False}, {'mql': 'InpBearishColor', 'py': 'InpBearishColor', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Color of bearish candle', 'sinput': False}, {'mql': 'InpDojiColor', 'py': 'InpDojiColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Color of doji candle', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBeginDayHour = _input('InpBeginDayHour', 0)  # Hour of begin day
InpShift = _input('InpShift', 500)  # Candles vertical shift
InpBullishColor = _input('InpBullishColor', clrMediumSeaGreen)  # Color of bullish candle
InpBearishColor = _input('InpBearishColor', clrOrange)  # Color of bearish candle
InpDojiColor = _input('InpDojiColor', clrGray)  # Color of doji candle
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)

def OnInit():
    if Period() != PERIOD_D1:
        Alert('"Custom Day Candles": Timeframe must be D1')
        return INIT_FAILED
    SetIndexBuffer(0, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, 0, InpBullishColor)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, 1, InpBearishColor)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Custom Day Candles')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2:
        return 0
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferCandleOpen, 0.0)
        ArrayInitialize(BufferCandleHigh, 0.0)
        ArrayInitialize(BufferCandleLow, 0.0)
        ArrayInitialize(BufferCandleClose, 0.0)
    for i in range(limit, 0 - 1, -1):
        DT1 = time[i] + (InpBeginDayHour * PeriodSeconds(PERIOD_H1))
        DT2 = time[i] + PeriodSeconds(PERIOD_D1) + (InpBeginDayHour * PeriodSeconds(PERIOD_H1)) - 1
        Bar1 = BarShift(Symbol(), PERIOD_H1, DT1)
        Bar2 = BarShift(Symbol(), PERIOD_H1, DT2)
        if Bar1 == WRONG_VALUE or Bar2 == WRONG_VALUE:
            return 0
        Time1 = Time("", PERIOD_H1, Bar1)
        Time2 = Time("", PERIOD_H1, Bar2)
        if Time1 == 0 or Time2 == 0:
            return 0
        if Time1 < DT1:
            Bar1 -= 1
        if Time2 > DT2:
            Bar2 += 1
        if Bar1 < Bar2:
            continue
        O = Open(Symbol(), PERIOD_H1, Bar1)
        C = Close(Symbol(), PERIOD_H1, Bar2)
        H = High(Symbol(), PERIOD_H1, Highest(Symbol(), PERIOD_H1, PRICE_HIGH, Bar1 - Bar2 + 1, Bar2))
        L = Low(Symbol(), PERIOD_H1, Lowest(Symbol(), PERIOD_H1, PRICE_LOW, Bar1 - Bar2 + 1, Bar2))
        if ((O == 0 or H == 0) or L == 0) or C == 0:
            return 0
        if DT1 > TimeCurrent() or Point() == 0:
            return 0
        BufferCandleOpen[i] = NormalizeDouble(O + (InpShift * Point()), Digits())
        BufferCandleHigh[i] = NormalizeDouble(H + (InpShift * Point()), Digits())
        BufferCandleLow[i] = NormalizeDouble(L + (InpShift * Point()), Digits())
        BufferCandleClose[i] = NormalizeDouble(C + (InpShift * Point()), Digits())
        if O < C:
            BufferColors[i] = 0.0
        elif O > C:
            BufferColors[i] = 1.0
        else:
            BufferColors[i] = 2.0
    return rates_total

def BarShift(symbol_name, timeframe, time):
    res = WRONG_VALUE
    last_bar = Box(0)
    if SeriesInfoInteger(symbol_name, timeframe, SERIES_LASTBAR_DATE, last_bar):
        if time > last_bar.v:
            res = 0
        else:
            shift = Bars(symbol_name, timeframe, time, last_bar.v)
            if shift > 0:
                res = shift - 1
    return res

def Open(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    if CopyOpen(symbol_name, timeframe, shift, 1, array) == 1:
        return array[0]
    return 0.0

def High(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    if CopyHigh(symbol_name, timeframe, shift, 1, array) == 1:
        return array[0]
    return 0.0

def Low(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    if CopyLow(symbol_name, timeframe, shift, 1, array) == 1:
        return array[0]
    return 0.0

def Close(symbol_name, timeframe, shift):
    array = Arr(0, 0.0)
    if CopyClose(symbol_name, timeframe, shift, 1, array) == 1:
        return array[0]
    return 0.0

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    if CopyTime(symbol_name, timeframe, shift, 1, array) == 1:
        return array[0]
    return 0

def Highest(symbol_name, timeframe, mode_price, count=WHOLE_ARRAY, start=0):
    if start < 0:
        return -1
    if count == WHOLE_ARRAY:
        count = Bars(symbol_name, timeframe)
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    copied = (CopyClose(symbol_name, timeframe, start, count, array) if (mode_price == PRICE_CLOSE) else CopyHigh(symbol_name, timeframe, start, count, array) if (mode_price == PRICE_HIGH) else CopyLow(symbol_name, timeframe, start, count, array) if (mode_price == PRICE_LOW) else CopyOpen(symbol_name, timeframe, start, count, array))
    return (0 if (copied <= 0) else (ArrayMaximum(array) + start))

def Lowest(symbol_name, timeframe, mode_price, count=WHOLE_ARRAY, start=0):
    if start < 0:
        return -1
    if count == WHOLE_ARRAY:
        count = Bars(symbol_name, timeframe)
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    copied = (CopyClose(symbol_name, timeframe, start, count, array) if (mode_price == PRICE_CLOSE) else CopyHigh(symbol_name, timeframe, start, count, array) if (mode_price == PRICE_HIGH) else CopyLow(symbol_name, timeframe, start, count, array) if (mode_price == PRICE_LOW) else CopyOpen(symbol_name, timeframe, start, count, array))
    return (0 if (copied <= 0) else (ArrayMinimum(array) + start))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomDayCandles(_MQL5Indicator):
    name = 'Custom_Day_Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBeginDayHour': 0,  # Hour of begin day
        'InpShift': 500,  # Candles vertical shift
    }

