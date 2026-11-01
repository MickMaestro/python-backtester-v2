"""bb_macd — converted from MQL5: MQL5 Indicators/BB MACD/bb_macd.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 1}, 'colors': {1: [3749427], 2: [3329330, 65280, 13850042, 16711935], 3: [6908265]}, 'widths': {2: 2, 3: 1}, 'styles': {}, 'labels': {1: 'Bollinger bands of MACD', 2: 'MACD', 3: 'MACD signal'}, 'levels': [], 'description': [], 'name': 'bb_macd', 'source': 'MQL5 Indicators/BB MACD/bb_macd.mq5', 'folder': 'BB MACD', 'inputs': [{'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'int', 'default': 12, 'label': 'MACD fast EMA period', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'int', 'default': 26, 'label': 'MACD slow EMA period', 'sinput': False}, {'mql': 'SignalEMA', 'py': 'SignalEMA', 'param': 'SignalEMA', 'type': 'int', 'default': 9, 'label': 'Signal EMA period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Aplied price', 'sinput': False}, {'mql': 'StDv', 'py': 'StDv', 'param': 'StDv', 'type': 'double', 'default': 2.0, 'label': 'Bands deviation multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastEMA = _input('FastEMA', 12)  # MACD fast EMA period
SlowEMA = _input('SlowEMA', 26)  # MACD slow EMA period
SignalEMA = _input('SignalEMA', 9)  # Signal EMA period
Price = _input('Price', PRICE_CLOSE)  # Aplied price
StDv = _input('StDv', 2.0)  # Bands deviation multiplier
BBUpperBand = Arr(0, 0.0)
BBLowerBand = Arr(0, 0.0)
Macd = Arr(0, 0.0)
MacdColors = Arr(0, 0.0)
fastMA = Arr(0, 0.0)
slowMA = Arr(0, 0.0)
signalBuffer = Arr(0, 0.0)
FastMaHandle = 0
SlowMaHandle = 0

def OnInit():
    global FastMaHandle, SlowMaHandle
    SetIndexBuffer(0, BBUpperBand, INDICATOR_DATA)
    ArraySetAsSeries(BBUpperBand, True)
    SetIndexBuffer(1, BBLowerBand, INDICATOR_DATA)
    ArraySetAsSeries(BBLowerBand, True)
    SetIndexBuffer(2, Macd, INDICATOR_DATA)
    ArraySetAsSeries(Macd, True)
    SetIndexBuffer(3, MacdColors, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(MacdColors, True)
    SetIndexBuffer(4, signalBuffer, INDICATOR_DATA)
    ArraySetAsSeries(signalBuffer, True)
    SetIndexBuffer(5, fastMA, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(fastMA, True)
    SetIndexBuffer(6, slowMA, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(slowMA, True)
    FastMaHandle = iMA(None, 0, FastEMA, 0, MODE_EMA, Price)
    SlowMaHandle = iMA(None, 0, SlowEMA, 0, MODE_EMA, Price)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB macd (' + _str(FastEMA) + ',' + _str(SlowEMA) + ',' + _str(SignalEMA) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    last = (FastEMA if (FastEMA > SlowEMA) else SlowEMA)
    last = (SignalEMA if (SignalEMA > last) else last)
    if rates_total <= last:
        return 0
    limit = rates_total - prev_calculated
    if prev_calculated > 0:
        limit += 1
    if not checkCalculated(FastMaHandle, rates_total, 'fast MA'):
        return 0
    if not checkCalculated(SlowMaHandle, rates_total, 'slow MA'):
        return 0
    if not doCopy(FastMaHandle, fastMA, 0, limit, 'fast MA buffer'):
        return 0
    if not doCopy(SlowMaHandle, slowMA, 0, limit, 'slow MA buffer'):
        return 0
    if prev_calculated == 0:
        limit -= last
        for i in range(1, last + 1):
            Macd[rates_total - i] = 0.0
            MacdColors[rates_total - i] = 0.0
            signalBuffer[rates_total - i] = 0.0
            BBUpperBand[rates_total - i] = 0.0
            BBLowerBand[rates_total - i] = 0.0
    alpha = _fdiv(2.0, SignalEMA + 1.0)
    for i in range(limit, 0 - 1, -1):
        Macd[i] = fastMA[i] - slowMA[i]
        signalBuffer[i] = signalBuffer[i + 1] + (alpha * (Macd[i] - signalBuffer[i + 1]))
        standardDeviation = iDeviation(Macd, signalBuffer[i], SignalEMA, i)
        BBUpperBand[i] = signalBuffer[i] + (StDv * standardDeviation)
        BBLowerBand[i] = signalBuffer[i] - (StDv * standardDeviation)
        MacdColors[i] = MacdColors[i + 1]
        if Macd[i] > Macd[i + 1]:
            MacdColors[i] = (0 if (Macd[i] <= BBUpperBand[i] and Macd[i] >= BBLowerBand[i]) else 1)
        if Macd[i] < Macd[i + 1]:
            MacdColors[i] = (2 if (Macd[i] <= BBUpperBand[i] and Macd[i] >= BBLowerBand[i]) else 3)
    return rates_total

def iDeviation(array, dMA, period, shift):
    dSum = 0.0
    for i in range(0, period):
        dSum += (array[shift + i] - dMA) * (array[shift + i] - dMA)
    return MathSqrt(_fdiv(dSum, period))

def checkCalculated(bufferHandle, total, checkDescription):
    calculated = BarsCalculated(bufferHandle)
    if calculated < total:
        Print('Not all data of ' + checkDescription + ' calculated (', _str(total - calculated), ' un-calculated bars )')
        return False
    return True

def doCopy(bufferHandle, buffer, buffNum, copyCount, copyDescription):
    if CopyBuffer(bufferHandle, buffNum, 0, copyCount, buffer) <= 0:
        Print('Getting ' + copyDescription + ' failed! Error', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BbMacd(_MQL5Indicator):
    name = 'bb_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastEMA': 12,  # MACD fast EMA period
        'SlowEMA': 26,  # MACD slow EMA period
        'SignalEMA': 9,  # Signal EMA period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Aplied price
        'StDv': 2.0,  # Bands deviation multiplier
    }

