"""macd_histogram_mc_mtf — converted from MQL5: MQL5 Indicators/MACD Histogram, multi-timeframe, multi-color [v03]/macd_histogram_mc_mtf.mq5

Moving Average Convergence/Divergence, Histogram, Multi-timeframe, Multi-color
Copyright: 2010, traderak20@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [16711680], 2: [255], 3: [32768, 255, 16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'MACD_TF2', 2: 'Signal_TF2', 3: 'Histogram_TF2'}, 'levels': [], 'description': ['Moving Average Convergence/Divergence, Histogram, Multi-timeframe, Multi-color'], 'name': 'macd_histogram_mc_mtf', 'source': 'MQL5 Indicators/MACD Histogram, multi-timeframe, multi-color [v03]/macd_histogram_mc_mtf.mq5', 'folder': 'MACD Histogram, multi-timeframe, multi-color [v03]', 'inputs': [{'mql': 'InpTimeFrame_2', 'py': 'InpTimeFrame_2', 'param': 'InpTimeFrame_2', 'type': 'int', 'default': 16385, 'label': 'Timeframe 2 (TF2) period', 'sinput': False}, {'mql': 'InpIndicator_TF1', 'py': 'InpIndicator_TF1', 'param': None, 'type': 'string', 'default': 'MACD_Histogram_MC', 'label': 'Location of single timeframe indicator', 'sinput': False}, {'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalMA', 'py': 'InpSignalMA', 'param': 'InpSignalMA', 'type': 'int', 'default': 9, 'label': 'Signal MA period', 'sinput': False}, {'mql': 'InpAppliedSignalMA', 'py': 'InpAppliedSignalMA', 'param': 'InpAppliedSignalMA', 'type': 'int', 'default': 0, 'label': 'Applied MA method for signal line', 'sinput': False}, {'mql': 'InpUseMultiColor', 'py': 'InpUseMultiColor', 'param': 'InpUseMultiColor', 'type': 'int', 'default': 0, 'label': 'Use multi-color or single-color histogram', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum colorswitch
MultiColor = 0
SingleColor = 1
_enum('colorswitch', {0: 'MultiColor', 1: 'SingleColor'})

# ---- inputs and global variables
InpTimeFrame_2 = _input('InpTimeFrame_2', PERIOD_H1)  # Timeframe 2 (TF2) period
InpIndicator_TF1 = _input('InpIndicator_TF1', 'MACD_Histogram_MC')  # Location of single timeframe indicator
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpSignalMA = _input('InpSignalMA', 9)  # Signal MA period
InpAppliedSignalMA = _input('InpAppliedSignalMA', MODE_SMA)  # Applied MA method for signal line
InpUseMultiColor = _input('InpUseMultiColor', MultiColor)  # Use multi-color or single-color histogram
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtMacdBuffer_TF2 = Arr(0, 0.0)
ExtSignalBuffer_TF2 = Arr(0, 0.0)
ExtHistogramBuffer_TF2 = Arr(0, 0.0)
ExtHistogramColorBuffer_TF2 = Arr(0, 0.0)
ExtMacdArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 MACD buffer values
ExtSignalArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 signal buffer values
ExtHistogramArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 histogram buffer values
ExtHistogramColorArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 histogram color buffer values
PeriodRatio = 1  # ratio between timeframe 1 (TF1) and timeframe 2 (TF2)
PeriodSeconds_TF1 = 0  # TF1 period in seconds
PeriodSeconds_TF2 = 0  # TF2 period in seconds
ExtMacdHandle_TF2 = 0  # MACD handle TF2
ShowErrorMessages = True  # turn on/off error messages for debugging

def OnInit():
    global ExtMacdHandle_TF2, PeriodRatio, PeriodSeconds_TF1, PeriodSeconds_TF2
    SetIndexBuffer(0, ExtMacdBuffer_TF2, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSignalBuffer_TF2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHistogramBuffer_TF2, INDICATOR_DATA)
    SetIndexBuffer(3, ExtHistogramColorBuffer_TF2, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtMacdBuffer_TF2, True)
    ArraySetAsSeries(ExtSignalBuffer_TF2, True)
    ArraySetAsSeries(ExtHistogramBuffer_TF2, True)
    ArraySetAsSeries(ExtHistogramColorBuffer_TF2, True)
    ArraySetAsSeries(ExtMacdArray_TF2, True)
    ArraySetAsSeries(ExtSignalArray_TF2, True)
    ArraySetAsSeries(ExtHistogramArray_TF2, True)
    ArraySetAsSeries(ExtHistogramColorArray_TF2, True)
    PeriodSeconds_TF1 = PeriodSeconds()
    PeriodSeconds_TF2 = PeriodSeconds(InpTimeFrame_2)
    if PeriodSeconds_TF1 < PeriodSeconds_TF2:
        PeriodRatio = _idiv(PeriodSeconds_TF2, PeriodSeconds_TF1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD(' + _str(InpFastEMA) + ',' + _str(InpSlowEMA) + ',' + _str(InpSignalMA) + ')')
    ExtMacdHandle_TF2 = iCustom(None, InpTimeFrame_2, InpIndicator_TF1, InpFastEMA, InpSlowEMA, InpSignalMA, InpAppliedSignalMA, InpUseMultiColor, InpAppliedPrice)
    if ExtMacdHandle_TF2 == INVALID_HANDLE:
        Print('Error creating MACD_Histogram_MC indicator')
        return 1
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    ArraySetAsSeries(Time, True)
    bars_TF2 = Bars(None, InpTimeFrame_2)
    if bars_TF2 < (InpSlowEMA + InpSignalMA):
        return 0
    calculated_TF2 = 0
    calculated_TF2 = BarsCalculated(ExtMacdHandle_TF2)
    if calculated_TF2 < bars_TF2:
        if ShowErrorMessages:
            Print('Not all data of ExtMacdHandle_TF2 has been calculated (', calculated_TF2, ' bars). Error', GetLastError())
        return 0
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    convertedTime = 0
    for i in range(limit, 0 - 1, -1):
        if InpAppliedPrice != PRICE_OPEN:
            convertedTime = Time[i] + PeriodSeconds_TF1 - PeriodSeconds_TF2
        if InpAppliedPrice == PRICE_OPEN:
            convertedTime = Time[i]
        tempTimeArray_TF2 = Arr(0, 0)
        CopyTime(None, InpTimeFrame_2, calculated_TF2 - 1, 1, tempTimeArray_TF2)
        if convertedTime < tempTimeArray_TF2[0]:
            ExtMacdBuffer_TF2[i] = EMPTY_VALUE
            ExtSignalBuffer_TF2[i] = EMPTY_VALUE
            ExtHistogramBuffer_TF2[i] = EMPTY_VALUE
            ExtHistogramColorBuffer_TF2[i] = EMPTY_VALUE
            continue
        if CopyBuffer(ExtMacdHandle_TF2, 0, _DT(convertedTime), 1, ExtMacdArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting MACD TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtMacdBuffer_TF2[i] = ExtMacdArray_TF2[0]
        if CopyBuffer(ExtMacdHandle_TF2, 1, _DT(convertedTime), 1, ExtSignalArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting Signal TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtSignalBuffer_TF2[i] = ExtSignalArray_TF2[0]
        if CopyBuffer(ExtMacdHandle_TF2, 2, _DT(convertedTime), 1, ExtHistogramArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting Histogram TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtHistogramBuffer_TF2[i] = ExtHistogramArray_TF2[0]
        if CopyBuffer(ExtMacdHandle_TF2, 3, _DT(convertedTime), 1, ExtHistogramColorArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting Histogram Color TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtHistogramColorBuffer_TF2[i] = ExtHistogramColorArray_TF2[0]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdHistogramMcMtf(_MQL5Indicator):
    name = 'macd_histogram_mc_mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeFrame_2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Timeframe 2 (TF2) period
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpSignalMA': 9,  # Signal MA period
        'InpAppliedSignalMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Applied MA method for signal line
        'InpUseMultiColor': _Choice({0: 'MultiColor', 1: 'SingleColor'}, default=0),  # Use multi-color or single-color histogram
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

