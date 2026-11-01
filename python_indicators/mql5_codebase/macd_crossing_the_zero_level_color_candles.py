"""MACD Crossing the zero level (color candles) — converted from MQL5: MQL5 Indicators/MACD Crossing the zero level (color candles)/MACD Crossing the zero level (color candles).mq5

Moving Average Convergence/Divergence and lines
Color candles crossing the zero level
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.000', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Crossing'}, 'levels': [], 'description': ['Moving Average Convergence/Divergence and lines', 'Color candles crossing the zero level'], 'name': 'MACD Crossing the zero level (color candles)', 'source': 'MQL5 Indicators/MACD Crossing the zero level (color candles)/MACD Crossing the zero level (color candles).mq5', 'folder': 'MACD Crossing the zero level (color candles)', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalSMA', 'py': 'InpSignalSMA', 'param': 'InpSignalSMA', 'type': 'int', 'default': 9, 'label': 'Signal SMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpBaseCrossingLine', 'py': 'InpBaseCrossingLine', 'param': 'InpBaseCrossingLine', 'type': 'int', 'default': 1, 'label': 'Crossing the zero level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum BASE_CROSSING_LINE
MACD = 0
Signal = 1
_enum('BASE_CROSSING_LINE', {0: 'MACD', 1: 'Signal'})

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpSignalSMA = _input('InpSignalSMA', 9)  # Signal SMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpBaseCrossingLine = _input('InpBaseCrossingLine', Signal)  # Crossing the zero level
ExtColorCandlesBuffer1 = Arr(0, 0.0)
ExtColorCandlesBuffer2 = Arr(0, 0.0)
ExtColorCandlesBuffer3 = Arr(0, 0.0)
ExtColorCandlesBuffer4 = Arr(0, 0.0)
ExtColorCandlesColors = Arr(0, 0.0)
ExtMacdBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
ExtFastMaHandle = 0
ExtSlowMaHandle = 0

def OnInit():
    global ExtFastMaHandle, ExtSlowMaHandle
    SetIndexBuffer(0, ExtColorCandlesBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorCandlesBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtColorCandlesBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtColorCandlesBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorCandlesColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, ExtMacdBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtSignalBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    if InpBaseCrossingLine == Signal:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpSignalSMA - 1)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpSignalSMA - 1)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpSignalSMA - 1)
        PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, InpSignalSMA - 1)
        PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, InpSignalSMA - 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD Crossing the zero level (color candles)(' + _str(InpFastEMA) + ',' + _str(InpSlowEMA) + ',' + _str(InpSignalSMA) + ')')
    ExtFastMaHandle = iMA(None, 0, InpFastEMA, 0, MODE_EMA, InpAppliedPrice)
    ExtSlowMaHandle = iMA(None, 0, InpSlowEMA, 0, MODE_EMA, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < InpSignalSMA:
        return 0
    calculated = BarsCalculated(ExtFastMaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtFastMaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtSlowMaHandle)
    if calculated < rates_total:
        Print('Not all data of ExtSlowMaHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtFastMaHandle, 0, 0, to_copy, ExtFastMaBuffer) <= 0:
        Print('Getting fast EMA is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtSlowMaHandle, 0, 0, to_copy, ExtSlowMaBuffer) <= 0:
        Print('Getting slow SMA is failed! Error', GetLastError())
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        ExtMacdBuffer[i] = ExtFastMaBuffer[i] - ExtSlowMaBuffer[i]
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, InpSignalSMA, ExtMacdBuffer, ExtSignalBuffer)
    for i in range(limit, rates_total):
        ExtColorCandlesBuffer1[i] = open[i]
        ExtColorCandlesBuffer2[i] = high[i]
        ExtColorCandlesBuffer3[i] = low[i]
        ExtColorCandlesBuffer4[i] = close[i]
        if InpBaseCrossingLine == Signal:
            if ExtSignalBuffer[i] < 0.0:
                ExtColorCandlesColors[i] = 0.0
            else:
                ExtColorCandlesColors[i] = 1.0
        else:
            if ExtMacdBuffer[i] < 0.0:
                ExtColorCandlesColors[i] = 0.0
            else:
                ExtColorCandlesColors[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDCrossingTheZeroLevelColorCandles(_MQL5Indicator):
    name = 'MACD Crossing the zero level (color candles)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpSignalSMA': 9,  # Signal SMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpBaseCrossingLine': _Choice({0: 'MACD', 1: 'Signal'}, default=1),  # Crossing the zero level
    }

