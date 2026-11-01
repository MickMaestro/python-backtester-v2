"""zerolag_macd — converted from MQL5: MQL5 Indicators/ZeroLag MACD/zerolag_macd.mq5

ZeroLag Moving Average Convergence/Divergence
Copyright: Copyright 2010

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2010', 'link': '', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 3, 3: 3}, 'colors': {1: [11119017], 2: [32768], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'MACD', 2: 'Histogram up', 3: 'Histogram down'}, 'levels': [], 'description': ['ZeroLag Moving Average Convergence/Divergence'], 'name': 'zerolag_macd', 'source': 'MQL5 Indicators/ZeroLag MACD/zerolag_macd.mq5', 'folder': 'ZeroLag MACD', 'inputs': [{'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtMacdBuffer = Arr(0, 0.0)
ExtMacdUpBuffer = Arr(0, 0.0)
ExtMacdDownBuffer = Arr(0, 0.0)
ExtFastMaBuffer = Arr(0, 0.0)
ExtSlowMaBuffer = Arr(0, 0.0)
ExtFastResMaBuffer = Arr(0, 0.0)
ExtSlowResMaBuffer = Arr(0, 0.0)
ExtFastMaHandle = 0
ExtSlowMaHandle = 0

def OnInit():
    global ExtFastMaHandle, ExtSlowMaHandle
    SetIndexBuffer(0, ExtMacdBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMacdUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMacdDownBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtFastMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtSlowMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtFastResMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtSlowResMaBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpFastEMA - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ZeroLag MACD (' + _str(InpFastEMA) + ',' + _str(InpSlowEMA) + ')')
    ExtFastMaHandle = iMA(None, 0, InpFastEMA, 0, MODE_EMA, InpAppliedPrice)
    ExtSlowMaHandle = iMA(None, 0, InpSlowEMA, 0, MODE_EMA, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < InpFastEMA:
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
    if CopyBuffer(ExtFastMaHandle, 0, 0, to_copy, ExtFastMaBuffer) <= 0:
        Print('Getting fast EMA is failed! Error', GetLastError())
        return 0
    if CopyBuffer(ExtSlowMaHandle, 0, 0, to_copy, ExtSlowMaBuffer) <= 0:
        Print('Getting slow SMA is failed! Error', GetLastError())
        return 0
    limit = 0
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    ExtMacdUpBuffer[0] = 0.0
    ExtMacdDownBuffer[0] = 0.0
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpFastEMA, ExtFastMaBuffer, ExtFastResMaBuffer)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, InpSlowEMA, ExtSlowMaBuffer, ExtSlowResMaBuffer)
    for i in range(limit, rates_total):
        ExtMacdBuffer[i] = 10 * ((2 * ExtFastMaBuffer[i]) - ExtFastResMaBuffer[i] - ((2 * ExtSlowMaBuffer[i]) - ExtSlowResMaBuffer[i]))
        if i > 0:
            if ExtMacdBuffer[i] > ExtMacdBuffer[i - 1]:
                ExtMacdUpBuffer[i] = ExtMacdBuffer[i]
                ExtMacdDownBuffer[i] = 0.0
            else:
                ExtMacdDownBuffer[i] = ExtMacdBuffer[i]
                ExtMacdUpBuffer[i] = 0.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZerolagMacd(_MQL5Indicator):
    name = 'zerolag_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

