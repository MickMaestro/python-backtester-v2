"""Doteki Heikin Ashi — converted from MQL5: MQL5 Indicators/Dōteki Heikin Ashi (Dynamic Average Foot_Bar)/Doteki Heikin Ashi.mq5

_NAME_
MetaTrader 4/5 Indicator (Build 2018-10-16 08:51)
Copyright: Copyright \\x00A9 2018, Fernando M. I. Carreiro, All rights reserved; Link: https://www.mql5.com/en/users/FMIC; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.001', 'copyright': 'Copyright \\x00A9 2018, Fernando M. I. Carreiro, All rights reserved', 'link': 'https://www.mql5.com/en/users/FMIC', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 2237106, 55295]}, 'widths': {}, 'styles': {}, 'labels': {1: 'dhaOpen;dhaHigh;dhaLow;dhaClose'}, 'levels': [], 'description': ['_NAME_', 'MetaTrader 4/5 Indicator (Build 2018-10-16 08:51)'], 'name': 'Doteki Heikin Ashi', 'source': 'MQL5 Indicators/Dōteki Heikin Ashi (Dynamic Average Foot_Bar)/Doteki Heikin Ashi.mq5', 'folder': 'Dōteki Heikin Ashi (Dynamic Average Foot_Bar)', 'inputs': [{'mql': 'dblPeriod', 'py': 'dblPeriod', 'param': 'dblPeriod', 'type': 'double', 'default': 3.0, 'label': 'Averaging Period for Heikin Ashi (Original = 3.0)', 'sinput': False}, {'mql': 'boolZeroLag', 'py': 'boolZeroLag', 'param': 'boolZeroLag', 'type': 'bool', 'default': False, 'label': 'Use a Zero-Lag Exponential Averaging', 'sinput': False}, {'mql': 'boolLineGraph', 'py': 'boolLineGraph', 'param': 'boolLineGraph', 'type': 'bool', 'default': True, 'label': 'Set Chart Mode to Line Graph', 'sinput': False}, {'mql': 'boolHideLine', 'py': 'boolHideLine', 'param': 'boolHideLine', 'type': 'bool', 'default': False, 'label': 'Hide Close Line in Line Graph mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
dblPeriod = _input('dblPeriod', 3.0)  # Averaging Period for Heikin Ashi (Original = 3.0)
boolZeroLag = _input('boolZeroLag', False)  # Use a Zero-Lag Exponential Averaging
boolLineGraph = _input('boolLineGraph', True)  # Set Chart Mode to Line Graph
boolHideLine = _input('boolHideLine', False)  # Hide Close Line in Line Graph mode
enumChartMode = WRONG_VALUE  # Save the Initial Chart Mode for Deinitialisation
clrChartLine = WRONG_VALUE  # Save Colour of Line Graph for Deinitialisation
dblEMAWeight = 0.0  # Weight to be used for EMA
dblEMAComplement = 0.0  # Complement of the Weight to be used for EMA
dblBufferOpen = Arr(0, 0.0)  # Buffer Array for Opening Price
dblBufferHigh = Arr(0, 0.0)  # Buffer Array for High Price (or Low)
dblBufferLow = Arr(0, 0.0)  # Buffer Array for Low  Price (or High)
dblBufferClose = Arr(0, 0.0)  # Buffer Array for Closing Price
dblBufferEMA = Arr(0, 0.0)  # Buffer Array for Exponential Moving Average of Total Price
dblBufferDEMA = Arr(0, 0.0)  # Buffer Array for Double Exponential Moving Average
dblBufferZEMA = Arr(0, 0.0)  # Buffer Array for Zero-Lag Exponential Moving Average
dblBufferColour = Arr(0, 0.0)  # Buffer Array for Candle Colour

def intInvalidParameter(strText):
    Print('Error: ', strText)
    return INIT_PARAMETERS_INCORRECT

def OnInit():
    global clrChartLine, dblEMAComplement, dblEMAWeight, enumChartMode
    if dblPeriod <= 1.0:
        return intInvalidParameter('Invalid Averaging Period!')
    dblEMAWeight = _fdiv(2.0, dblPeriod + 1.0)
    dblEMAComplement = 1.0 - dblEMAWeight
    enumChartMode = WRONG_VALUE
    clrChartLine = WRONG_VALUE
    if boolLineGraph:
        enumChartMode = ChartGetInteger(0, CHART_MODE)
        ChartSetInteger(0, CHART_MODE, CHART_LINE)
        if boolHideLine:
            clrChartLine = _uint(ChartGetInteger(0, CHART_COLOR_CHART_LINE))
            ChartSetInteger(0, CHART_COLOR_CHART_LINE, clrNONE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, dblBufferOpen, INDICATOR_DATA)
    SetIndexBuffer(1, dblBufferHigh, INDICATOR_DATA)
    SetIndexBuffer(2, dblBufferLow, INDICATOR_DATA)
    SetIndexBuffer(3, dblBufferClose, INDICATOR_DATA)
    SetIndexBuffer(4, dblBufferColour, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, dblBufferEMA, INDICATOR_CALCULATIONS)
    if boolZeroLag:
        SetIndexBuffer(6, dblBufferDEMA, INDICATOR_CALCULATIONS)
        SetIndexBuffer(7, dblBufferZEMA, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(dblBufferColour, True)
    ArraySetAsSeries(dblBufferOpen, True)
    ArraySetAsSeries(dblBufferHigh, True)
    ArraySetAsSeries(dblBufferLow, True)
    ArraySetAsSeries(dblBufferClose, True)
    ArraySetAsSeries(dblBufferEMA, True)
    if boolZeroLag:
        ArraySetAsSeries(dblBufferDEMA, True)
        ArraySetAsSeries(dblBufferZEMA, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Dōteki Heikin Ashi' + ('(Z' if boolZeroLag else '(') + DoubleToString(dblPeriod, 3) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if boolLineGraph and enumChartMode != WRONG_VALUE:
        ChartSetInteger(0, CHART_MODE, enumChartMode)
    if boolHideLine and _int(clrChartLine) != WRONG_VALUE:
        ChartSetInteger(0, CHART_COLOR_CHART_LINE, clrChartLine)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    intPrevCalc = prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    boolUpCandle = False
    boolDownCandle = False
    dblClose = 0.0
    dblEMA = 0.0
    dblDEMA = 0.0
    dblZEMA = 0.0
    dblClosePrevious = 0.0
    dblEMAPrevious = 0.0
    dblDEMAPrevious = 0.0
    dblOpen = EMPTY_VALUE
    dblLow = 0.0
    dblHigh = 0.0
    intMax = rates_total - 1
    intLimit = rates_total - (1 if (intPrevCalc < 1) else intPrevCalc)
    intIndex = intLimit
    intIndexPrev = intIndex + 1
    while intIndex >= 0:
        dblLow = low[intIndex]
        dblHigh = high[intIndex]
        dblClose = NormalizeDouble((open[intIndex] + dblHigh + dblLow + close[intIndex]) * 0.25, Digits())
        dblBufferClose[intIndex] = dblClose
        if intIndex < intMax:
            dblClosePrevious = dblBufferClose[intIndexPrev]
            dblEMAPrevious = dblBufferEMA[intIndexPrev]
            dblEMA = dblEMAPrevious + ((dblClosePrevious - dblEMAPrevious) * dblEMAWeight)
            dblOpen = dblEMA
            if boolZeroLag:
                dblDEMAPrevious = dblBufferDEMA[intIndexPrev]
                dblDEMA = dblDEMAPrevious + ((dblEMA - dblDEMAPrevious) * dblEMAWeight)
                dblBufferDEMA[intIndex] = dblDEMA
                dblZEMA = (dblEMA * 2) - dblDEMA
                dblOpen = dblZEMA
                dblBufferZEMA[intIndex] = dblOpen
            dblLow = fmin(fmin(dblLow, dblOpen), dblClose)
            dblHigh = fmax(fmax(dblHigh, dblOpen), dblClose)
        else:
            dblEMA = open[intIndex] + ((close[intIndex] - open[intIndex]) * dblEMAWeight)
            dblDEMA = dblEMA
            dblZEMA = dblDEMA
            dblOpen = dblZEMA
            dblClosePrevious = dblOpen
        dblBufferEMA[intIndex] = dblEMA
        if boolZeroLag:
            dblBufferDEMA[intIndex] = dblDEMA
            dblBufferZEMA[intIndex] = dblZEMA
        dblOpen = NormalizeDouble(dblOpen, Digits())
        dblBufferOpen[intIndex] = dblOpen
        boolUpCandle = dblOpen < dblClose
        boolDownCandle = dblOpen > dblClose
        dblBufferLow[intIndex] = dblLow
        dblBufferHigh[intIndex] = dblHigh
        dblBufferColour[intIndex] = (0 if boolUpCandle else 1 if boolDownCandle else 2)
        intIndex -= 1
        intIndexPrev -= 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DotekiHeikinAshi(_MQL5Indicator):
    name = 'Doteki Heikin Ashi'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'dblPeriod': 3.0,  # Averaging Period for Heikin Ashi (Original = 3.0)
        'boolZeroLag': False,  # Use a Zero-Lag Exponential Averaging
        'boolLineGraph': True,  # Set Chart Mode to Line Graph
        'boolHideLine': False,  # Hide Close Line in Line Graph mode
    }

