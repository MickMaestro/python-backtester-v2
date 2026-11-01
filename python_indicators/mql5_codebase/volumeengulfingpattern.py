"""VolumeEngulfingPattern — converted from MQL5: MQL5 Indicators/Engulfing Pattern Indicator with Volume Confirmation/VolumeEngulfingPattern.mq5

Detects bullish and bearish engulfing candlestick patterns.
Optional volume filter: highlights patterns with increasing volume.
Copyright: 2024, @ezhenrique; Link: https://www.mql5.com/en/users/ezhenrique; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2024, @ezhenrique', 'link': 'https://www.mql5.com/en/users/ezhenrique', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Detects bullish and bearish engulfing candlestick patterns.', 'Optional volume filter: highlights patterns with increasing volume.'], 'name': 'VolumeEngulfingPattern', 'source': 'MQL5 Indicators/Engulfing Pattern Indicator with Volume Confirmation/VolumeEngulfingPattern.mq5', 'folder': 'Engulfing Pattern Indicator with Volume Confirmation', 'inputs': [{'mql': 'BullishArrowColor', 'py': 'BullishArrowColor', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Color of the arrow for bullish engulfing', 'sinput': False}, {'mql': 'BearishArrowColor', 'py': 'BearishArrowColor', 'param': None, 'type': 'color', 'default': 4678655, 'label': 'Color of the arrow for bearish engulfing', 'sinput': False}, {'mql': 'UseVolumeFilter', 'py': 'UseVolumeFilter', 'param': 'UseVolumeFilter', 'type': 'bool', 'default': True, 'label': 'Enable volume confirmation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum CANDLE_MOVEMENT
UP = 1
DOWN = 0
_enum('CANDLE_MOVEMENT', {1: 'UP', 0: 'DOWN'})

# enum ENGULFING_PATTERN
BULLISH = 1
BEARISH = 0
NONE = -1
_enum('ENGULFING_PATTERN', {1: 'BULLISH', 0: 'BEARISH', -1: 'NONE'})

# ---- inputs and global variables
BullishArrowColor = _input('BullishArrowColor', clrLimeGreen)  # Color of the arrow for bullish engulfing
BearishArrowColor = _input('BearishArrowColor', clrTomato)  # Color of the arrow for bearish engulfing
UseVolumeFilter = _input('UseVolumeFilter', True)  # Enable volume confirmation
objectNames = Arr(0, "")
bullishBuffer = Arr(0, 0.0)
bearishBuffer = Arr(0, 0.0)

class CANDLE_STRUCTURE(MqlObject):
    _q_fields = ('open', 'high', 'low', 'close', 'volume', 'time', 'move')
    def __init__(self, *args):
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.volume = 0
        self.time = 0
        self.move = 0

def isEngulfingPattern(prevCandle, currentCandle):
    bullishCondition1 = prevCandle.move == DOWN and currentCandle.move == UP
    bullishCondition2 = currentCandle.open <= prevCandle.close and currentCandle.close > prevCandle.open
    bearishCondition1 = prevCandle.move == UP and currentCandle.move == DOWN
    bearishCondition2 = currentCandle.open >= prevCandle.close and currentCandle.close < prevCandle.open
    volumeCondition = False
    if UseVolumeFilter:
        volumeCondition = currentCandle.volume > prevCandle.volume
    else:
        volumeCondition = True
    if (bullishCondition1 and bullishCondition2) and volumeCondition:
        return BULLISH
    if (bearishCondition1 and bearishCondition2) and volumeCondition:
        return BEARISH
    return NONE

def OnInit():
    SetIndexBuffer(0, bullishBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, bearishBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_ARROW)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, BullishArrowColor)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, BearishArrowColor)
    PlotIndexSetString(0, PLOT_LABEL, 'Bullish Engulfing')
    PlotIndexSetString(1, PLOT_LABEL, 'Bearish Engulfing')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    candles = Arr(0, 0, factory=CANDLE_STRUCTURE)
    ArrayResize(candles, rates_total)
    ArrayInitialize(bullishBuffer, EMPTY_VALUE)
    ArrayInitialize(bearishBuffer, EMPTY_VALUE)
    for i in range(0, rates_total):
        candles[i].open = open[i]
        candles[i].high = high[i]
        candles[i].low = low[i]
        candles[i].close = close[i]
        candles[i].volume = tick_volume[i]
        candles[i].time = time[i]
        candles[i].move = (UP if (close[i] > open[i]) else DOWN)
    for i in range(1, rates_total - 1):
        pattern = isEngulfingPattern(candles[i - 1], candles[i])
        if pattern == BULLISH:
            bullishBuffer[i] = low[i] - (Point() * 10)
        if pattern == BEARISH:
            bearishBuffer[i] = high[i] + (Point() * 10)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeEngulfingPattern(_MQL5Indicator):
    name = 'VolumeEngulfingPattern'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'UseVolumeFilter': True,  # Enable volume confirmation
    }

