"""macd_histogram — converted from MQL5: MQL5 Indicators/MACD with Histogram/macd_histogram.mq5

Moving Average Convergence/Divergence with Histogram
Copyright: Pablo Rego; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Pablo Rego', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 3}, 'colors': {1: [16711680], 2: [255], 3: [16776960]}, 'widths': {1: 2, 2: 1, 3: 4}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'MACD', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': ['Moving Average Convergence/Divergence with Histogram'], 'name': 'macd_histogram', 'source': 'MQL5 Indicators/MACD with Histogram/macd_histogram.mq5', 'folder': 'MACD with Histogram', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalSMA', 'py': 'InpSignalSMA', 'param': 'InpSignalSMA', 'type': 'int', 'default': 9, 'label': 'Signal SMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpSignalSMA = _input('InpSignalSMA', 9)  # Signal SMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtMacdBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
ExtHistogBuffer = Arr(0, 0.0)
ExtFastMaHandle = 0
ExtSlowMaHandle = 0

def OnInit():
    global ExtFastMaHandle, ExtSlowMaHandle
    SetIndexBuffer(0, ExtMacdBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSignalBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtHistogBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpSignalSMA - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD(' + _str(InpFastEMA) + ',' + _str(InpSlowEMA) + ',' + _str(InpSignalSMA) + ')')
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
        ExtHistogBuffer[i] = ExtMacdBuffer[i] - ExtSignalBuffer[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdHistogram(_MQL5Indicator):
    name = 'macd_histogram'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpSignalSMA': 9,  # Signal SMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

