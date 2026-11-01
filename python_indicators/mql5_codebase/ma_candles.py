"""MA_Candles — converted from MQL5: MQL5 Indicators/Moving Average Candles/MA_Candles.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [7451452, 42495]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CandleMA'}, 'levels': [], 'description': [], 'name': 'MA_Candles', 'source': 'MQL5 Indicators/Moving Average Candles/MA_Candles.mq5', 'folder': 'Moving Average Candles', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpShiftMA', 'py': 'InpShiftMA', 'param': 'InpShiftMA', 'type': 'int', 'default': 0, 'label': 'MA shift', 'sinput': False}, {'mql': 'InpBullishColor', 'py': 'InpBullishColor', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'Bullish candles color', 'sinput': False}, {'mql': 'InpBearishColor', 'py': 'InpBearishColor', 'param': None, 'type': 'color', 'default': 42495, 'label': 'Bearish candles color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # MA period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
InpShiftMA = _input('InpShiftMA', 0)  # MA shift
InpBullishColor = _input('InpBullishColor', clrMediumSeaGreen)  # Bullish candles color
InpBearishColor = _input('InpBearishColor', clrOrange)  # Bearish candles color
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferOpen = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
handle_open = 0
handle_high = 0
handle_low = 0
handle_close = 0
period = 0
shift = 0

def OnInit():
    global handle_close, handle_high, handle_low, handle_open, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BufferOpen, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferLow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferClose, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferOpen, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ArraySetAsSeries(BufferClose, True)
    for i in range(0, 4):
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, 0, InpBullishColor)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, 1, InpBearishColor)
        PlotIndexSetInteger(i, PLOT_SHIFT, InpShiftMA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Moving averages candles(' + _str(period) + ')')
    ResetLastError()
    handle_open = iMA(Symbol(), PERIOD_CURRENT, period, 0, InpMethod, PRICE_OPEN)
    if handle_open == INVALID_HANDLE:
        Print('The iMAbyOpen(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_high = iMA(Symbol(), PERIOD_CURRENT, period, 0, InpMethod, PRICE_HIGH)
    if handle_high == INVALID_HANDLE:
        Print('The iMAbyHigh(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_low = iMA(Symbol(), PERIOD_CURRENT, period, 0, InpMethod, PRICE_LOW)
    if handle_low == INVALID_HANDLE:
        Print('The iMAbyLow(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_close = iMA(Symbol(), PERIOD_CURRENT, period, 0, InpMethod, PRICE_CLOSE)
    if handle_close == INVALID_HANDLE:
        Print('The iMAbyClose(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 0)
        ArrayInitialize(BufferOpen, EMPTY_VALUE)
        ArrayInitialize(BufferHigh, EMPTY_VALUE)
        ArrayInitialize(BufferLow, EMPTY_VALUE)
        ArrayInitialize(BufferClose, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_open, 0, 0, count, BufferOpen)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_high, 0, 0, count, BufferHigh)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_low, 0, 0, count, BufferLow)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_close, 0, 0, count, BufferClose)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCandleOpen[i] = BufferOpen[i]
        BufferCandleHigh[i] = BufferHigh[i]
        BufferCandleLow[i] = BufferLow[i]
        BufferCandleClose[i] = BufferClose[i]
        if BufferClose[i] < BufferOpen[i]:
            BufferColors[i] = 1.0
        else:
            BufferColors[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACandles(_MQL5Indicator):
    name = 'MA_Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpShiftMA': 0,  # MA shift
    }

