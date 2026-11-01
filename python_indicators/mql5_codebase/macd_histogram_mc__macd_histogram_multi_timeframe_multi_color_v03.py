"""macd_histogram_mc — converted from MQL5: MQL5 Indicators/MACD Histogram, multi-timeframe, multi-color [v03]/macd_histogram_mc.mq5

Moving Average Convergence/Divergence, Histogram, Multi-color
Copyright: 2010, traderak20@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [16711680], 2: [255], 3: [32768, 255, 16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'MACD', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': ['Moving Average Convergence/Divergence, Histogram, Multi-color'], 'name': 'macd_histogram_mc', 'source': 'MQL5 Indicators/MACD Histogram, multi-timeframe, multi-color [v03]/macd_histogram_mc.mq5', 'folder': 'MACD Histogram, multi-timeframe, multi-color [v03]', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalMA', 'py': 'InpSignalMA', 'param': 'InpSignalMA', 'type': 'int', 'default': 9, 'label': 'Signal MA period', 'sinput': False}, {'mql': 'InpAppliedSignalMA', 'py': 'InpAppliedSignalMA', 'param': 'InpAppliedSignalMA', 'type': 'int', 'default': 0, 'label': 'Applied MA method for signal line', 'sinput': False}, {'mql': 'InpUseMultiColor', 'py': 'InpUseMultiColor', 'param': 'InpUseMultiColor', 'type': 'int', 'default': 0, 'label': 'Use multi-color or single-color histogram', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum colorswitch
MultiColor = 0
SingleColor = 1
_enum('colorswitch', {0: 'MultiColor', 1: 'SingleColor'})

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpSignalMA = _input('InpSignalMA', 9)  # Signal MA period
InpAppliedSignalMA = _input('InpAppliedSignalMA', MODE_SMA)  # Applied MA method for signal line
InpUseMultiColor = _input('InpUseMultiColor', MultiColor)  # Use multi-color or single-color histogram
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtMacdBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtHistogramBuffer = Arr(0, 0.0)
ExtHistogramColorBuffer = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
weightsum_global = 0  # used for calculation of LWMA
ExtFastMaHandle = 0
ExtSlowMaHandle = 0
ShowErrorMessages = True  # turn on/off error messages for debugging

def OnInit():
    global ExtFastMaHandle, ExtSlowMaHandle, weightsum_global
    SetIndexBuffer(0, ExtMacdBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHistogramBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtHistogramColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtMacdBuffer, True)
    ArraySetAsSeries(ExtSignalBuffer, True)
    ArraySetAsSeries(ExtHistogramBuffer, True)
    ArraySetAsSeries(ExtHistogramColorBuffer, True)
    ArraySetAsSeries(ExtFastMaBuffer, True)
    ArraySetAsSeries(ExtSlowMaBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpSlowEMA - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpSlowEMA + InpSignalMA - 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpSlowEMA + InpSignalMA - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD(' + _str(InpFastEMA) + ',' + _str(InpSlowEMA) + ',' + _str(InpSignalMA) + ')')
    ExtFastMaHandle = iMA(None, 0, InpFastEMA, 0, MODE_EMA, InpAppliedPrice)
    ExtSlowMaHandle = iMA(None, 0, InpSlowEMA, 0, MODE_EMA, InpAppliedPrice)
    weightsum_global = 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < InpSignalMA:
        return 0
    calculated = 0
    calculated = BarsCalculated(ExtFastMaHandle)
    if calculated < rates_total:
        if ShowErrorMessages:
            Print('Not all data of ExtFastMaHandle has been calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtSlowMaHandle)
    if calculated < rates_total:
        if ShowErrorMessages:
            Print('Not all data of ExtSlowMaHandle has been calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyBuffer(ExtFastMaHandle, 0, 0, to_copy, ExtFastMaBuffer) <= 0:
        if ShowErrorMessages:
            Print('Getting fast EMA failed! Error', GetLastError())
        return 0
    if CopyBuffer(ExtSlowMaHandle, 0, 0, to_copy, ExtSlowMaBuffer) <= 0:
        if ShowErrorMessages:
            Print('Getting slow SMA failed! Error', GetLastError())
        return 0
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    if limit > (rates_total - 1 - 1):
        limit = rates_total - 1 - 1
    for i in range(limit, 0 - 1, -1):
        ExtMacdBuffer[i] = ExtFastMaBuffer[i] - ExtSlowMaBuffer[i]
    if InpAppliedSignalMA == MODE_SMA:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, InpSignalMA, ExtMacdBuffer, ExtSignalBuffer)
    if InpAppliedSignalMA == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpSignalMA, ExtMacdBuffer, ExtSignalBuffer)
    if InpAppliedSignalMA == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, InpSignalMA, ExtMacdBuffer, ExtSignalBuffer)
    if InpAppliedSignalMA == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, InpSignalMA, ExtMacdBuffer, ExtSignalBuffer, _GlobRef(globals(), 'weightsum_global'))
    for i in range(limit, 0 - 1, -1):
        ExtHistogramBuffer[i] = ExtMacdBuffer[i] - ExtSignalBuffer[i]
        if InpUseMultiColor == MultiColor:
            if ExtHistogramBuffer[i] > ExtHistogramBuffer[i + 1]:
                ExtHistogramColorBuffer[i] = 0.0
            if ExtHistogramBuffer[i] < ExtHistogramBuffer[i + 1]:
                ExtHistogramColorBuffer[i] = 1.0
            if ExtHistogramBuffer[i] == ExtHistogramBuffer[i + 1]:
                ExtHistogramColorBuffer[i] = 2.0
        if InpUseMultiColor == SingleColor:
            ExtHistogramColorBuffer[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdHistogramMc(_MQL5Indicator):
    name = 'macd_histogram_mc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpSignalMA': 9,  # Signal MA period
        'InpAppliedSignalMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Applied MA method for signal line
        'InpUseMultiColor': _Choice({0: 'MultiColor', 1: 'SingleColor'}, default=0),  # Use multi-color or single-color histogram
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

