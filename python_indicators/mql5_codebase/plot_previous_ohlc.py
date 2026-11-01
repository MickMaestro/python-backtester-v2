"""Plot Previous OHLC — converted from MQL5: MQL5 Indicators/Plot the previous candlestick OHLC of the selected period/Plot Previous OHLC.mq5

Copyright: Copyright 2023, https://www.mql5.com/en/users/phade/; Link: https://www.mql5.com/en/users/phade/; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, https://www.mql5.com/en/users/phade/', 'link': 'https://www.mql5.com/en/users/phade/', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'High', 2: 'Low', 3: 'Open', 4: 'Close'}, 'levels': [], 'description': [], 'name': 'Plot Previous OHLC', 'source': 'MQL5 Indicators/Plot the previous candlestick OHLC of the selected period/Plot Previous OHLC.mq5', 'folder': 'Plot the previous candlestick OHLC of the selected period', 'inputs': [{'mql': 'timeFrameSelector', 'py': 'timeFrameSelector', 'param': 'timeFrameSelector', 'type': 'int', 'default': 16408, 'label': 'Choose period to find the previous highs and lows', 'sinput': False}, {'mql': 'resistanceLineColor', 'py': 'resistanceLineColor', 'param': None, 'type': 'color', 'default': 13749760, 'label': 'Color of the previous highs', 'sinput': False}, {'mql': 'supportLineColor', 'py': 'supportLineColor', 'param': None, 'type': 'color', 'default': 11119017, 'label': 'Color of the previous lows', 'sinput': False}, {'mql': 'candleOpenColor', 'py': 'candleOpenColor', 'param': None, 'type': 'color', 'default': 13882323, 'label': 'Color of the previous candle open', 'sinput': False}, {'mql': 'candleCloseColor', 'py': 'candleCloseColor', 'param': None, 'type': 'color', 'default': 12180223, 'label': 'Color of the previous candle close', 'sinput': False}, {'mql': 'shift', 'py': 'shift', 'param': 'shift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
OpenBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
timeToUse = 0
prevTimeFrame = PERIOD_CURRENT
timeFrameSelector = _input('timeFrameSelector', PERIOD_D1)  # Choose period to find the previous highs and lows
resistanceLineColor = _input('resistanceLineColor', clrDarkTurquoise)  # Color of the previous highs
supportLineColor = _input('supportLineColor', clrDarkGray)  # Color of the previous lows
candleOpenColor = _input('candleOpenColor', clrLightGray)  # Color of the previous candle open
candleCloseColor = _input('candleCloseColor', clrPeachPuff)  # Color of the previous candle close
shift = _input('shift', 0)  # Shift

def OnInit():
    global timeToUse
    IndicatorSetString(INDICATOR_SHORTNAME, 'PrevDayHighLow')
    SetIndexBuffer(0, HighBuffer)
    SetIndexBuffer(1, LowBuffer)
    SetIndexBuffer(2, OpenBuffer)
    SetIndexBuffer(3, CloseBuffer)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, resistanceLineColor)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, supportLineColor)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, candleOpenColor)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, candleCloseColor)
    timeToUse = iTime(Symbol(), timeFrameSelector, shift)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated == 0:
        ResetBuffers()
    start = (1 if (prev_calculated == 0) else (prev_calculated - 1))
    for i in range(start, rates_total):
        HighBuffer[i] = prevDayHigh(timeToUse, timeFrameSelector)
        LowBuffer[i] = prevDayLow(timeToUse, timeFrameSelector)
        OpenBuffer[i] = prevDayOpen(timeToUse, timeFrameSelector)
        CloseBuffer[i] = prevDayClose(timeToUse, timeFrameSelector)
    return rates_total

def ResetBuffers():
    ArrayInitialize(HighBuffer, EMPTY_VALUE)
    ArrayInitialize(LowBuffer, EMPTY_VALUE)
    ArrayInitialize(OpenBuffer, EMPTY_VALUE)
    ArrayInitialize(CloseBuffer, EMPTY_VALUE)

def prevDayHigh(barShift, timeFrame):
    prevBar = iBarShift(Symbol(), timeFrame, barShift)
    highPrice = iHigh(Symbol(), timeFrame, prevBar)
    return highPrice

def prevDayLow(barShift, timeFrame):
    prevBar = iBarShift(Symbol(), timeFrame, barShift)
    lowPrice = iLow(Symbol(), timeFrame, prevBar)
    return lowPrice

def prevDayOpen(barShift, timeFrame):
    prevBar = iBarShift(Symbol(), timeFrame, barShift)
    openPrice = iOpen(Symbol(), timeFrame, prevBar)
    return openPrice

def prevDayClose(barShift, timeFrame):
    prevBar = iBarShift(Symbol(), timeFrame, barShift)
    closePrice = iClose(Symbol(), timeFrame, prevBar)
    return closePrice


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PlotPreviousOHLC(_MQL5Indicator):
    name = 'Plot Previous OHLC'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'timeFrameSelector': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Choose period to find the previous highs and lows
        'shift': 0,  # Shift
    }

