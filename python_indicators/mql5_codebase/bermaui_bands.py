"""Bermaui Bands — converted from MQL5: MQL5 Indicators/Bermaui Bands LCS lite/Bermaui Bands.mq5

Copyright: Misha; Link: textyping@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Misha', 'link': 'textyping@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 1, 2: 0, 3: 0}, 'labels': {1: 'MiddleBB', 2: 'UpperBB', 3: 'LowerBB'}, 'levels': [], 'description': [], 'name': 'Bermaui Bands', 'source': 'MQL5 Indicators/Bermaui Bands LCS lite/Bermaui Bands.mq5', 'folder': 'Bermaui Bands LCS lite', 'inputs': [{'mql': 'candles', 'py': 'candles', 'param': 'candles', 'type': 'int', 'default': 50, 'label': 'Candles [Min=2]', 'sinput': False}, {'mql': 'deviation', 'py': 'deviation', 'param': 'deviation', 'type': 'double', 'default': 2.1, 'label': 'Deviation Multiplier [>0]', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
candles = _input('candles', 50)  # Candles [Min=2]
deviation = _input('deviation', 2.1)  # Deviation Multiplier [>0]
dev = 0.0
csd = Arr(0, 0.0)
bbMiddle = Arr(0, 0.0)
bbUpper = Arr(0, 0.0)
bbLower = Arr(0, 0.0)
maxValue = 0.0
minValue = 0.0
curValue = 0.0
handleStdDev = 0
handleMA = 0
handleBB = 0
MiddleBBBuffer = Arr(0, 0.0)
UpperBBBuffer = Arr(0, 0.0)
LowerBBBuffer = Arr(0, 0.0)

def OnInit():
    global handleBB, handleMA, handleStdDev
    SetIndexBuffer(0, MiddleBBBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpperBBBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowerBBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 2)
    PlotIndexSetInteger(2, PLOT_LINE_WIDTH, 2)
    handleStdDev = iStdDev(Symbol(), PERIOD_CURRENT, candles, 0, MODE_SMA, PRICE_CLOSE)
    handleMA = iMA(Symbol(), PERIOD_CURRENT, candles, 0, MODE_SMA, PRICE_CLOSE)
    handleBB = iBands(Symbol(), PERIOD_CURRENT, candles, 0, deviation, PRICE_CLOSE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global curValue, dev, maxValue, minValue
    for i in range(prev_calculated - 1, rates_total):
        if i < 0:
            continue
        if i <= (candles * 2):
            MiddleBBBuffer[i] = EMPTY_VALUE
            UpperBBBuffer[i] = EMPTY_VALUE
            LowerBBBuffer[i] = EMPTY_VALUE
            continue
        CopyBuffer(handleStdDev, 0, rates_total - i - 1, candles, csd)
        CopyBuffer(handleBB, BASE_LINE, rates_total - i - 1, 1, bbMiddle)
        CopyBuffer(handleBB, UPPER_BAND, rates_total - i - 1, 1, bbUpper)
        CopyBuffer(handleBB, LOWER_BAND, rates_total - i - 1, 1, bbLower)
        maxValue = csd[ArrayMaximum(csd)]
        minValue = csd[ArrayMinimum(csd)]
        curValue = csd[candles - 1]
        dev = _fdiv(maxValue - curValue, maxValue - minValue)
        MiddleBBBuffer[i] = bbMiddle[0]
        UpperBBBuffer[i] = bbMiddle[0] + (dev * (bbUpper[0] - bbMiddle[0]))
        LowerBBBuffer[i] = bbMiddle[0] + (dev * (bbLower[0] - bbMiddle[0]))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BermauiBands(_MQL5Indicator):
    name = 'Bermaui Bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'candles': 50,  # Candles [Min=2]
        'deviation': 2.1,  # Deviation Multiplier [>0]
    }

