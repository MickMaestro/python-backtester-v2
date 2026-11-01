"""OBOS — converted from MQL5: MQL5 Indicators/OBOS/OBOS.mq5

Overbought/Oversold Indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 11, 4: 5}, 'colors': {1: [255], 2: [32768], 3: [32768, 255, 16711680, 11119017], 4: [8421504]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Up', 2: 'Down', 3: 'Histogram', 4: 'Signal'}, 'levels': [], 'description': ['Overbought/Oversold Indicator'], 'name': 'OBOS', 'source': 'MQL5 Indicators/OBOS/OBOS.mq5', 'folder': 'OBOS', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 9, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 100.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -100.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 9)  # Period
InpOverbought = _input('InpOverbought', 100.0)  # Overbought
InpOversold = _input('InpOversold', -100.0)  # Oversold
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferHist1 = Arr(0, 0.0)
BufferHist2 = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSig = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferAvgRAW = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_ma = 0
handle_ma = 0
handle_dev = 0

def OnInit():
    global handle_dev, handle_ma, overbought, oversold, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    oversold = (0 if (InpOversold > 0) else InpOversold)
    overbought = (0 if (InpOverbought < 0) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHist1, INDICATOR_DATA)
    SetIndexBuffer(3, BufferHist2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BufferSig, INDICATOR_DATA)
    SetIndexBuffer(6, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferAvgRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferDev, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(3, PLOT_ARROW, 32)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'OBOS (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferHist1, True)
    ArraySetAsSeries(BufferHist2, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSig, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferAvgRAW, True)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDev, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_EMA, PRICE_WEIGHTED)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dev = iStdDev(None, PERIOD_CURRENT, period_ma, 0, MODE_EMA, PRICE_WEIGHTED)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferHist1, EMPTY_VALUE)
        ArrayInitialize(BufferHist2, EMPTY_VALUE)
        ArrayInitialize(BufferSig, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 3)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferAvgRAW, 0)
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferDev, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferPrice[i] = (high[i] + low[i] + close[i] + close[i]) / 4.0
        BufferRAW[i] = (_fdiv((BufferPrice[i] - BufferMA[i]) * 100.0, BufferDev[i]) if (BufferDev[i] != 0) else 0)
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferRAW, BufferAvgRAW) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferAvgRAW, BufferUP) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferUP, BufferDN) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferHist1[i] = BufferUP[i]
        BufferHist2[i] = BufferDN[i]
        BufferSig[i] = 0.0
        BufferColors[i] = 3.0
        if BufferUP[i + 1] < BufferUP[i] and BufferDN[i + 1] < BufferDN[i]:
            BufferSig[i] = Point()
            BufferColors[i] = 0.0
        elif BufferUP[i + 1] > BufferUP[i] and BufferDN[i + 1] > BufferDN[i]:
            BufferSig[i] = -Point()
            BufferColors[i] = 1.0
        else:
            BufferSig[i] = 0.0
            BufferColors[i] = 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OBOS(_MQL5Indicator):
    name = 'OBOS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 9,  # Period
        'InpOverbought': 100.0,  # Overbought
        'InpOversold': -100.0,  # Oversold
    }

