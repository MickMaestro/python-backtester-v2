"""keltnerchannelwithflatzone — converted from MQL5: MQL5 Indicators/KeltnerChannelWithFlatZone/keltnerchannelwithflatzone.mq5

Keltner Channel With Flat Zone indicator
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 8}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [13422920], 2: [8034025], 3: [8421504], 4: [11119017], 5: [16711680], 6: [255], 7: [16711680], 8: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, 'labels': {1: 'BullFill', 2: 'BearFill', 3: 'FlatFill', 4: 'MA', 5: 'FlatUp', 6: 'FlatDown', 7: 'Bull', 8: 'Bear'}, 'levels': [], 'description': ['Keltner Channel With Flat Zone indicator'], 'name': 'keltnerchannelwithflatzone', 'source': 'MQL5 Indicators/KeltnerChannelWithFlatZone/keltnerchannelwithflatzone.mq5', 'folder': 'KeltnerChannelWithFlatZone', 'inputs': [{'mql': 'InpMaPeriod', 'py': 'InpMaPeriod', 'param': 'InpMaPeriod', 'type': 'int', 'default': 10, 'label': 'МА period', 'sinput': False}, {'mql': 'InpMaMethod', 'py': 'InpMaMethod', 'param': 'InpMaMethod', 'type': 'int', 'default': 1, 'label': 'МА method', 'sinput': False}, {'mql': 'InpAtrPeriod', 'py': 'InpAtrPeriod', 'param': 'InpAtrPeriod', 'type': 'int', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpFlatMultiplier', 'py': 'InpFlatMultiplier', 'param': 'InpFlatMultiplier', 'type': 'double', 'default': 0.3, 'label': 'Ratio of flat', 'sinput': False}, {'mql': 'InpBandMultiplier', 'py': 'InpBandMultiplier', 'param': 'InpBandMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Ratio of channel boundaries', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMaPeriod = _input('InpMaPeriod', 10)  # МА period
InpMaMethod = _input('InpMaMethod', MODE_EMA)  # МА method
InpAtrPeriod = _input('InpAtrPeriod', 10)  # Period
InpFlatMultiplier = _input('InpFlatMultiplier', 0.3)  # Ratio of flat
InpBandMultiplier = _input('InpBandMultiplier', 2.0)  # Ratio of channel boundaries
BullFillBuffer1 = Arr(0, 0.0)
BullFillBuffer2 = Arr(0, 0.0)
BearFillBuffer1 = Arr(0, 0.0)
BearFillBuffer2 = Arr(0, 0.0)
FlatFillBuffer1 = Arr(0, 0.0)
FlatFillBuffer2 = Arr(0, 0.0)
MaBuffer = Arr(0, 0.0)
FlatUpBuffer = Arr(0, 0.0)
FlatDownBuffer = Arr(0, 0.0)
BullBuffer = Arr(0, 0.0)
BearBuffer = Arr(0, 0.0)
AtrBuffer = Arr(0, 0.0)
minRequiredBars = 0
maHandle = 0
atrHandle = 0

def OnInit():
    global atrHandle, maHandle, minRequiredBars
    minRequiredBars = MathMax(InpMaPeriod, InpAtrPeriod)
    maHandle = iMA(Symbol(), Period(), InpMaPeriod, 0, InpMaMethod, PRICE_CLOSE)
    if maHandle < 0:
        Print('Failed to create the МА indicator')
        return -1
    atrHandle = iATR(Symbol(), Period(), InpAtrPeriod)
    if atrHandle < 0:
        Print('Failed to create the ATR indicator')
        return -1
    SetIndexBuffer(0, BullFillBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, BullFillBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, BearFillBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, BearFillBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, FlatFillBuffer1, INDICATOR_DATA)
    SetIndexBuffer(5, FlatFillBuffer2, INDICATOR_DATA)
    SetIndexBuffer(6, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, FlatUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, FlatDownBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, BullBuffer, INDICATOR_DATA)
    SetIndexBuffer(10, BearBuffer, INDICATOR_DATA)
    SetIndexBuffer(11, AtrBuffer, INDICATOR_CALCULATIONS)
    for i in range(0, 8):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Keltner Channel with Flat Zone (' + _str(InpMaPeriod) + ', ' + _str(InpAtrPeriod) + ', ' + DoubleToString(InpFlatMultiplier, 2) + ', ' + DoubleToString(InpBandMultiplier, 2) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    startBar = 0
    calculated = 0
    toCopy = 0
    if rates_total < minRequiredBars:
        Print('Not enough data to calculate')
        return 0
    calculated = BarsCalculated(maHandle)
    if calculated < rates_total:
        Print('Not all data of the МА are calculated. Error #', GetLastError())
        return 0
    calculated = BarsCalculated(atrHandle)
    if calculated < rates_total:
        Print('Not all data of the ATR are calculated. Error #', GetLastError())
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        toCopy = rates_total
        startBar = minRequiredBars
    else:
        toCopy = rates_total - prev_calculated
        if prev_calculated > 0:
            toCopy += 1
        startBar = prev_calculated - 1
    if CopyBuffer(maHandle, 0, 0, toCopy, MaBuffer) < toCopy or CopyBuffer(atrHandle, 0, 0, toCopy, AtrBuffer) < toCopy:
        Print('Indicator data copy error')
        return 0
    for bar in range(startBar, rates_total):
        maValue = MaBuffer[bar]
        atrValue = AtrBuffer[bar]
        BullBuffer[bar] = maValue + (atrValue * InpBandMultiplier)
        BearBuffer[bar] = maValue - (atrValue * InpBandMultiplier)
        FlatUpBuffer[bar] = maValue + (atrValue * InpFlatMultiplier)
        FlatDownBuffer[bar] = maValue - (atrValue * InpFlatMultiplier)
        FlatFillBuffer1[bar] = FlatUpBuffer[bar]
        FlatFillBuffer2[bar] = FlatDownBuffer[bar]
        BullFillBuffer1[bar] = BullBuffer[bar]
        BullFillBuffer2[bar] = FlatUpBuffer[bar]
        BearFillBuffer1[bar] = FlatDownBuffer[bar]
        BearFillBuffer2[bar] = BearBuffer[bar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Keltnerchannelwithflatzone(_MQL5Indicator):
    name = 'keltnerchannelwithflatzone'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMaPeriod': 10,  # МА period
        'InpMaMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # МА method
        'InpAtrPeriod': 10,  # Period
        'InpFlatMultiplier': 0.3,  # Ratio of flat
        'InpBandMultiplier': 2.0,  # Ratio of channel boundaries
    }

