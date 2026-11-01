"""CF_HLCTrend — converted from MQL5: MQL5 Indicators/HLC Trend confirmation indicator/CF_HLCTrend.mq5

Copyright: mr_schmidt; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mr_schmidt', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16777215], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 2}, 'labels': {1: 'Long signal line', 2: 'Short signal line'}, 'levels': [], 'description': [], 'name': 'CF_HLCTrend', 'source': 'MQL5 Indicators/HLC Trend confirmation indicator/CF_HLCTrend.mq5', 'folder': 'HLC Trend confirmation indicator', 'inputs': [{'mql': 'InpMAMode', 'py': 'InpMAMode', 'param': 'InpMAMode', 'type': 'int', 'default': 0, 'label': 'Moving average method', 'sinput': False}, {'mql': 'InpHighPeriod', 'py': 'InpHighPeriod', 'param': 'InpHighPeriod', 'type': 'int', 'default': 34, 'label': 'High MA period', 'sinput': False}, {'mql': 'InpLowPeriod', 'py': 'InpLowPeriod', 'param': 'InpLowPeriod', 'type': 'int', 'default': 13, 'label': 'Low MA period', 'sinput': False}, {'mql': 'InpClosePeriod', 'py': 'InpClosePeriod', 'param': 'InpClosePeriod', 'type': 'int', 'default': 5, 'label': 'Close MA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMAMode = _input('InpMAMode', MODE_SMA)  # Moving average method
InpHighPeriod = _input('InpHighPeriod', 34)  # High MA period
InpLowPeriod = _input('InpLowPeriod', 13)  # Low MA period
InpClosePeriod = _input('InpClosePeriod', 5)  # Close MA period
handleHigh = 0
handleLow = 0
handleClose = 0
longBuffer = Arr(0, 0.0)
shortBuffer = Arr(0, 0.0)
bufferHigh = Arr(0, 0.0)
bufferLow = Arr(0, 0.0)
bufferClose = Arr(0, 0.0)

def OnInit():
    global handleClose, handleHigh, handleLow
    SetIndexBuffer(0, longBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, shortBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, bufferHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, bufferLow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, bufferClose, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(longBuffer, 1)
    ArraySetAsSeries(shortBuffer, 1)
    ArraySetAsSeries(bufferHigh, 1)
    ArraySetAsSeries(bufferLow, 1)
    ArraySetAsSeries(bufferClose, 1)
    if (handleHigh := iMA(Symbol(), PERIOD_CURRENT, InpHighPeriod, 0, InpMAMode, PRICE_HIGH)) == INVALID_HANDLE:
        Print('Error assigning high MA, lasterror: ', GetLastError())
        return INIT_FAILED
    if (handleLow := iMA(Symbol(), PERIOD_CURRENT, InpLowPeriod, 0, InpMAMode, PRICE_LOW)) == INVALID_HANDLE:
        Print('Error assigning low MA, lasterror: ', GetLastError())
        return INIT_FAILED
    if (handleClose := iMA(Symbol(), PERIOD_CURRENT, InpClosePeriod, 0, InpMAMode, PRICE_CLOSE)) == INVALID_HANDLE:
        Print('Error assigning close MA, lasterror: ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(handleHigh)
    IndicatorRelease(handleLow)
    IndicatorRelease(handleClose)
    return reason

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if False:
        return 0
    if BarsCalculated(handleHigh) < rates_total:
        return 0
    if BarsCalculated(handleLow) < rates_total:
        return 0
    if BarsCalculated(handleClose) < rates_total:
        return 0
    copyBars = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        copyBars = rates_total
    else:
        copyBars = rates_total - prev_calculated
        if prev_calculated > 0:
            copyBars += 1
    for i in range(0, rates_total):
        longBuffer[i] = NormalizeDouble(bufferClose[i] - bufferHigh[i], Digits())
        shortBuffer[i] = NormalizeDouble(bufferLow[i] - bufferClose[i], Digits())
    if CopyBuffer(handleHigh, 0, 0, rates_total, bufferHigh) <= 0:
        return 0
    if CopyBuffer(handleLow, 0, 0, rates_total, bufferLow) <= 0:
        return 0
    if CopyBuffer(handleClose, 0, 0, rates_total, bufferClose) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CFHLCTrend(_MQL5Indicator):
    name = 'CF_HLCTrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMAMode': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Moving average method
        'InpHighPeriod': 34,  # High MA period
        'InpLowPeriod': 13,  # Low MA period
        'InpClosePeriod': 5,  # Close MA period
    }

